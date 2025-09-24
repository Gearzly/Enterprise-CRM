"""
Bounded memory management for in-memory data structures to prevent memory leaks
and ensure optimal performance. Provides LRU caches, TTL-based expiration,
and memory-bounded collections.
"""
import logging
import threading
import time
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TypeVar, Generic, Callable, Iterator
from threading import Lock, RLock
from weakref import WeakSet
import gc
import sys
from enum import Enum

logger = logging.getLogger(__name__)

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class EvictionPolicy(Enum):
    """Cache eviction policies"""
    LRU = "lru"           # Least Recently Used
    LFU = "lfu"           # Least Frequently Used
    FIFO = "fifo"         # First In, First Out
    TTL = "ttl"           # Time To Live
    SIZE_BASED = "size"   # Size-based eviction


@dataclass
class CacheEntry:
    """Entry in a bounded cache with metadata"""
    value: Any
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    ttl_seconds: Optional[float] = None
    size_bytes: Optional[int] = None
    
    @property
    def is_expired(self) -> bool:
        """Check if entry has expired based on TTL"""
        if self.ttl_seconds is None:
            return False
        return time.time() - self.created_at > self.ttl_seconds
    
    @property
    def age_seconds(self) -> float:
        """Get age of entry in seconds"""
        return time.time() - self.created_at
    
    def touch(self):
        """Update last accessed time and increment access count"""
        self.last_accessed = time.time()
        self.access_count += 1


class BoundedLRUCache(Generic[K, V]):
    """LRU cache with memory bounds and TTL support"""
    
    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: Optional[float] = None,
        max_memory_mb: Optional[float] = None,
        eviction_policy: EvictionPolicy = EvictionPolicy.LRU
    ):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.eviction_policy = eviction_policy
        
        self._cache: OrderedDict[K, CacheEntry] = OrderedDict()
        self._lock = RLock()
        self._current_memory_bytes = 0
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "memory_evictions": 0,
            "ttl_evictions": 0,
            "size_evictions": 0
        }
        
        # Start cleanup thread if TTL is enabled
        if self.ttl_seconds:
            self._cleanup_thread = threading.Thread(target=self._cleanup_expired, daemon=True)
            self._cleanup_thread.start()
    
    def get(self, key: K, default: V = None) -> Optional[V]:
        """Get value from cache"""
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                self._stats["misses"] += 1
                return default
            
            if entry.is_expired:
                self._remove_entry(key, "ttl_evictions")
                self._stats["misses"] += 1
                return default
            
            # Update access information
            entry.touch()
            
            # Move to end for LRU (most recently used)
            if self.eviction_policy == EvictionPolicy.LRU:
                self._cache.move_to_end(key)
            
            self._stats["hits"] += 1
            return entry.value
    
    def put(self, key: K, value: V, ttl_seconds: Optional[float] = None) -> bool:
        """Put value in cache"""
        with self._lock:
            # Calculate size if memory limiting is enabled
            size_bytes = None
            if self.max_memory_bytes:
                size_bytes = self._estimate_size(value)
                
                # Check if single item exceeds max memory
                if size_bytes > self.max_memory_bytes:
                    logger.warning(f"Item size ({size_bytes} bytes) exceeds max memory limit")
                    return False
            
            # Remove existing entry if present
            if key in self._cache:
                self._remove_entry(key)
            
            # Create new entry
            entry = CacheEntry(
                value=value,
                ttl_seconds=ttl_seconds or self.ttl_seconds,
                size_bytes=size_bytes
            )
            
            # Ensure we have space (size and memory)
            self._ensure_capacity(size_bytes or 0)
            
            # Add to cache
            self._cache[key] = entry
            if size_bytes:
                self._current_memory_bytes += size_bytes
            
            return True
    
    def remove(self, key: K) -> bool:
        """Remove entry from cache"""
        with self._lock:
            if key in self._cache:
                self._remove_entry(key)
                return True
            return False
    
    def clear(self):
        """Clear all entries from cache"""
        with self._lock:
            self._cache.clear()
            self._current_memory_bytes = 0
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)
    
    def memory_usage_mb(self) -> float:
        """Get current memory usage in MB"""
        return self._current_memory_bytes / (1024 * 1024)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total_requests if total_requests > 0 else 0
        
        return {
            **self._stats,
            "total_requests": total_requests,
            "hit_rate": hit_rate,
            "current_size": len(self._cache),
            "max_size": self.max_size,
            "memory_usage_mb": self.memory_usage_mb(),
            "max_memory_mb": self.max_memory_bytes / (1024 * 1024) if self.max_memory_bytes else None
        }
    
    def _ensure_capacity(self, new_item_size: int):
        """Ensure cache has capacity for new item"""
        # Size-based eviction
        while len(self._cache) >= self.max_size:
            self._evict_one("size_evictions")
        
        # Memory-based eviction
        if self.max_memory_bytes:
            while self._current_memory_bytes + new_item_size > self.max_memory_bytes:
                if not self._evict_one("memory_evictions"):
                    break  # Can't evict any more items
    
    def _evict_one(self, stat_key: str) -> bool:
        """Evict one item based on eviction policy"""
        if not self._cache:
            return False
        
        if self.eviction_policy == EvictionPolicy.LRU:
            # Remove least recently used (first item)
            key = next(iter(self._cache))
        elif self.eviction_policy == EvictionPolicy.LFU:
            # Remove least frequently used
            key = min(self._cache.keys(), key=lambda k: self._cache[k].access_count)
        elif self.eviction_policy == EvictionPolicy.FIFO:
            # Remove oldest (first item)
            key = next(iter(self._cache))
        else:
            # Default to LRU
            key = next(iter(self._cache))
        
        self._remove_entry(key, stat_key)
        return True
    
    def _remove_entry(self, key: K, stat_key: str = "evictions"):
        """Remove entry and update memory usage"""
        entry = self._cache.pop(key, None)
        if entry:
            if entry.size_bytes:
                self._current_memory_bytes -= entry.size_bytes
            self._stats[stat_key] += 1
    
    def _cleanup_expired(self):
        """Background thread to clean up expired entries"""
        while True:
            try:
                time.sleep(min(self.ttl_seconds, 60))  # Check at least every minute
                
                with self._lock:
                    expired_keys = [
                        key for key, entry in self._cache.items()
                        if entry.is_expired
                    ]
                    
                    for key in expired_keys:
                        self._remove_entry(key, "ttl_evictions")
                    
                    if expired_keys:
                        logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
                        
            except Exception as e:
                logger.error(f"Error in cache cleanup thread: {e}")
    
    def _estimate_size(self, obj: Any) -> int:
        """Estimate memory size of an object"""
        return sys.getsizeof(obj)


