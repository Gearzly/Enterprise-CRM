from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL - using environment variable for production
# For development, set DATABASE_URL in .env file
# Example for PostgreSQL: postgresql://user:password@localhost:5432/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# If no DATABASE_URL is set, use SQLite as fallback for testing
if DATABASE_URL is None:
    print("Warning: DATABASE_URL not set, using SQLite fallback for testing")
    DATABASE_URL = "sqlite:///./crm_test.db"

# Create the SQLAlchemy engine with enhanced connection pooling
# Optimize pool settings for better performance
if "sqlite" in DATABASE_URL:
    # SQLite configuration with optimizations
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30,  # 30 second timeout for SQLite operations
            "isolation_level": None  # Use autocommit mode for better performance
        },
        pool_pre_ping=True,
        pool_recycle=7200,  # 2 hours
        echo=False  # Disable SQL logging for performance
    )
else:
    # PostgreSQL configuration with optimized pooling
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=8,               # Optimized pool size
        max_overflow=12,           # Optimized overflow
        pool_pre_ping=True,        # Validate connections before use
        pool_recycle=7200,         # 2 hours (increased from 1 hour)
        pool_timeout=15,           # 15 second timeout for getting connection
        connect_args={
            "connect_timeout": 15,  # 15 second connection timeout
            "application_name": "CRM_Backend",
            "keepalives_idle": "600",
            "keepalives_interval": "30",
            "keepalives_count": "3"
        },
        echo=False  # Disable SQL logging for performance
    )

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Import all models to ensure they are registered with the Base metadata
# This must be done after Base is defined to avoid circular imports
from app.models import sales, marketing, support

def get_db():
    """Dependency to get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()