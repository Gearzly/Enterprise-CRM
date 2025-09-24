"""
Comprehensive rate limiting system for authentication endpoints and API protection.
Provides multiple rate limiting strategies including sliding window, token bucket,
and adaptive rate limiting with Redis backend support.
"""
import time
import logging
import hashlib
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from threading import Lock

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import redis
import os
from dotenv import load_dotenv

from ..memory.bounded_collections import BoundedLRUCache

load_dotenv()
logger = logging.getLogger(__name__)


class RateLimitStrategy(Enum):
    """Rate limiting strategies"""
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"
    FIXED_WINDOW = "fixed_window"
    ADAPTIVE = "adaptive"


class RateLimitScope(Enum):
    """Rate limit scopes"""
    GLOBAL = "global"
    PER_IP = "per_ip"
    PER_USER = "per_user"
    PER_ENDPOINT = "per_endpoint"


@dataclass
class RateLimitRule:
    """Rate limiting rule configuration"""
    requests: int                    # Number of requests allowed
    window_seconds: int             # Time window in seconds
    strategy: RateLimitStrategy = RateLimitStrategy.SLIDING_WINDOW
    scope: RateLimitScope = RateLimitScope.PER_IP
    burst_multiplier: float = 1.5   # Allow burst requests (token bucket)
    cooldown_seconds: int = 300     # Cooldown period after limit exceeded


@dataclass
class RateLimitState:
    """Current rate limit state"""
    requests_made: int = 0
    window_start: float = 0
    last_request: float = 0
    tokens: float = 0  # For token bucket
    blocked_until: float = 0
    violation_count: int = 0


