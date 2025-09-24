#!/usr/bin/env python3
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test the import
try:
    from app.core.crud import opportunity as crud_opportunity
    print("Import successful")
    print(f"Type of crud_opportunity: {type(crud_opportunity)}")
    print(f"Has get_multi: {hasattr(crud_opportunity, 'get_multi')}")
    print(f"Dir of crud_opportunity: {dir(crud_opportunity)}")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()