#!/usr/bin/env python3
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test the opportunity CRUD import specifically
try:
    print("Importing opportunity CRUD module...")
    import app.core.crud.opportunity as opportunity_module
    print(f"Module type: {type(opportunity_module)}")
    print(f"Module dir: {dir(opportunity_module)}")
    
    print("\nChecking if 'opportunity' instance exists...")
    if hasattr(opportunity_module, 'opportunity'):
        print("Found 'opportunity' instance")
        opportunity_instance = opportunity_module.opportunity
        print(f"Instance type: {type(opportunity_instance)}")
        print(f"Instance dir: {dir(opportunity_instance)}")
        print(f"Has get_multi: {hasattr(opportunity_instance, 'get_multi')}")
    else:
        print("ERROR: 'opportunity' instance not found in module")
        
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()