class RateLimiter:
    """Base rate limiter class"""
    
    def __init__(self, rule: RateLimitRule, use_redis: bool = True):
        self.rule = rule
        self.use_redis = use_redis
        self._redis_client = None
        self._memory_cache = BoundedLRUCache(max_size=10000, ttl_seconds=rule.window_seconds * 2)
        self._lock = Lock()
        
        if use_redis:
            try:
                redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/1")
                self._redis_client = redis.from_url(redis_url, decode_responses=True)
                self._redis_client.ping()
                logger.info("Rate limiter using Redis backend")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis, falling back to memory: {e}")
                self.use_redis = False
    
    def check_rate_limit(self, identifier: str) -> Tuple[bool, Dict[str, Any]]:
        """Check if request is within rate limit"""
        current_time = time.time()
        
        # Get current state
        state = self._get_state(identifier)
        
        # Check if currently blocked
        if state.blocked_until > current_time:
            remaining_cooldown = int(state.blocked_until - current_time)
            return False, {
                "allowed": False,
                "reason": "rate_limit_exceeded",
                "retry_after": remaining_cooldown,
                "violation_count": state.violation_count
            }
        
        # Apply rate limiting strategy
        allowed, new_state, info = self._apply_strategy(state, current_time)
        
        # Update state
        self._set_state(identifier, new_state)
        
        # If request was denied, apply cooldown for repeated violations
        if not allowed:
            new_state.violation_count += 1
            if new_state.violation_count >= 3:  # After 3 violations, apply cooldown
                new_state.blocked_until = current_time + self.rule.cooldown_seconds
                self._set_state(identifier, new_state)
                info["cooldown_applied"] = True
        
        return allowed, info
    
    def _apply_strategy(self, state: RateLimitState, current_time: float) -> Tuple[bool, RateLimitState, Dict[str, Any]]:
        """Apply specific rate limiting strategy"""
        if self.rule.strategy == RateLimitStrategy.SLIDING_WINDOW:
            return self._sliding_window(state, current_time)
        elif self.rule.strategy == RateLimitStrategy.TOKEN_BUCKET:
            return self._token_bucket(state, current_time)
        elif self.rule.strategy == RateLimitStrategy.FIXED_WINDOW:
            return self._fixed_window(state, current_time)
        elif self.rule.strategy == RateLimitStrategy.ADAPTIVE:
            return self._adaptive_limiting(state, current_time)
        else:
            return self._sliding_window(state, current_time)
    
    def _sliding_window(self, state: RateLimitState, current_time: float) -> Tuple[bool, RateLimitState, Dict[str, Any]]:
        """Sliding window rate limiting"""
        window_start = current_time - self.rule.window_seconds
        
        # Reset if we're starting a new tracking period
        if state.window_start < window_start:
            state.requests_made = 0
            state.window_start = current_time
        
        # Check if we can make the request
        if state.requests_made >= self.rule.requests:
            return False, state, {
                "allowed": False,
                "requests_remaining": 0,
                "reset_time": state.window_start + self.rule.window_seconds,
                "retry_after": int((state.window_start + self.rule.window_seconds) - current_time)
            }
        
        # Allow the request
        state.requests_made += 1
        state.last_request = current_time
        
        return True, state, {
            "allowed": True,
            "requests_remaining": self.rule.requests - state.requests_made,
            "reset_time": state.window_start + self.rule.window_seconds,
            "window_seconds": self.rule.window_seconds
        }
    
    def _token_bucket(self, state: RateLimitState, current_time: float) -> Tuple[bool, RateLimitState, Dict[str, Any]]:
        """Token bucket rate limiting"""
        # Initialize tokens if first request
        if state.tokens == 0 and state.last_request == 0:
            state.tokens = self.rule.requests
        
        # Add tokens based on time passed
        time_passed = current_time - state.last_request if state.last_request > 0 else 0
        tokens_to_add = (time_passed / self.rule.window_seconds) * self.rule.requests
        max_tokens = self.rule.requests * self.rule.burst_multiplier
        
        state.tokens = min(max_tokens, state.tokens + tokens_to_add)
        state.last_request = current_time
        
        # Check if we have tokens available
        if state.tokens < 1:
            return False, state, {
                "allowed": False,
                "tokens_remaining": state.tokens,
                "retry_after": int((1 - state.tokens) * (self.rule.window_seconds / self.rule.requests))
            }
        
        # Consume a token
        state.tokens -= 1
        
        return True, state, {
            "allowed": True,
            "tokens_remaining": int(state.tokens),
            "bucket_size": max_tokens
        }
    
    def _fixed_window(self, state: RateLimitState, current_time: float) -> Tuple[bool, RateLimitState, Dict[str, Any]]:
        """Fixed window rate limiting"""
        window_number = int(current_time // self.rule.window_seconds)
        current_window_start = window_number * self.rule.window_seconds
        
        # Reset if we're in a new window
        if state.window_start != current_window_start:
            state.requests_made = 0
            state.window_start = current_window_start
        
        # Check limit
        if state.requests_made >= self.rule.requests:
            next_window = (window_number + 1) * self.rule.window_seconds
            return False, state, {
                "allowed": False,
                "requests_remaining": 0,
                "reset_time": next_window,
                "retry_after": int(next_window - current_time)
            }
        
        # Allow request
        state.requests_made += 1
        
        return True, state, {
            "allowed": True,
            "requests_remaining": self.rule.requests - state.requests_made,
            "reset_time": current_window_start + self.rule.window_seconds
        }
    
    def _adaptive_limiting(self, state: RateLimitState, current_time: float) -> Tuple[bool, RateLimitState, Dict[str, Any]]:
        """Adaptive rate limiting based on violation history"""
        # Start with base rate limit
        current_limit = self.rule.requests
        
        # Reduce limit based on violation count
        if state.violation_count > 0:
            reduction_factor = 1 - (state.violation_count * 0.2)  # Reduce by 20% per violation
            current_limit = max(1, int(current_limit * reduction_factor))
        
        # Create temporary rule with adjusted limit
        temp_rule = RateLimitRule(
            requests=current_limit,
            window_seconds=self.rule.window_seconds,
            strategy=RateLimitStrategy.SLIDING_WINDOW
        )
        
        # Use sliding window with adjusted limit
        old_rule = self.rule
        self.rule = temp_rule
        result = self._sliding_window(state, current_time)
        self.rule = old_rule
        
        # Add adaptive info
        allowed, new_state, info = result
        info["adaptive_limit"] = current_limit
        info["violation_count"] = state.violation_count
        
        return allowed, new_state, info
    
    def _get_state(self, identifier: str) -> RateLimitState:
        """Get current rate limit state"""
        key = f"rate_limit:{self.rule.scope.value}:{identifier}"
        
        if self.use_redis and self._redis_client:
            try:
                data = self._redis_client.hgetall(key)
                if data:
                    return RateLimitState(
                        requests_made=int(data.get("requests_made", 0)),
                        window_start=float(data.get("window_start", 0)),
                        last_request=float(data.get("last_request", 0)),
                        tokens=float(data.get("tokens", 0)),
                        blocked_until=float(data.get("blocked_until", 0)),
                        violation_count=int(data.get("violation_count", 0))
                    )
            except Exception as e:
                logger.error(f"Redis error in get_state: {e}")
        
        # Fallback to memory cache
        cached_state = self._memory_cache.get(key)
        return cached_state if cached_state else RateLimitState()
    
    def _set_state(self, identifier: str, state: RateLimitState):
        """Set rate limit state"""
        key = f"rate_limit:{self.rule.scope.value}:{identifier}"
        
        if self.use_redis and self._redis_client:
            try:
                data = {
                    "requests_made": state.requests_made,
                    "window_start": state.window_start,
                    "last_request": state.last_request,
                    "tokens": state.tokens,
                    "blocked_until": state.blocked_until,
                    "violation_count": state.violation_count
                }
                self._redis_client.hset(key, mapping=data)
                self._redis_client.expire(key, self.rule.window_seconds * 2)
                return
            except Exception as e:
                logger.error(f"Redis error in set_state: {e}")
        
        # Fallback to memory cache
        self._memory_cache.put(key, state, ttl_seconds=self.rule.window_seconds * 2)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for FastAPI"""
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default rate limiting rules"""
        # Authentication endpoints - strict limits
        auth_rule = RateLimitRule(
            requests=5,  # 5 requests
            window_seconds=300,  # per 5 minutes
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            scope=RateLimitScope.PER_IP,
            cooldown_seconds=600  # 10 minute cooldown
        )
        
        # Registration endpoints - very strict
        register_rule = RateLimitRule(
            requests=3,  # 3 attempts
            window_seconds=3600,  # per hour
            strategy=RateLimitStrategy.FIXED_WINDOW,
            scope=RateLimitScope.PER_IP,
            cooldown_seconds=1800  # 30 minute cooldown
        )
        
        # Password reset - moderate limits
        password_reset_rule = RateLimitRule(
            requests=3,  # 3 requests
            window_seconds=900,  # per 15 minutes
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            scope=RateLimitScope.PER_IP,
            cooldown_seconds=900
        )
        
        # MFA endpoints - strict but higher than auth
        mfa_rule = RateLimitRule(
            requests=10,  # 10 attempts
            window_seconds=300,  # per 5 minutes
            strategy=RateLimitStrategy.TOKEN_BUCKET,
            scope=RateLimitScope.PER_IP,
            cooldown_seconds=300
        )
        
        # General API endpoints - generous limits
        api_rule = RateLimitRule(
            requests=100,  # 100 requests
            window_seconds=60,  # per minute
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            scope=RateLimitScope.PER_IP
        )
        
        # Setup rate limiters
        self.rate_limiters = {
            "/api/superadmin/security/auth/token": RateLimiter(auth_rule),
            "/api/superadmin/security/auth/register": RateLimiter(register_rule),
            "/api/superadmin/security/auth/refresh": RateLimiter(auth_rule),
            "/api/superadmin/security/auth/reset-password": RateLimiter(password_reset_rule),
            "/api/superadmin/security/auth/mfa": RateLimiter(mfa_rule),
            "/api": RateLimiter(api_rule),  # Default for all API endpoints
        }
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process rate limiting for requests"""
        
        # Skip rate limiting for certain paths
        skip_paths = ["/docs", "/openapi.json", "/favicon.ico", "/health"]
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_identifier(request)
        
        # Find applicable rate limiter
        rate_limiter = self._get_rate_limiter(request.url.path)
        
        if rate_limiter:
            # Check rate limit
            allowed, info = rate_limiter.check_rate_limit(client_id)
            
            if not allowed:
                # Log rate limit violation
                logger.warning(f"Rate limit exceeded for {client_id} on {request.url.path}: {info}")
                
                # Create rate limit response
                response_headers = {
                    "X-RateLimit-Limit": str(rate_limiter.rule.requests),
                    "X-RateLimit-Window": str(rate_limiter.rule.window_seconds),
                    "X-RateLimit-Remaining": "0",
                }
                
                if "retry_after" in info:
                    response_headers["Retry-After"] = str(info["retry_after"])
                
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": "Too many requests. Please try again later.",
                        **info
                    },
                    headers=response_headers
                )
            
            # Add rate limit headers to successful requests
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(rate_limiter.rule.requests)
            response.headers["X-RateLimit-Window"] = str(rate_limiter.rule.window_seconds)
            response.headers["X-RateLimit-Remaining"] = str(info.get("requests_remaining", 0))
            
            if "reset_time" in info:
                response.headers["X-RateLimit-Reset"] = str(int(info["reset_time"]))
            
            return response
        
        return await call_next(request)
    
    def _get_client_identifier(self, request: Request) -> str:
        """Get client identifier for rate limiting"""
        # Try to get real IP from headers (for proxy setups)
        real_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
            request.headers.get("X-Real-IP", "") or
            (request.client.host if request.client else "unknown")
        )
        
        # For user-based rate limiting, you might want to include user ID
        # if hasattr(request.state, 'user') and request.state.user:
        #     return f"{real_ip}:{request.state.user.id}"
        
        return real_ip
    
    def _get_rate_limiter(self, path: str) -> Optional[RateLimiter]:
        """Get appropriate rate limiter for path"""
        # Exact match first
        if path in self.rate_limiters:
            return self.rate_limiters[path]
        
        # Pattern matching
        for pattern, limiter in self.rate_limiters.items():
            if path.startswith(pattern):
                return limiter
        
        return None


class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts limits based on system load"""
    
    def __init__(self):
        self.base_limits = {}
        self.current_limits = {}
        self.system_load_factor = 1.0
        self._lock = Lock()
    
    def set_base_limit(self, endpoint: str, requests: int, window_seconds: int):
        """Set base rate limit for an endpoint"""
        with self._lock:
            self.base_limits[endpoint] = RateLimitRule(requests, window_seconds)
            self.current_limits[endpoint] = requests
    
    def update_system_load(self, cpu_percent: float, memory_percent: float, response_time_ms: float):
        """Update system load factor"""
        # Calculate load factor based on system metrics
        load_factors = []
        
        if cpu_percent > 80:
            load_factors.append(0.5)  # Reduce by 50% if CPU is high
        elif cpu_percent > 60:
            load_factors.append(0.7)  # Reduce by 30% if CPU is moderate
        
        if memory_percent > 85:
            load_factors.append(0.6)  # Reduce by 40% if memory is high
        
        if response_time_ms > 1000:
            load_factors.append(0.8)  # Reduce by 20% if response time is slow
        
        # Use the most restrictive factor
        self.system_load_factor = min(load_factors) if load_factors else 1.0
        
        # Update current limits
        with self._lock:
            for endpoint, base_rule in self.base_limits.items():
                self.current_limits[endpoint] = int(base_rule.requests * self.system_load_factor)
    
    def get_current_limit(self, endpoint: str) -> int:
        """Get current rate limit for endpoint"""
        return self.current_limits.get(endpoint, 100)  # Default limit


# Utility functions
def create_auth_rate_limiter() -> RateLimiter:
    """Create rate limiter specifically for authentication"""
    rule = RateLimitRule(
        requests=5,
        window_seconds=300,
        strategy=RateLimitStrategy.ADAPTIVE,
        scope=RateLimitScope.PER_IP,
        cooldown_seconds=600
    )
    return RateLimiter(rule)


def create_api_rate_limiter() -> RateLimiter:
    """Create rate limiter for general API use"""
    rule = RateLimitRule(
        requests=100,
        window_seconds=60,
        strategy=RateLimitStrategy.SLIDING_WINDOW,
        scope=RateLimitScope.PER_IP
    )
    return RateLimiter(rule)


def get_rate_limit_stats(rate_limiter: RateLimiter, identifier: str) -> Dict[str, Any]:
    """Get rate limit statistics for a client"""
    state = rate_limiter._get_state(identifier)
    current_time = time.time()
    
    return {
        "requests_made": state.requests_made,
        "violation_count": state.violation_count,
        "blocked_until": state.blocked_until,
        "is_blocked": state.blocked_until > current_time,
        "last_request": datetime.fromtimestamp(state.last_request) if state.last_request > 0 else None,
        "rule": {
            "requests": rate_limiter.rule.requests,
            "window_seconds": rate_limiter.rule.window_seconds,
            "strategy": rate_limiter.rule.strategy.value,
            "scope": rate_limiter.rule.scope.value
        }
    }


# Global adaptive rate limiter instance
adaptive_limiter = AdaptiveRateLimiter()