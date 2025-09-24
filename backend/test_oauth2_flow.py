#!/usr/bin/env python3
"""
OAuth2+PKCE End-to-End Testing Script
Tests the complete OAuth2 authentication flow
"""
import requests
import json
import sys
import time
from typing import Dict, Any

BASE_URL = "http://localhost:5173"

class OAuth2TestSuite:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"    Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        print()
    
    def test_server_health(self) -> bool:
        """Test if server is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                self.log_test("Server Health Check", True, f"Status: {response.json()['status']}")
                return True
            else:
                self.log_test("Server Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Health Check", False, str(e))
            return False
    
    def test_pkce_challenge_generation(self) -> Dict[str, str]:
        """Test PKCE challenge generation"""
        try:
            response = self.session.post(f"{self.base_url}/auth/challenge", json={})
            
            if response.status_code == 200:
                data = response.json()
                if "code_challenge" in data and "code_challenge_method" in data:
                    self.log_test("PKCE Challenge Generation", True, 
                                f"Challenge method: {data['code_challenge_method']}")
                    return data
                else:
                    self.log_test("PKCE Challenge Generation", False, 
                                "Missing required fields in response")
                    return {}
            else:
                self.log_test("PKCE Challenge Generation", False, 
                            f"Status code: {response.status_code}, Response: {response.text}")
                return {}
        except Exception as e:
            self.log_test("PKCE Challenge Generation", False, str(e))
            return {}
    
    def test_oauth2_discovery(self) -> bool:
        """Test OAuth2 discovery endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/auth/.well-known/oauth-authorization-server")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["issuer", "authorization_endpoint", "token_endpoint"]
                
                if all(field in data for field in required_fields):
                    self.log_test("OAuth2 Discovery", True, 
                                f"Issuer: {data['issuer']}")
                    return True
                else:
                    self.log_test("OAuth2 Discovery", False, 
                                "Missing required discovery fields")
                    return False
            else:
                self.log_test("OAuth2 Discovery", False, 
                            f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("OAuth2 Discovery", False, str(e))
            return False
    
    def test_token_endpoint_direct(self) -> Dict[str, Any]:
        """Test direct token generation using simplified endpoint"""
        try:
            token_data = {
                "grant_type": "password",
                "username": "test@crm.com",
        "password": "TestPassword123!",
                "client_id": "crm_web_app",
                "scope": "read write"
            }
            
            response = self.session.post(f"{self.base_url}/auth/token", json=token_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.log_test("Direct Token Generation", True, 
                                f"Token type: {data['token_type']}")
                    return data
                else:
                    self.log_test("Direct Token Generation", False, 
                                "Missing required token fields")
                    return {}
            else:
                self.log_test("Direct Token Generation", False, 
                            f"Status code: {response.status_code}, Response: {response.text}")
                return {}
        except Exception as e:
            self.log_test("Direct Token Generation", False, str(e))
            return {}
    
    def test_protected_endpoint_access(self, access_token: str) -> bool:
        """Test accessing protected endpoint with access token"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = self.session.get(f"{self.base_url}/auth/userinfo", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "sub" in data or "email" in data:
                    self.log_test("Protected Endpoint Access", True, 
                                f"User info retrieved for: {data.get('email', 'N/A')}")
                    return True
                else:
                    self.log_test("Protected Endpoint Access", False, 
                                "Invalid user info response")
                    return False
            else:
                self.log_test("Protected Endpoint Access", False, 
                            f"Status code: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Protected Endpoint Access", False, str(e))
            return False
    
    def test_token_refresh(self, refresh_token: str) -> Dict[str, Any]:
        """Test token refresh functionality"""
        try:
            refresh_data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": "crm_web_app"
            }
            
            response = self.session.post(f"{self.base_url}/auth/refresh", json=refresh_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.log_test("Token Refresh", True, 
                                "New access token generated")
                    return data
                else:
                    self.log_test("Token Refresh", False, 
                                "Missing access token in refresh response")
                    return {}
            else:
                self.log_test("Token Refresh", False, 
                            f"Status code: {response.status_code}, Response: {response.text}")
                return {}
        except Exception as e:
            self.log_test("Token Refresh", False, str(e))
            return {}
    
    def test_token_revocation(self, access_token: str) -> bool:
        """Test token revocation"""
        try:
            revoke_data = {
                "token": access_token,
                "token_type_hint": "access_token"
            }
            
            response = self.session.post(f"{self.base_url}/auth/revoke", json=revoke_data)
            
            if response.status_code == 200:
                self.log_test("Token Revocation", True, "Token revoked successfully")
                return True
            else:
                self.log_test("Token Revocation", False, 
                            f"Status code: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Token Revocation", False, str(e))
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive OAuth2+PKCE test suite"""
        print("=" * 60)
        print("OAuth2+PKCE COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print()
        
        # Test 1: Server Health
        if not self.test_server_health():
            print("❌ Server is not accessible. Stopping tests.")
            return
        
        # Test 2: PKCE Challenge Generation
        challenge_data = self.test_pkce_challenge_generation()
        
        # Test 3: OAuth2 Discovery
        self.test_oauth2_discovery()
        
        # Test 4: Direct Token Generation
        token_data = self.test_token_endpoint_direct()
        
        if token_data and "access_token" in token_data:
            access_token = token_data["access_token"]
            
            # Test 5: Protected Endpoint Access
            self.test_protected_endpoint_access(access_token)
            
            # Test 6: Token Refresh (if refresh token available)
            if "refresh_token" in token_data:
                refresh_data = self.test_token_refresh(token_data["refresh_token"])
                
                # Use new access token if refresh was successful
                if refresh_data and "access_token" in refresh_data:
                    access_token = refresh_data["access_token"]
            
            # Test 7: Token Revocation
            self.test_token_revocation(access_token)
        
        # Generate Summary
        self.generate_test_summary()
    
    def generate_test_summary(self):
        """Generate test summary report"""
        print("=" * 60)
        print("TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: ✅ {passed_tests}")
        print(f"Failed: ❌ {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        else:
            print("🎉 All tests passed! OAuth2+PKCE implementation is working correctly.")
        
        print("=" * 60)

def main():
    """Main test execution"""
    tester = OAuth2TestSuite()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()