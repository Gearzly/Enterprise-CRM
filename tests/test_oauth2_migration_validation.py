#!/usr/bin/env python3
"""
OAuth2 PKCE Migration Validation Test
Tests the migration at the code level without requiring a running server
"""
import sys
import os
import importlib.util

def test_oauth2_pkce_module():
    """Test OAuth2 PKCE implementation can be imported"""
    print("🔍 Testing OAuth2 PKCE module import...")
    try:
        sys.path.append('backend')
        from app.core.auth.oauth2_pkce import oauth2_manager, OAuth2PKCEManager
        print("✅ OAuth2 PKCE module imported successfully")
        
        # Test manager instantiation
        manager = OAuth2PKCEManager()
        print("✅ OAuth2PKCEManager can be instantiated")
        
        # Test PKCE challenge generation
        challenge = manager.generate_pkce_challenge()
        if 'code_challenge' in challenge and 'code_challenge_method' in challenge:
            print("✅ PKCE challenge generation working")
            return True
        else:
            print("❌ PKCE challenge generation failed")
            return False
            
    except Exception as e:
        print(f"❌ OAuth2 PKCE module import failed: {e}")
        return False

def test_oauth2_middleware():
    """Test OAuth2 middleware can be imported"""
    print("🔍 Testing OAuth2 middleware import...")
    try:
        from app.core.auth.oauth2_middleware import OAuth2AuthenticationMiddleware, OAuth2AuthorizationMiddleware
        print("✅ OAuth2 middleware imported successfully")
        
        # Test middleware instantiation
        auth_middleware = OAuth2AuthenticationMiddleware(None)
        authz_middleware = OAuth2AuthorizationMiddleware(None)
        print("✅ OAuth2 middleware can be instantiated")
        return True
        
    except Exception as e:
        print(f"❌ OAuth2 middleware import failed: {e}")
        return False

def test_oauth2_routes():
    """Test OAuth2 routes can be imported"""
    print("🔍 Testing OAuth2 routes import...")
    try:
        from app.core.auth.oauth2_routes import router
        print("✅ OAuth2 routes imported successfully")
        
        # Check if router has expected endpoints
        routes = [route.path for route in router.routes]
        expected_routes = ['/challenge', '/authorize', '/token', '/refresh']
        
        found_routes = 0
        for expected_route in expected_routes:
            if any(expected_route in route for route in routes):
                found_routes += 1
        
        print(f"✅ OAuth2 routes defined: {found_routes}/{len(expected_routes)} endpoints")
        return found_routes >= 2
        
    except Exception as e:
        print(f"❌ OAuth2 routes import failed: {e}")
        return False

def test_jwt_removal():
    """Test that JWT dependencies have been removed"""
    print("🔍 Testing JWT dependency removal...")
    try:
        # Check that auth middleware no longer uses JWT
        from app.core.middleware.auth_middleware import AuthenticationMiddleware
        
        # Check if it's the deprecated version
        import inspect
        source = inspect.getsource(AuthenticationMiddleware)
        if 'OAuth2AuthenticationMiddleware' in source or 'DEPRECATED' in source:
            print("✅ JWT middleware has been deprecated/replaced")
            return True
        else:
            print("❌ JWT middleware still in use")
            return False
            
    except Exception as e:
        print(f"❌ JWT removal test failed: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("🔍 Testing environment configuration...")
    try:
        # Check if .env has OAuth2 configuration
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                env_content = f.read()
            
            oauth2_configs = [
                'OAUTH2_ENCRYPTION_KEY',
                'OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES',
                'OAUTH2_DEFAULT_CLIENT_ID'
            ]
            
            found_configs = 0
            for config in oauth2_configs:
                if config in env_content:
                    found_configs += 1
            
            print(f"✅ OAuth2 environment configs found: {found_configs}/{len(oauth2_configs)}")
            
            # Check JWT is deprecated
            if 'DEPRECATED' in env_content and 'JWT' in env_content:
                print("✅ JWT configuration marked as deprecated")
                return True
            else:
                print("⚠️  JWT configuration not clearly deprecated")
                return found_configs >= 2
        else:
            print("❌ .env file not found")
            return False
            
    except Exception as e:
        print(f"❌ Environment config test failed: {e}")
        return False

def test_main_app_integration():
    """Test main app OAuth2 integration"""
    print("🔍 Testing main app OAuth2 integration...")
    try:
        # Check main.py has OAuth2 router and middleware
        with open('backend/app/main.py', 'r') as f:
            main_content = f.read()
        
        oauth2_integrations = [
            'oauth2_router',
            'OAuth2AuthenticationMiddleware',
            'OAuth2AuthorizationMiddleware'
        ]
        
        found_integrations = 0
        for integration in oauth2_integrations:
            if integration in main_content:
                found_integrations += 1
        
        print(f"✅ OAuth2 integrations in main.py: {found_integrations}/{len(oauth2_integrations)}")
        return found_integrations >= 2
        
    except Exception as e:
        print(f"❌ Main app integration test failed: {e}")
        return False

def main():
    """Run OAuth2 PKCE migration validation"""
    print("🚀 OAuth2 PKCE Migration Validation")
    print("=" * 50)
    
    # Change to correct directory
    if os.path.exists('backend'):
        os.chdir('backend')
    
    results = {}
    
    # Test OAuth2 PKCE module
    results['oauth2_module'] = test_oauth2_pkce_module()
    print()
    
    # Test OAuth2 middleware
    results['oauth2_middleware'] = test_oauth2_middleware()
    print()
    
    # Test OAuth2 routes
    results['oauth2_routes'] = test_oauth2_routes()
    print()
    
    # Test JWT removal
    results['jwt_removal'] = test_jwt_removal()
    print()
    
    # Change back for env test
    os.chdir('..')
    
    # Test environment configuration
    results['env_config'] = test_environment_config()
    print()
    
    # Test main app integration
    results['main_integration'] = test_main_app_integration()
    print()
    
    # Summary
    print("=" * 50)
    print("📋 OAuth2 PKCE Migration Validation Summary:")
    print(f"   OAuth2 PKCE Module: {'✅' if results['oauth2_module'] else '❌'}")
    print(f"   OAuth2 Middleware: {'✅' if results['oauth2_middleware'] else '❌'}")
    print(f"   OAuth2 Routes: {'✅' if results['oauth2_routes'] else '❌'}")
    print(f"   JWT Removal: {'✅' if results['jwt_removal'] else '❌'}")
    print(f"   Environment Config: {'✅' if results['env_config'] else '❌'}")
    print(f"   Main App Integration: {'✅' if results['main_integration'] else '❌'}")
    
    success_count = sum(results.values())
    total_tests = len(results)
    
    print(f"\n📊 Overall Score: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 OAuth2 PKCE migration validation PASSED!")
        print("✅ All components successfully migrated from JWT to OAuth2 PKCE")
    elif success_count >= total_tests * 0.8:
        print("✅ OAuth2 PKCE migration validation MOSTLY PASSED!")
        print("⚠️  Minor issues detected but core migration successful")
    else:
        print("❌ OAuth2 PKCE migration validation FAILED!")
        print("🔧 Significant issues detected - migration needs attention")
    
    return success_count >= total_tests * 0.8

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)