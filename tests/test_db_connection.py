import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get the database URL from environment variables
# No default to SQLite anymore
DATABASE_URL: str = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure it in your .env file.")

print(f"Database URL: {DATABASE_URL}")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.fetchone()
        print(f"Database connection successful!")
        if version:
            print(f"Database version: {version[0]}")
        else:
            print("Connected to database, but could not retrieve version.")
        
except Exception as e:
    print(f"Database connection failed: {e}")