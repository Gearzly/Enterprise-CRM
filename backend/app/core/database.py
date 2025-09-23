from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os

# Database URL - using SQLite for development, can be changed to PostgreSQL or MySQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm_sales.db")

# Create the SQLAlchemy engine with enhanced connection pooling
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    # Connection pooling settings
    poolclass=QueuePool,
    pool_size=20,              # Number of connections to maintain in the pool
    max_overflow=30,           # Number of connections to allow beyond pool_size
    pool_pre_ping=True,        # Validate connections before use
    pool_recycle=300,          # Recycle connections after 5 minutes
    pool_timeout=30,           # Seconds to wait before giving up on getting a connection
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

def get_db():
    """Dependency to get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()