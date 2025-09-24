#!/usr/bin/env python3
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test the opportunity CRUD import through the package system
try:
    print("Importing opportunity through package system...")
    from app.core.crud import opportunity
    print(f"Import type: {type(opportunity)}")
    print(f"Import dir: {dir(opportunity)}")
    print(f"Has get_multi: {hasattr(opportunity, 'get_multi')}")
    
    if hasattr(opportunity, 'get_multi'):
        print("SUCCESS: get_multi method is accessible!")
    else:
        print("ERROR: get_multi method is NOT accessible!")
        
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()