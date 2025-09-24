#!/usr/bin/env python3
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test the import sequence as it happens in the application
try:
    print("Importing FastAPI...")
    from fastapi import FastAPI
    
    print("Importing sales router...")
    from app.sales import router as sales_router
    
    print("Creating app...")
    app = FastAPI()
    
    print("Including router...")
    app.include_router(sales_router, prefix="/sales", tags=["Sales"])
    
    print("Testing opportunity CRUD access...")
    from app.core.crud import opportunity as crud_opportunity
    print(f"Has get_multi: {hasattr(crud_opportunity, 'get_multi')}")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()