#!/usr/bin/env python3
import sys
import os
sys.path.append('d:/CRM/backend')

def deep_router_debug():
    print('🔍 DEEP ROUTER REGISTRATION DEBUGGING')
    print('=' * 60)
    
    try:
        # Test 1: Compare working vs non-working router imports
        print('\n📊 STEP 1: Router Import Comparison')
        print('-' * 40)
        
        print('Testing WORKING endpoint: /marketing/ (✅ Returns 200)')
        from app.marketing import router as marketing_main_router
        print('✅ Marketing main router imported successfully')
        
        print(f'   Main router routes: {[r.path for r in marketing_main_router.routes if hasattr(r, "path")][:3]}')
        
        print('\nTesting NON-WORKING endpoint: /marketing/automation/ (❌ Returns 404)')
        from app.marketing.automation.automation import router as automation_router
        print('✅ Automation router imported successfully')
        
        print(f'   Automation router routes: {[r.path for r in automation_router.routes if hasattr(r, "path")][:3]}')
        
        # Test 2: Check if automation router is actually included in marketing router
        print('\n📊 STEP 2: Router Inclusion Analysis')
        print('-' * 40)
        
        # Get all sub-routers included in main marketing router
        included_routers = []
        for route in marketing_main_router.routes:
            if hasattr(route, 'path') and hasattr(route, 'route'):
                included_routers.append({
                    'path': route.path,
                    'router': str(type(route.route))
                })
        
        print('Marketing main router includes these sub-routers:')
        for router_info in included_routers:
            print(f'   {router_info["path"]} -> {router_info["router"]}')
        
        # Check if automation is included
        automation_included = any('/automation' in router_info['path'] for router_info in included_routers)
        print(f'\n✅ Automation router included in main marketing router: {automation_included}')
        
        # Test 3: Check main app router registration
        print('\n📊 STEP 3: Main App Router Registration')
        print('-' * 40)
        
        from app.main import app
        print('✅ Main app imported successfully')
        
        # Get all routes registered in main app
        main_app_routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                main_app_routes.append({
                    'path': route.path,
                    'methods': getattr(route, 'methods', ['Unknown'])
                })
        
        print('Main app registered routes:')
        for route_info in main_app_routes:
            print(f'   {route_info["path"]} -> {route_info["methods"]}')
        
        # Check marketing registration
        marketing_registered = any('/marketing' in route_info['path'] for route_info in main_app_routes)
        print(f'\n✅ Marketing router registered in main app: {marketing_registered}')
        
        # Test 4: Direct router endpoint testing
        print('\n📊 STEP 4: Direct Router Function Testing')
        print('-' * 40)
        
        # Test automation root endpoint directly
        try:
            from app.marketing.automation.automation import get_automation_dashboard
            result = get_automation_dashboard()
            print(f'✅ Automation dashboard function works: {result.get("message", "No message")}')
        except Exception as e:
            print(f'❌ Automation dashboard function error: {e}')
        
        # Test marketing main dashboard
        try:
            from app.marketing import get_marketing_dashboard
            result = get_marketing_dashboard()
            print(f'✅ Marketing main dashboard function works: {result.get("message", "No message")}')
        except Exception as e:
            print(f'❌ Marketing main dashboard function error: {e}')
        
        # Test 5: FastAPI route resolution
        print('\n📊 STEP 5: FastAPI Route Resolution Testing')
        print('-' * 40)
        
        # Create a test client to debug route resolution
        from fastapi.testclient import TestClient
        
        print('Creating test client...')
        client = TestClient(app)
        
        # Test working endpoint
        print('Testing /marketing/ (working):')
        response = client.get('/marketing/')
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            print(f'   Response: {response.json()}')
        
        # Test non-working endpoint
        print('Testing /marketing/automation/ (non-working):')
        response = client.get('/marketing/automation/')
        print(f'   Status: {response.status_code}')
        if response.status_code != 200:
            print(f'   Error: {response.text}')
        
        # Test 6: OpenAPI schema analysis
        print('\n📊 STEP 6: OpenAPI Schema Analysis')
        print('-' * 40)
        
        openapi_schema = app.openapi()
        paths = openapi_schema.get('paths', {})
        
        print('Registered paths in OpenAPI schema:')
        marketing_paths = [path for path in paths.keys() if '/marketing' in path]
        for path in sorted(marketing_paths):
            print(f'   {path}')
        
        automation_in_schema = any('/automation' in path for path in marketing_paths)
        print(f'\n✅ Automation endpoints in OpenAPI schema: {automation_in_schema}')
        
        return True
        
    except Exception as e:
        print(f'❌ Debug error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    deep_router_debug()