"""
Startup optimizations for the CRM Backend system.
Handles database initialization, connection verification, and performance tuning.
"""
import logging
import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from .core.database import engine, SessionLocal
from .models import sales, marketing, support

logger = logging.getLogger(__name__)


async def optimize_database_connections():
    """Optimize database connections and warm up the connection pool"""
    try:
        logger.info("Optimizing database connections...")
        
        # Test database connection
        with SessionLocal() as db:
            # Execute a simple query to warm up the connection
            db.execute(text("SELECT 1"))
            db.commit()
        
        logger.info("Database connection optimization completed")
        
    except Exception as e:
        logger.error(f"Database optimization failed: {e}")
        raise


async def initialize_application_state():
    """Initialize application state and cache"""
    try:
        logger.info("Initializing application state...")
        
        # Pre-load any necessary data or configuration
        # This can include cache warming, configuration validation, etc.
        
        logger.info("Application state initialization completed")
        
    except Exception as e:
        logger.error(f"Application state initialization failed: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with optimizations"""
    
    # Startup
    logger.info("🚀 Starting CRM Backend with optimizations...")
    start_time = time.time()
    
    try:
        # Run startup optimizations
        await optimize_database_connections()
        await initialize_application_state()
        
        startup_time = time.time() - start_time
        logger.info(f"✅ CRM Backend startup completed in {startup_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"❌ Startup optimization failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down CRM Backend...")
    
    try:
        # Clean shutdown procedures
        if hasattr(engine, 'dispose'):
            engine.dispose()
        logger.info("✅ CRM Backend shutdown completed")
        
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# Import comprehensive logging configuration
from .core.logging_config import configure_logging

# Initialize comprehensive logging when module is imported
configure_logging()