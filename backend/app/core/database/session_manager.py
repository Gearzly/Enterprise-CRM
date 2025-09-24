"""
Standardized database session management with comprehensive error handling,
transaction management, and connection pooling optimization.
"""
import logging
from contextlib import contextmanager, asynccontextmanager
from typing import AsyncGenerator, Generator, Optional, Callable, Any, Dict
from functools import wraps
import asyncio
import time

from fastapi import Depends, HTTPException, status
from sqlalchemy import create_engine, event, pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError, TimeoutError
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration and connection settings"""
    
    def __init__(self):
        self.database_url = self._get_database_url()
        self.async_database_url = self._get_async_database_url()
        
        # Connection pool settings
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "20"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "30"))
        self.pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "300"))
        
        # Transaction settings
        self.statement_timeout = int(os.getenv("DB_STATEMENT_TIMEOUT", "30"))
        self.lock_timeout = int(os.getenv("DB_LOCK_TIMEOUT", "10"))
        
        # Retry settings
        self.max_retries = int(os.getenv("DB_MAX_RETRIES", "3"))
        self.retry_delay = float(os.getenv("DB_RETRY_DELAY", "1.0"))
    
    def _get_database_url(self) -> str:
        """Get synchronous database URL"""
        url = os.getenv("DATABASE_URL")
        if not url:
            raise ValueError("DATABASE_URL environment variable is not set")
        return url
    
    def _get_async_database_url(self) -> str:
        """Get asynchronous database URL"""
        url = self._get_database_url()
        # Convert to async URL if needed
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("mysql://"):
            return url.replace("mysql://", "mysql+aiomysql://", 1)
        return url


class DatabaseManager:
    """Centralized database connection and session management"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._sync_engine = None
        self._async_engine = None
        self._sync_session_factory = None
        self._async_session_factory = None
        self._connection_pool_stats = {
            "total_connections": 0,
            "active_connections": 0,
            "checked_out_connections": 0,
            "pool_size": 0,
            "checked_in_connections": 0,
        }
        
        self._setup_sync_engine()
        self._setup_async_engine()
    
    def _setup_sync_engine(self):
        """Setup synchronous database engine"""
        self._sync_engine = create_engine(
            self.config.database_url,
            poolclass=QueuePool,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow,
            pool_pre_ping=True,
            pool_recycle=self.config.pool_recycle,
            pool_timeout=self.config.pool_timeout,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            echo_pool=os.getenv("DB_ECHO_POOL", "false").lower() == "true",
            connect_args={
                "options": f"-c statement_timeout={self.config.statement_timeout}s "
                          f"-c lock_timeout={self.config.lock_timeout}s"
            } if "postgresql" in self.config.database_url else {}
        )
        
        # Setup event listeners for monitoring
        self._setup_engine_events(self._sync_engine)
        
        # Create session factory
        self._sync_session_factory = sessionmaker(
            bind=self._sync_engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
    
    def _setup_async_engine(self):
        """Setup asynchronous database engine"""
        try:
            self._async_engine = create_async_engine(
                self.config.async_database_url,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                echo=os.getenv("DB_ECHO", "false").lower() == "true"
            )
            
            # Create async session factory
            self._async_session_factory = async_sessionmaker(
                bind=self._async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
        except Exception as e:
            logger.warning(f"Failed to setup async engine: {e}. Async operations will not be available.")
            self._async_engine = None
            self._async_session_factory = None
    
    def _setup_engine_events(self, engine):
        """Setup event listeners for monitoring and debugging"""
        
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """Set database-specific pragmas and settings"""
            if "sqlite" in str(engine.url):
                # SQLite specific settings
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.close()
        
        @event.listens_for(engine, "checkout")
        def log_connection_checkout(dbapi_connection, connection_record, connection_proxy):
            """Log connection checkout for monitoring"""
            self._connection_pool_stats["checked_out_connections"] += 1
            logger.debug("Database connection checked out")
        
        @event.listens_for(engine, "checkin")
        def log_connection_checkin(dbapi_connection, connection_record):
            """Log connection checkin for monitoring"""
            self._connection_pool_stats["checked_in_connections"] += 1
            logger.debug("Database connection checked in")
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with proper error handling and cleanup"""
        if not self._sync_session_factory:
            raise RuntimeError("Sync session factory not initialized")
        
        session = self._sync_session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session with proper error handling and cleanup"""
        if not self._async_session_factory:
            raise RuntimeError("Async session factory not initialized")
        
        session = self._async_session_factory()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Async database session error: {e}")
            raise
        finally:
            await session.close()
    
    @contextmanager
    def transaction(self) -> Generator[Session, None, None]:
        """Execute operations in a transaction with automatic rollback on error"""
        with self.get_session() as session:
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Transaction failed: {e}")
                raise
    
    @asynccontextmanager
    async def async_transaction(self) -> AsyncGenerator[AsyncSession, None]:
        """Execute async operations in a transaction with automatic rollback on error"""
        async with self.get_async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Async transaction failed: {e}")
                raise
    
    def execute_with_retry(self, operation: Callable, *args, **kwargs) -> Any:
        """Execute database operation with retry logic"""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                return operation(*args, **kwargs)
            except (DisconnectionError, TimeoutError, ConnectionError) as e:
                last_exception = e
                if attempt < self.config.max_retries:
                    wait_time = self.config.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Database operation failed (attempt {attempt + 1}), retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Database operation failed after {self.config.max_retries} retries: {e}")
                    break
            except Exception as e:
                # Don't retry for non-connection errors
                logger.error(f"Database operation failed (non-retryable): {e}")
                raise
        
        if last_exception:
            raise last_exception
    
    def get_connection_pool_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        if self._sync_engine and hasattr(self._sync_engine.pool, 'size'):
            pool = self._sync_engine.pool
            return {
                "pool_size": pool.size(),
                "checked_in_connections": pool.checkedin(),
                "checked_out_connections": pool.checkedout(),
                "overflow_connections": pool.overflow(),
                "invalid_connections": pool.invalid(),
                "total_connections": pool.size() + pool.overflow(),
                **self._connection_pool_stats
            }
        return self._connection_pool_stats
    
    def health_check(self) -> bool:
        """Perform database health check"""
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def close_all_connections(self):
        """Close all database connections"""
        if self._sync_engine:
            self._sync_engine.dispose()
        if self._async_engine:
            # Note: For async engines, this should be awaited in an async context
            pass


# Global database manager instance
config = DatabaseConfig()
db_manager = DatabaseManager(config)


# FastAPI dependency functions
def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency to get a database session"""
    with db_manager.get_session() as session:
        yield session


def get_db_transaction() -> Generator[Session, None, None]:
    """FastAPI dependency to get a database session within a transaction"""
    with db_manager.transaction() as session:
        yield session


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get an async database session"""
    async with db_manager.get_async_session() as session:
        yield session


async def get_async_db_transaction() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get an async database session within a transaction"""
    async with db_manager.async_transaction() as session:
        yield session


# Decorators for automatic session management
def with_db_session(func):
    """Decorator to automatically inject database session"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'db' not in kwargs:
            with db_manager.get_session() as session:
                kwargs['db'] = session
                return func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


def with_db_transaction(func):
    """Decorator to automatically wrap function in a database transaction"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with db_manager.transaction() as session:
            kwargs['db'] = session
            return func(*args, **kwargs)
    return wrapper


def with_retry(max_retries: int = None):
    """Decorator to add retry logic to database operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = max_retries or config.max_retries
            return db_manager.execute_with_retry(func, *args, **kwargs)
        return wrapper
    return decorator


# Exception handling utilities
class DatabaseException(Exception):
    """Base class for database-related exceptions"""
    pass


class ConnectionPoolExhaustedException(DatabaseException):
    """Raised when database connection pool is exhausted"""
    pass


class TransactionTimeoutException(DatabaseException):
    """Raised when database transaction times out"""
    pass


def handle_db_exceptions(func):
    """Decorator to handle common database exceptions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutError as e:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Database operation timed out"
            )
        except DisconnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection lost"
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error in {func.__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
    return wrapper


# Migration and maintenance utilities
def run_database_maintenance():
    """Run database maintenance tasks"""
    logger.info("Running database maintenance...")
    
    # Update connection pool statistics
    stats = db_manager.get_connection_pool_stats()
    logger.info(f"Connection pool stats: {stats}")
    
    # Check for long-running transactions (would need custom implementation)
    # Close idle connections if needed
    # Run VACUUM or ANALYZE if supported
    
    logger.info("Database maintenance completed")


# Health check endpoint function
def get_database_health() -> Dict[str, Any]:
    """Get comprehensive database health information"""
    try:
        health_status = db_manager.health_check()
        pool_stats = db_manager.get_connection_pool_stats()
        
        return {
            "healthy": health_status,
            "connection_pool": pool_stats,
            "database_url": config.database_url.split('@')[-1] if '@' in config.database_url else "configured",
            "pool_settings": {
                "pool_size": config.pool_size,
                "max_overflow": config.max_overflow,
                "pool_timeout": config.pool_timeout,
                "pool_recycle": config.pool_recycle
            }
        }
    except Exception as e:
        return {
            "healthy": False,
            "error": str(e),
            "database_url": "error"
        }