#!/usr/bin/env python3
"""
Database testing strategy for Sales modules
"""
import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

def setup_test_database():
    """Setup test database"""
    print("Setting up test database...")
    try:
        import importlib
        # Import the database module
        database_module = importlib.import_module('app.core.database')
        Base = getattr(database_module, 'Base')
        engine = getattr(database_module, 'engine')
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Test database setup complete")
        return True
    except Exception as e:
        print(f"Error setting up test database: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        import importlib
        # Import the database module
        database_module = importlib.import_module('app.core.database')
        SessionLocal = getattr(database_module, 'SessionLocal')
        
        # Create a test session
        db = SessionLocal()
        
        # Execute a simple query
        from sqlalchemy import text
        result = db.execute(text("SELECT 1"))
        row = result.fetchone()
        
        if row and row[0] == 1:
            print("[PASS] Database connection test passed")
            db.close()
            return True
        else:
            print("[FAIL] Database connection test failed")
            db.close()
            return False
    except Exception as e:
        print(f"[FAIL] Database connection test failed with error: {e}")
        return False