class BoundedSet(Generic[T]):
    """A set with maximum size limit"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._items: OrderedDict[T, None] = OrderedDict()
        self._lock = Lock()
    
    def add(self, item: T):
        """Add item to set"""
        with self._lock:
            if item in self._items:
                # Move to end (most recently added)
                self._items.move_to_end(item)
            else:
                # Add new item
                self._items[item] = None
                
                # Remove oldest if over limit
                while len(self._items) > self.max_size:
                    self._items.popitem(last=False)
    
    def remove(self, item: T) -> bool:
        """Remove item from set"""
        with self._lock:
            if item in self._items:
                del self._items[item]
                return True
            return False
    
    def __contains__(self, item: T) -> bool:
        """Check if item is in set"""
        return item in self._items
    
    def __len__(self) -> int:
        """Get size of set"""
        return len(self._items)
    
    def clear(self):
        """Clear all items"""
        with self._lock:
            self._items.clear()


class BoundedList(Generic[T]):
    """A list with maximum size limit using circular buffer"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._items: List[Optional[T]] = [None] * max_size
        self._start = 0
        self._size = 0
        self._lock = Lock()
    
    def append(self, item: T):
        """Add item to end of list"""
        with self._lock:
            if self._size < self.max_size:
                # Still have space
                index = (self._start + self._size) % self.max_size
                self._items[index] = item
                self._size += 1
            else:
                # Overwrite oldest item
                self._items[self._start] = item
                self._start = (self._start + 1) % self.max_size
    
    def __len__(self) -> int:
        """Get current size"""
        return self._size
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over items"""
        with self._lock:
            for i in range(self._size):
                index = (self._start + i) % self.max_size
                yield self._items[index]
    
    def clear(self):
        """Clear all items"""
        with self._lock:
            self._items = [None] * self.max_size
            self._start = 0
            self._size = 0


class MemoryMonitor:
    """Monitor and manage memory usage across bounded collections"""
    
    def __init__(self):
        self._collections: WeakSet = WeakSet()
        self._lock = Lock()
        self._stats = defaultdict(int)
    
    def register(self, collection):
        """Register a collection for monitoring"""
        with self._lock:
            self._collections.add(collection)
    
    def get_total_memory_usage(self) -> Dict[str, Any]:
        """Get total memory usage across all collections"""
        total_memory = 0
        collection_count = 0
        
        with self._lock:
            for collection in self._collections:
                if hasattr(collection, 'memory_usage_mb'):
                    total_memory += collection.memory_usage_mb()
                collection_count += 1
        
        return {
            "total_memory_mb": total_memory,
            "collection_count": collection_count,
            "python_memory_mb": self._get_python_memory_usage()
        }
    
    def cleanup_all(self):
        """Force cleanup on all registered collections"""
        with self._lock:
            for collection in self._collections:
                if hasattr(collection, 'clear'):
                    collection.clear()
        
        # Force garbage collection
        gc.collect()
    
    def _get_python_memory_usage(self) -> float:
        """Get current Python process memory usage"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)  # MB
        except ImportError:
            return 0.0


