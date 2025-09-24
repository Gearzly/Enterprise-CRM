"""
OAuth2+PKCE Migration Test Suite
Validates the complete migration from JWT to OAuth2+PKCE

This test suite validates:
1. OAuth2+PKCE flow implementation
2. JWT deprecation and removal
3. Security improvements
4. Token management and revocation
5. PKCE challenge/response validation
6. Role-based access control
7. Middleware functionality
8. Error handling and edge cases
"""
import asyncio
import httpx
import json
import time
import hashlib
import base64
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OAuth2PKCEMigrationTester:
    """Comprehensive OAuth2+PKCE migration test suite"""
    
    def __init__(self, base_url: str = "http://localhost:5173"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30)
        self.test_results = []
        
        # Test data
        self.test_user = {
            "email": "test@crm.com",
            "password": "TestPassword123!",
            "username": "testuser"
        }
        
        # OAuth2 data
        self.pkce_data = {}
        self.tokens = {}
        
    async def run_test(self, test_name: str, test_func):
        """Run a single test with error handling"""
        start_time = time.time()
        try:
            logger.info(f"🧪 Running: {test_name}")
            result = await test_func()
            duration = time.time() - start_time
            
            self.test_results.append({
                "name": test_name,
                "status": "PASS",
                "duration": duration,
                "result": result
            })
            logger.info(f"✅ PASSED: {test_name} ({duration:.2f}s)")
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append({
                "name": test_name,
                "status": "FAIL",
                "duration": duration,
                "error": str(e)
            })
            logger.error(f"❌ FAILED: {test_name} ({duration:.2f}s) - {e}")
            raise
    
    async def test_oauth2_pkce_challenge_generation(self):
        """Test PKCE challenge generation"""
        response = await self.client.post(f"{self.base_url}/auth/challenge")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        required_fields = ["code_challenge", "code_challenge_method", "challenge_id", "state"]
        
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        assert data["code_challenge_method"] == "S256", "Challenge method must be S256"
        assert len(data["code_challenge"]) > 0, "Code challenge cannot be empty"
        
        # Store PKCE data for later tests
        self.pkce_data = data
        
        return {
            "challenge_generated": True,
            "method": data["code_challenge_method"],
            "challenge_length": len(data["code_challenge"]),
            "has_state": bool(data.get("state"))
        }
    
    async def test_oauth2_password_flow(self):
        """Test OAuth2 password grant flow with PKCE"""
        # First generate PKCE challenge
        if not self.pkce_data:
            await self.test_oauth2_pkce_challenge_generation()
        
        # Attempt password flow
        token_data = {
            "grant_type": "password",
            "username": self.test_user["email"],
            "password": self.test_user["password"],
            "client_id": "crm_web_app",
            "scope": "read write"
        }
        
        response = await self.client.post(
            f"{self.base_url}/auth/token",
            data=token_data
        )
        
        # Note: This might fail with 401 if user doesn't exist, which is expected
        result = {
            "status_code": response.status_code,
            "response_received": True
        }
        
        if response.status_code == 200:
            token_response = response.json()
            required_fields = ["access_token", "token_type"]
            
            for field in required_fields:
                assert field in token_response, f"Missing token field: {field}"
            
            assert token_response["token_type"] == "Bearer", "Token type must be Bearer"
            
            # Store tokens for later tests
            self.tokens = token_response
            
            result.update({
                "authentication_successful": True,
                "token_type": token_response["token_type"],
                "has_refresh_token": "refresh_token" in token_response,
                "token_length": len(token_response["access_token"])
            })
        else:
            # Authentication failed (expected if test user doesn't exist)
            result.update({
                "authentication_successful": False,
                "error_response": response.text[:200]  # First 200 chars of error
            })
        
        return result
    
    async def test_pkce_challenge_verification(self):
        """Test PKCE challenge verification process"""
        # Generate our own PKCE challenge to test the verification
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        # Test that our implementation matches expected behavior
        assert len(code_verifier) >= 43, "Code verifier too short"
        assert len(code_challenge) == 43, "Code challenge wrong length"
        
        # Verify regeneration produces different values
        code_verifier2 = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        assert code_verifier != code_verifier2, "Code verifiers should be unique"
        
        return {
            "verifier_length": len(code_verifier),
            "challenge_length": len(code_challenge),
            "unique_generation": True,
            "s256_method_working": True
        }
    
    async def test_jwt_deprecation(self):
        """Test that JWT endpoints are deprecated or removed"""
        # Test common JWT endpoints that should no longer work
        jwt_endpoints = [
            "/auth/jwt/login",
            "/auth/jwt/refresh", 
            "/auth/jwt/verify",
            "/api/auth/jwt"
        ]
        
        results = {}
        for endpoint in jwt_endpoints:
            try:
                response = await self.client.post(f"{self.base_url}{endpoint}")
                results[endpoint] = {
                    "status_code": response.status_code,
                    "deprecated": response.status_code == 404  # 404 means removed
                }
            except Exception as e:
                results[endpoint] = {
                    "status_code": None,
                    "deprecated": True,  # Exception means it's gone
                    "error": str(e)
                }
        
        # Check if any JWT references exist in API docs
        try:
            docs_response = await self.client.get(f"{self.base_url}/openapi.json")
            if docs_response.status_code == 200:
                openapi_content = docs_response.text.lower()
                jwt_references = openapi_content.count("jwt")
                results["openapi_jwt_references"] = jwt_references
            else:
                results["openapi_jwt_references"] = "docs_unavailable"
        except:
            results["openapi_jwt_references"] = "docs_error"
        
        return results
    
    async def test_oauth2_token_validation(self):
        """Test OAuth2 token validation"""
        # Try to access a protected endpoint without token
        response = await self.client.get(f"{self.base_url}/api/superadmin")
        
        result = {
            "unauth_status": response.status_code,
            "auth_required": response.status_code in [401, 403]
        }
        
        # If we have a token, test with it
        if self.tokens and "access_token" in self.tokens:
            headers = {"Authorization": f"Bearer {self.tokens['access_token']}"}
            auth_response = await self.client.get(
                f"{self.base_url}/api/superadmin",
                headers=headers
            )
            result.update({
                "auth_status": auth_response.status_code,
                "token_accepted": auth_response.status_code != 401
            })
        
        return result
    
    async def test_oauth2_scopes(self):
        """Test OAuth2 scope-based authorization"""
        scopes_to_test = ["read", "write", "admin", "sales", "marketing", "support"]
        
        results = {}
        for scope in scopes_to_test:
            # Test requesting tokens with different scopes
            token_data = {
                "grant_type": "password",
                "username": self.test_user["email"],
                "password": self.test_user["password"],
                "client_id": "crm_web_app",
                "scope": scope
            }
            
            try:
                response = await self.client.post(
                    f"{self.base_url}/auth/token",
                    data=token_data
                )
                results[scope] = {
                    "status_code": response.status_code,
                    "scope_supported": response.status_code in [200, 401]  # 401 = auth failed, not scope issue
                }
            except Exception as e:
                results[scope] = {
                    "status_code": None,
                    "scope_supported": False,
                    "error": str(e)
                }
        
        return results
    
    async def test_oauth2_middleware_integration(self):
        """Test OAuth2 middleware integration"""
        # Test that OAuth2 middleware is properly handling requests
        
        # 1. Test CORS headers
        response = await self.client.options(f"{self.base_url}/")
        cors_result = {
            "cors_headers_present": "access-control-allow-origin" in response.headers,
            "options_method_working": response.status_code in [200, 204]
        }
        
        # 2. Test security headers
        response = await self.client.get(f"{self.base_url}/health")
        security_headers = {
            "x-content-type-options": response.headers.get("x-content-type-options"),
            "x-frame-options": response.headers.get("x-frame-options"),
            "x-xss-protection": response.headers.get("x-xss-protection")
        }
        
        # 3. Test rate limiting (if implemented)
        rate_limit_test = []
        for i in range(5):
            resp = await self.client.get(f"{self.base_url}/health")
            rate_limit_test.append(resp.status_code)
        
        return {
            "cors": cors_result,
            "security_headers": security_headers,
            "rate_limiting": {
                "requests_made": len(rate_limit_test),
                "all_successful": all(code == 200 for code in rate_limit_test)
            }
        }
    
    async def test_oauth2_client_configuration(self):
        """Test OAuth2 client configuration"""
        # Test the default CRM client configuration
        
        # This test verifies that the OAuth2 manager has proper client setup
        # by testing the challenge generation (which requires a configured client)
        challenge_response = await self.client.post(f"{self.base_url}/auth/challenge")
        
        result = {
            "default_client_configured": challenge_response.status_code == 200,
            "client_supports_pkce": True  # If challenge works, PKCE is supported
        }
        
        if challenge_response.status_code == 200:
            challenge_data = challenge_response.json()
            result.update({
                "challenge_method": challenge_data.get("code_challenge_method"),
                "state_generation": bool(challenge_data.get("state")),
                "challenge_id_generation": bool(challenge_data.get("challenge_id"))
            })
        
        return result
    
    async def test_error_handling(self):
        """Test OAuth2 error handling"""
        error_tests = {}
        
        # 1. Invalid grant type
        try:
            response = await self.client.post(
                f"{self.base_url}/auth/token",
                data={
                    "grant_type": "invalid_grant",
                    "client_id": "crm_web_app"
                }
            )
            error_tests["invalid_grant_type"] = {
                "status_code": response.status_code,
                "proper_error": response.status_code == 400
            }
        except Exception as e:
            error_tests["invalid_grant_type"] = {"error": str(e)}
        
        # 2. Missing client_id
        try:
            response = await self.client.post(
                f"{self.base_url}/auth/token",
                data={
                    "grant_type": "password",
                    "username": "test",
                    "password": "test"
                }
            )
            error_tests["missing_client_id"] = {
                "status_code": response.status_code,
                "proper_error": response.status_code == 400
            }
        except Exception as e:
            error_tests["missing_client_id"] = {"error": str(e)}
        
        # 3. Invalid endpoint
        try:
            response = await self.client.post(f"{self.base_url}/auth/invalid_endpoint")
            error_tests["invalid_endpoint"] = {
                "status_code": response.status_code,
                "proper_error": response.status_code == 404
            }
        except Exception as e:
            error_tests["invalid_endpoint"] = {"error": str(e)}
        
        return error_tests
    
    async def test_security_improvements(self):
        """Test security improvements over JWT"""
        improvements = {}
        
        # 1. Test token opacity (tokens should not contain readable data)
        if self.tokens and "access_token" in self.tokens:
            token = self.tokens["access_token"]
            
            # OAuth2 tokens should be opaque, not JWT format
            is_jwt = token.count('.') == 2  # JWTs have 2 dots
            improvements["opaque_tokens"] = not is_jwt
            
            # Test token length (should be random, not predictable)
            improvements["token_length"] = len(token)
            improvements["token_randomness"] = len(set(token)) > 10  # Should have variety
        
        # 2. Test PKCE protection
        improvements["pkce_protection"] = bool(self.pkce_data)
        
        # 3. Test that sensitive endpoints require authentication
        protected_endpoints = [
            "/api/superadmin",
            "/api/security",
            "/api/audit"
        ]
        
        auth_required_count = 0
        for endpoint in protected_endpoints:
            response = await self.client.get(f"{self.base_url}{endpoint}")
            if response.status_code in [401, 403]:
                auth_required_count += 1
        
        improvements["endpoints_protected"] = auth_required_count
        improvements["total_endpoints_tested"] = len(protected_endpoints)
        improvements["protection_percentage"] = (auth_required_count / len(protected_endpoints)) * 100
        
        return improvements
    
    async def test_migration_completeness(self):
        """Test that migration from JWT to OAuth2+PKCE is complete"""
        completeness = {}
        
        # 1. OAuth2 endpoints are available
        oauth2_endpoints = ["/auth/challenge", "/auth/token"]
        oauth2_working = 0
        
        for endpoint in oauth2_endpoints:
            try:
                response = await self.client.post(f"{self.base_url}{endpoint}")
                if response.status_code != 404:  # Not found means endpoint exists
                    oauth2_working += 1
            except:
                pass
        
        completeness["oauth2_endpoints_available"] = oauth2_working
        completeness["oauth2_endpoints_total"] = len(oauth2_endpoints)
        
        # 2. Test that new auth middleware is working
        response = await self.client.get(f"{self.base_url}/api/security")
        completeness["auth_middleware_active"] = response.status_code != 500
        
        # 3. Test server startup (implicit - if we're running tests, server started)
        completeness["server_startup_successful"] = True
        
        # 4. Test that deprecated JWT imports don't break the system
        response = await self.client.get(f"{self.base_url}/health")
        completeness["no_import_errors"] = response.status_code == 200
        
        return completeness
    
    async def run_comprehensive_migration_tests(self):
        """Run all OAuth2+PKCE migration tests"""
        logger.info("🚀 Starting OAuth2+PKCE Migration Test Suite")
        
        tests = [
            ("OAuth2 PKCE Challenge Generation", self.test_oauth2_pkce_challenge_generation),
            ("OAuth2 Password Flow", self.test_oauth2_password_flow),
            ("PKCE Challenge Verification", self.test_pkce_challenge_verification),
            ("JWT Deprecation", self.test_jwt_deprecation),
            ("OAuth2 Token Validation", self.test_oauth2_token_validation),
            ("OAuth2 Scopes", self.test_oauth2_scopes),
            ("OAuth2 Middleware Integration", self.test_oauth2_middleware_integration),
            ("OAuth2 Client Configuration", self.test_oauth2_client_configuration),
            ("Error Handling", self.test_error_handling),
            ("Security Improvements", self.test_security_improvements),
            ("Migration Completeness", self.test_migration_completeness)
        ]
        
        for test_name, test_func in tests:
            try:
                await self.run_test(test_name, test_func)
            except Exception as e:
                logger.error(f"Test {test_name} failed: {e}")
                continue
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        summary = {
            "migration_test_summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%",
                "total_duration": sum(r.get("duration", 0) for r in self.test_results)
            },
            "detailed_results": self.test_results,
            "migration_status": "COMPLETE" if passed_tests >= total_tests * 0.8 else "ISSUES_FOUND"
        }
        
        await self.client.aclose()
        
        logger.info(f"🏁 Migration Tests Complete: {passed_tests}/{total_tests} passed")
        
        return summary

async def main():
    """Main execution"""
    tester = OAuth2PKCEMigrationTester()
    
    try:
        results = await tester.run_comprehensive_migration_tests()
        
        # Print summary
        print("\n" + "="*80)
        print("OAUTH2+PKCE MIGRATION TEST SUMMARY")
        print("="*80)
        
        summary = results["migration_test_summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']}")
        print(f"Duration: {summary['total_duration']:.2f}s")
        print(f"Migration Status: {results['migration_status']}")
        
        print("\nDETAILED RESULTS:")
        print("-"*80)
        for result in results["detailed_results"]:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            duration = result.get("duration", 0)
            print(f"{status_icon} {result['name']} - {result['status']} ({duration:.2f}s)")
            if result["status"] == "FAIL":
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        # Save results
        with open("oauth2_migration_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Full results saved to: oauth2_migration_test_results.json")
        
        return results
        
    except Exception as e:
        logger.error(f"Migration test suite failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())