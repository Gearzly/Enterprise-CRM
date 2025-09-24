#!/usr/bin/env python3
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test the exact import sequence as in opportunities.py
try:
    print("Testing exact import sequence from opportunities.py...")
    
    # This is the exact import from opportunities.py
    from app.core.crud import opportunity as crud_opportunity
    
    print(f"Import type: {type(crud_opportunity)}")
    print(f"Has get_multi: {hasattr(crud_opportunity, 'get_multi')}")
    
    if hasattr(crud_opportunity, 'get_multi'):
        print("SUCCESS: get_multi method is accessible!")
        # Try to actually call the method
        print("Method signature:", crud_opportunity.get_multi)
    else:
        print("ERROR: get_multi method is NOT accessible!")
        
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()