# Global memory monitor
memory_monitor = MemoryMonitor()


# Factory functions for common use cases
def create_session_cache(max_size: int = 1000, ttl_minutes: int = 30) -> BoundedLRUCache:
    """Create a cache for session data"""
    cache = BoundedLRUCache(
        max_size=max_size,
        ttl_seconds=ttl_minutes * 60,
        max_memory_mb=100,  # Limit to 100MB
        eviction_policy=EvictionPolicy.LRU
    )
    memory_monitor.register(cache)
    return cache


def create_mfa_code_storage(max_size: int = 10000, ttl_minutes: int = 5) -> BoundedLRUCache:
    """Create storage for MFA codes with automatic expiration"""
    cache = BoundedLRUCache(
        max_size=max_size,
        ttl_seconds=ttl_minutes * 60,
        max_memory_mb=10,  # Limit to 10MB
        eviction_policy=EvictionPolicy.TTL
    )
    memory_monitor.register(cache)
    return cache


def create_device_tracking(max_size: int = 5000) -> BoundedSet:
    """Create bounded storage for device tracking"""
    devices = BoundedSet(max_size=max_size)
    memory_monitor.register(devices)
    return devices


def create_activity_log(max_size: int = 10000) -> BoundedList:
    """Create bounded list for activity logging"""
    log = BoundedList(max_size=max_size)
    memory_monitor.register(log)
    return log


# Utility functions
def get_memory_stats() -> Dict[str, Any]:
    """Get comprehensive memory statistics"""
    return memory_monitor.get_total_memory_usage()


def cleanup_all_memory():
    """Cleanup all bounded collections and force garbage collection"""
    memory_monitor.cleanup_all()


# Configuration from environment
def get_memory_config() -> Dict[str, int]:
    """Get memory configuration from environment variables"""
    import os
    
    return {
        "session_cache_size": int(os.getenv("MEMORY_SESSION_CACHE_SIZE", "1000")),
        "session_ttl_minutes": int(os.getenv("MEMORY_SESSION_TTL_MINUTES", "30")),
        "mfa_cache_size": int(os.getenv("MEMORY_MFA_CACHE_SIZE", "10000")),
        "mfa_ttl_minutes": int(os.getenv("MEMORY_MFA_TTL_MINUTES", "5")),
        "device_tracking_size": int(os.getenv("MEMORY_DEVICE_TRACKING_SIZE", "5000")),
        "activity_log_size": int(os.getenv("MEMORY_ACTIVITY_LOG_SIZE", "10000")),
        "max_memory_mb": int(os.getenv("MEMORY_MAX_TOTAL_MB", "500"))
    }