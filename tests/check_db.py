import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    print("Error: DATABASE_URL environment variable is not set.")
    sys.exit(1)

# Connect to the database using SQLAlchemy
try:
    from sqlalchemy import create_engine, text
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
except Exception as e:
    print(f"Error connecting to database: {e}")
    sys.exit(1)

# Get all tables
try:
    result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
    tables = result.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(f"  - {table[0]}")
except Exception as e:
    print(f"Error retrieving tables: {e}")
    connection.close()
    sys.exit(1)

# Check if contacts table exists and get its columns
try:
    result = connection.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'contacts'"))
    columns = result.fetchall()
    if columns:
        print("\nContacts table columns:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
    else:
        print("\nContacts table not found.")
except Exception as e:
    print(f"Error retrieving contacts table columns: {e}")

connection.close()