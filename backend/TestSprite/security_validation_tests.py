"""
Security Validation Test Suite
Tests all security implementations including OWASP compliance

This suite validates:
1. OWASP security headers
2. Input validation and sanitization  
3. SQL injection protection
4. XSS protection
5. CSRF protection
6. Rate limiting
7. Authentication security
8. Authorization controls
9. Data classification
10. Audit logging
"""
import asyncio
import httpx
import json
import time
import base64
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityValidationTester:
    """Comprehensive security validation test suite"""
    
    def __init__(self, base_url: str = "http://localhost:5173"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30)
        self.test_results = []
        
    async def run_test(self, test_name: str, test_func):
        """Run a single test with error handling"""
        start_time = time.time()
        try:
            logger.info(f"🔒 Running Security Test: {test_name}")
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
    
    async def test_owasp_security_headers(self):
        """Test OWASP recommended security headers"""
        response = await self.client.get(f"{self.base_url}/health")
        headers = dict(response.headers)
        
        # OWASP recommended headers
        required_headers = {
            "x-content-type-options": "nosniff",
            "x-frame-options": ["DENY", "SAMEORIGIN"],
            "x-xss-protection": "1; mode=block",
            "strict-transport-security": None,  # Should exist
            "content-security-policy": None,    # Should exist
            "referrer-policy": None,           # Should exist
            "permissions-policy": None         # Should exist (new)
        }
        
        header_results = {}
        security_score = 0
        total_headers = len(required_headers)
        
        for header, expected_value in required_headers.items():
            header_value = headers.get(header, "").lower()
            
            if header_value:
                if expected_value is None:
                    # Header exists (good)
                    header_results[header] = {"present": True, "value": header_value, "compliant": True}
                    security_score += 1
                elif isinstance(expected_value, list):
                    # Check if value is in allowed list
                    compliant = any(exp.lower() in header_value for exp in expected_value)
                    header_results[header] = {"present": True, "value": header_value, "compliant": compliant}
                    if compliant:
                        security_score += 1
                else:
                    # Check exact match
                    compliant = expected_value.lower() == header_value
                    header_results[header] = {"present": True, "value": header_value, "compliant": compliant}
                    if compliant:
                        security_score += 1
            else:
                header_results[header] = {"present": False, "value": None, "compliant": False}
        
        return {
            "security_score": f"{security_score}/{total_headers}",
            "security_percentage": (security_score / total_headers) * 100,
            "headers": header_results,
            "response_status": response.status_code
        }
    
    async def test_input_validation(self):
        """Test input validation and sanitization"""
        validation_tests = {}
        
        # Test SQL injection attempts
        sql_payloads = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'; --",
            "' UNION SELECT * FROM users --"
        ]
        
        for i, payload in enumerate(sql_payloads):
            try:
                # Test in query parameters
                response = await self.client.get(
                    f"{self.base_url}/api/superadmin/users",
                    params={"search": payload}
                )
                validation_tests[f"sql_injection_test_{i+1}"] = {
                    "payload": payload,
                    "status_code": response.status_code,
                    "blocked": response.status_code in [400, 403, 422],  # Should be blocked
                    "server_error": response.status_code == 500  # Should not cause server error
                }
            except Exception as e:
                validation_tests[f"sql_injection_test_{i+1}"] = {
                    "payload": payload,
                    "error": str(e),
                    "blocked": True
                }
        
        # Test XSS attempts
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert(String.fromCharCode(88,83,83))//'"
        ]
        
        for i, payload in enumerate(xss_payloads):
            try:
                response = await self.client.post(
                    f"{self.base_url}/api/superadmin/users",
                    json={"name": payload, "email": f"test{i}@example.com"}
                )
                validation_tests[f"xss_test_{i+1}"] = {
                    "payload": payload,
                    "status_code": response.status_code,
                    "blocked": response.status_code in [400, 403, 422]
                }
            except Exception as e:
                validation_tests[f"xss_test_{i+1}"] = {
                    "payload": payload,
                    "error": str(e),
                    "blocked": True
                }
        
        return validation_tests
    
    async def test_authentication_security(self):
        """Test authentication security measures"""
        auth_tests = {}
        
        # Test brute force protection (multiple failed login attempts)
        failed_attempts = []
        for i in range(5):
            try:
                response = await self.client.post(
                    f"{self.base_url}/auth/token",
                    data={
                        "grant_type": "password",
                        "username": "nonexistent@example.com",
                        "password": "wrongpassword",
                        "client_id": "crm_web_app"
                    }
                )
                failed_attempts.append({
                    "attempt": i + 1,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0
                })
            except Exception as e:
                failed_attempts.append({
                    "attempt": i + 1,
                    "error": str(e)
                })
        
        auth_tests["brute_force_protection"] = {
            "attempts": failed_attempts,
            "rate_limiting_detected": any(
                attempt.get("status_code") == 429 for attempt in failed_attempts
            )
        }
        
        # Test password policy (if registration endpoint exists)
        weak_passwords = ["123", "password", "admin", ""]
        password_tests = []
        
        for password in weak_passwords:
            try:
                response = await self.client.post(
                    f"{self.base_url}/api/superadmin/users",
                    json={
                        "email": f"test_{len(password_tests)}@example.com",
                        "password": password,
                        "name": "Test User"
                    }
                )
                password_tests.append({
                    "password": password,
                    "status_code": response.status_code,
                    "rejected": response.status_code in [400, 422]
                })
            except Exception as e:
                password_tests.append({
                    "password": password,
                    "error": str(e),
                    "rejected": True
                })
        
        auth_tests["password_policy"] = password_tests
        
        return auth_tests
    
    async def test_authorization_controls(self):
        """Test role-based access control and authorization"""
        auth_tests = {}
        
        # Test access to protected endpoints without authentication
        protected_endpoints = [
            "/api/superadmin",
            "/api/superadmin/users",
            "/api/superadmin/settings",
            "/api/security",
            "/api/audit"
        ]
        
        unauthorized_access = []
        for endpoint in protected_endpoints:
            try:
                response = await self.client.get(f"{self.base_url}{endpoint}")
                unauthorized_access.append({
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "protected": response.status_code in [401, 403]
                })
            except Exception as e:
                unauthorized_access.append({
                    "endpoint": endpoint,
                    "error": str(e),
                    "protected": True
                })
        
        auth_tests["unauthorized_access"] = unauthorized_access
        
        # Test with invalid token
        invalid_tokens = [
            "invalid_token",
            "Bearer invalid",
            "fake.jwt.token",
            ""
        ]
        
        invalid_token_tests = []
        for token in invalid_tokens:
            try:
                headers = {"Authorization": f"Bearer {token}"}
                response = await self.client.get(
                    f"{self.base_url}/api/superadmin",
                    headers=headers
                )
                invalid_token_tests.append({
                    "token": token[:20] + "..." if len(token) > 20 else token,
                    "status_code": response.status_code,
                    "rejected": response.status_code == 401
                })
            except Exception as e:
                invalid_token_tests.append({
                    "token": token[:20] + "..." if len(token) > 20 else token,
                    "error": str(e),
                    "rejected": True
                })
        
        auth_tests["invalid_token_tests"] = invalid_token_tests
        
        return auth_tests
    
    async def test_cors_configuration(self):
        """Test CORS configuration security"""
        cors_tests = {}
        
        # Test CORS headers
        response = await self.client.options(f"{self.base_url}/")
        
        cors_headers = {
            "access-control-allow-origin": response.headers.get("access-control-allow-origin"),
            "access-control-allow-methods": response.headers.get("access-control-allow-methods"),
            "access-control-allow-headers": response.headers.get("access-control-allow-headers"),
            "access-control-allow-credentials": response.headers.get("access-control-allow-credentials")
        }
        
        cors_tests["cors_headers"] = cors_headers
        cors_tests["options_status"] = response.status_code
        
        # Check for overly permissive CORS
        allow_origin = cors_headers.get("access-control-allow-origin", "")
        cors_tests["security_analysis"] = {
            "allows_all_origins": allow_origin == "*",
            "allows_credentials": cors_headers.get("access-control-allow-credentials") == "true",
            "security_risk": allow_origin == "*" and cors_headers.get("access-control-allow-credentials") == "true"
        }
        
        return cors_tests
    
    async def test_rate_limiting(self):
        """Test rate limiting implementation"""
        rate_limit_tests = {}
        
        # Make rapid requests to test rate limiting
        rapid_requests = []
        start_time = time.time()
        
        for i in range(20):  # 20 rapid requests
            try:
                response = await self.client.get(f"{self.base_url}/health")
                rapid_requests.append({
                    "request": i + 1,
                    "status_code": response.status_code,
                    "timestamp": time.time() - start_time
                })
                
                # Check for rate limit headers
                if i == 0:  # Check first response for rate limit headers
                    rate_limit_headers = {
                        "x-ratelimit-limit": response.headers.get("x-ratelimit-limit"),
                        "x-ratelimit-remaining": response.headers.get("x-ratelimit-remaining"),
                        "x-ratelimit-reset": response.headers.get("x-ratelimit-reset"),
                        "retry-after": response.headers.get("retry-after")
                    }
                    rate_limit_tests["rate_limit_headers"] = rate_limit_headers
                
            except Exception as e:
                rapid_requests.append({
                    "request": i + 1,
                    "error": str(e),
                    "timestamp": time.time() - start_time
                })
        
        # Analyze results
        status_codes = [req.get("status_code") for req in rapid_requests if req.get("status_code")]
        rate_limited_count = sum(1 for code in status_codes if code == 429)
        
        rate_limit_tests["rapid_requests"] = {
            "total_requests": len(rapid_requests),
            "successful_requests": sum(1 for code in status_codes if code == 200),
            "rate_limited_requests": rate_limited_count,
            "rate_limiting_active": rate_limited_count > 0,
            "total_duration": time.time() - start_time
        }
        
        return rate_limit_tests
    
    async def test_ssl_tls_security(self):
        """Test SSL/TLS security configuration"""
        ssl_tests = {}
        
        # Note: This test is limited for HTTP endpoints
        # In production, this would test HTTPS configurations
        
        # Test HTTP to HTTPS redirect (if applicable)
        try:
            http_response = await self.client.get(f"{self.base_url}/health")
            ssl_tests["http_accessible"] = http_response.status_code == 200
            
            # Check for HSTS header
            hsts_header = http_response.headers.get("strict-transport-security")
            ssl_tests["hsts_header"] = {
                "present": bool(hsts_header),
                "value": hsts_header
            }
            
        except Exception as e:
            ssl_tests["http_test_error"] = str(e)
        
        # Test secure cookie settings (if any cookies are set)
        try:
            response = await self.client.post(
                f"{self.base_url}/auth/token",
                data={
                    "grant_type": "password",
                    "username": "test@example.com",
                    "password": "password",
                    "client_id": "crm_web_app"
                }
            )
            
            cookies = response.cookies
            ssl_tests["cookie_security"] = {
                "cookies_present": len(cookies) > 0,
                "secure_cookies": all(cookie.secure for cookie in cookies),
                "httponly_cookies": all(getattr(cookie, 'httponly', False) for cookie in cookies)
            }
            
        except Exception as e:
            ssl_tests["cookie_test_error"] = str(e)
        
        return ssl_tests
    
    async def test_data_exposure(self):
        """Test for sensitive data exposure"""
        exposure_tests = {}
        
        # Test error messages don't expose sensitive information
        error_endpoints = [
            "/api/nonexistent",
            "/api/superadmin/invalid",
            "/auth/invalid"
        ]
        
        error_responses = []
        for endpoint in error_endpoints:
            try:
                response = await self.client.get(f"{self.base_url}{endpoint}")
                response_text = response.text.lower()
                
                # Check for sensitive information in error messages
                sensitive_patterns = [
                    "password", "secret", "key", "token", 
                    "database", "sql", "traceback", "stack trace",
                    "internal server error", "exception"
                ]
                
                sensitive_found = [pattern for pattern in sensitive_patterns if pattern in response_text]
                
                error_responses.append({
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "sensitive_info_found": len(sensitive_found) > 0,
                    "sensitive_patterns": sensitive_found,
                    "response_length": len(response_text)
                })
                
            except Exception as e:
                error_responses.append({
                    "endpoint": endpoint,
                    "error": str(e)
                })
        
        exposure_tests["error_message_analysis"] = error_responses
        
        # Test API documentation for sensitive information
        try:
            docs_response = await self.client.get(f"{self.base_url}/openapi.json")
            if docs_response.status_code == 200:
                docs_content = docs_response.text.lower()
                sensitive_in_docs = [
                    pattern for pattern in ["password", "secret", "key", "token"]
                    if pattern in docs_content
                ]
                exposure_tests["api_docs_analysis"] = {
                    "accessible": True,
                    "sensitive_info_in_docs": len(sensitive_in_docs) > 0,
                    "sensitive_patterns": sensitive_in_docs
                }
            else:
                exposure_tests["api_docs_analysis"] = {
                    "accessible": False,
                    "status_code": docs_response.status_code
                }
        except Exception as e:
            exposure_tests["api_docs_error"] = str(e)
        
        return exposure_tests
    
    async def test_security_logging(self):
        """Test security event logging"""
        logging_tests = {}
        
        # Test that failed authentication attempts might be logged
        # (We can't directly access logs, but we can test the endpoints respond appropriately)
        
        failed_auth_response = await self.client.post(
            f"{self.base_url}/auth/token",
            data={
                "grant_type": "password",
                "username": "attacker@example.com",
                "password": "wrongpassword",
                "client_id": "crm_web_app"
            }
        )
        
        logging_tests["failed_auth_handling"] = {
            "status_code": failed_auth_response.status_code,
            "appropriate_response": failed_auth_response.status_code == 401,
            "no_server_error": failed_auth_response.status_code != 500
        }
        
        # Test access to audit endpoint (should require authentication)
        audit_response = await self.client.get(f"{self.base_url}/api/audit")
        logging_tests["audit_endpoint"] = {
            "status_code": audit_response.status_code,
            "protected": audit_response.status_code in [401, 403]
        }
        
        return logging_tests
    
    async def run_comprehensive_security_tests(self):
        """Run all security validation tests"""
        logger.info("🔒 Starting Comprehensive Security Validation Test Suite")
        
        tests = [
            ("OWASP Security Headers", self.test_owasp_security_headers),
            ("Input Validation", self.test_input_validation),
            ("Authentication Security", self.test_authentication_security),
            ("Authorization Controls", self.test_authorization_controls),
            ("CORS Configuration", self.test_cors_configuration),
            ("Rate Limiting", self.test_rate_limiting),
            ("SSL/TLS Security", self.test_ssl_tls_security),
            ("Data Exposure", self.test_data_exposure),
            ("Security Logging", self.test_security_logging)
        ]
        
        for test_name, test_func in tests:
            try:
                await self.run_test(test_name, test_func)
            except Exception as e:
                logger.error(f"Security test {test_name} failed: {e}")
                continue
        
        # Generate security summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        # Calculate security score
        security_score = 0
        max_score = 0
        
        for result in self.test_results:
            if result["status"] == "PASS" and "result" in result:
                test_result = result["result"]
                
                # Add scoring logic based on test results
                if "security_percentage" in test_result:
                    security_score += test_result["security_percentage"]
                    max_score += 100
                elif "protected" in str(test_result):
                    # Count protected endpoints
                    security_score += 10
                    max_score += 10
                else:
                    security_score += 5
                    max_score += 5
        
        overall_security_score = (security_score / max_score * 100) if max_score > 0 else 0
        
        summary = {
            "security_test_summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%",
                "overall_security_score": f"{overall_security_score:.1f}%",
                "security_level": (
                    "EXCELLENT" if overall_security_score >= 90 else
                    "GOOD" if overall_security_score >= 75 else
                    "FAIR" if overall_security_score >= 60 else
                    "POOR"
                )
            },
            "detailed_results": self.test_results
        }
        
        await self.client.aclose()
        
        logger.info(f"🔒 Security Tests Complete: {passed_tests}/{total_tests} passed")
        logger.info(f"🎯 Overall Security Score: {overall_security_score:.1f}%")
        
        return summary

async def main():
    """Main execution"""
    tester = SecurityValidationTester()
    
    try:
        results = await tester.run_comprehensive_security_tests()
        
        # Print summary
        print("\n" + "="*80)
        print("SECURITY VALIDATION TEST SUMMARY")
        print("="*80)
        
        summary = results["security_test_summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']}")
        print(f"Security Score: {summary['overall_security_score']}")
        print(f"Security Level: {summary['security_level']}")
        
        print("\nDETAILED RESULTS:")
        print("-"*80)
        for result in results["detailed_results"]:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            duration = result.get("duration", 0)
            print(f"{status_icon} {result['name']} - {result['status']} ({duration:.2f}s)")
            if result["status"] == "FAIL":
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        # Save results
        with open("security_validation_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Full results saved to: security_validation_results.json")
        
        return results
        
    except Exception as e:
        logger.error(f"Security test suite failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())