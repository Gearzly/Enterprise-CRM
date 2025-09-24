"""
Comprehensive API endpoint testing suite
Tests all modules: Sales, Marketing, Support, Super Admin, Security, and Compliance
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from httpx import AsyncClient
from fastapi.testclient import TestClient
import pytest
from typing import Optional

try:
    from app.main import app
except ImportError:
    # Fallback for testing environment
    from fastapi import FastAPI
    app = FastAPI(title="Test App")

class APIEndpointTester:
    """Comprehensive API endpoint tester"""
    
    def __init__(self):
        if app is None:
            from fastapi import FastAPI
            test_app = FastAPI(title="Test App")
            self.client = TestClient(test_app)
        else:
            self.client = TestClient(app)
        self.base_url = "http://testserver"
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    def log_result(self, test_name: str, success: bool, error: Optional[str] = None):
        """Log test result"""
        if success:
            self.test_results["passed"] += 1
            print(f"✅ {test_name}")
        else:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"{test_name}: {error}")
            print(f"❌ {test_name}: {error}")
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        try:
            response = self.client.get("/")
            success = response.status_code == 200 and "SaaS CRM Backend API" in response.json()["message"]
            error_msg = None if success else f"Status: {response.status_code}"
            self.log_result("Root Endpoint", success, error_msg)
        except Exception as e:
            self.log_result("Root Endpoint", False, str(e))
    
    def test_sales_endpoints(self):
        """Test core sales module endpoints"""
        endpoints = [
            "/sales/leads",
            "/sales/opportunities", 
            "/sales/contacts",
            "/sales/activities",
            "/sales/quotations",
            "/sales/targets",
            "/sales/reports"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]  # 422 is acceptable for missing query params
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"Sales {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"Sales {endpoint}", False, str(e))
    
    def test_marketing_endpoints(self):
        """Test marketing module endpoints"""
        endpoints = [
            "/marketing/campaigns",
            "/marketing/leads",
            "/marketing/email",
            "/marketing/social",
            "/marketing/content",
            "/marketing/analytics",
            "/marketing/automation",
            "/marketing/segmentation",
            "/marketing/events",
            "/marketing/partners",
            "/marketing/resources",
            "/marketing/cdp"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"Marketing {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"Marketing {endpoint}", False, str(e))
    
    def test_support_endpoints(self):
        """Test support module endpoints"""
        endpoints = [
            "/support/tickets",
            "/support/knowledge",
            "/support/automation",
            "/support/sla",
            "/support/reporting",
            "/support/call-center",
            "/support/live-chat",
            "/support/community",
            "/support/feedback",
            "/support/integrations",
            "/support/assets",
            "/support/remote",
            "/support/interactions",
            "/support/social",
            "/support/language"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"Support {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"Support {endpoint}", False, str(e))
    
    def test_superadmin_endpoints(self):
        """Test super admin endpoints"""
        endpoints = [
            "/api/superadmin/users",
            "/api/superadmin/roles",
            "/api/superadmin/permissions"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"SuperAdmin {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"SuperAdmin {endpoint}", False, str(e))
    
    def test_compliance_endpoints(self):
        """Test GDPR/HIPAA compliance endpoints"""
        endpoints = [
            "/api/compliance/retention/policies",
            "/api/compliance/deletion/requests", 
            "/api/compliance/consent/templates",
            "/api/compliance/consent/records"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"Compliance {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"Compliance {endpoint}", False, str(e))
    
    def test_security_endpoints(self):
        """Test OWASP security endpoints"""
        endpoints = [
            "/api/security/rate-limits",
            "/api/security/config",
            "/api/security/secrets",
            "/api/security/certificates",
            "/api/security/key-rotation"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"Security {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"Security {endpoint}", False, str(e))
    
    def test_audit_endpoints(self):
        """Test audit logging endpoints"""
        endpoints = [
            "/api/audit/logs"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"Audit {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"Audit {endpoint}", False, str(e))
    
    def test_data_classification_endpoints(self):
        """Test data classification endpoints"""
        endpoints = [
            "/api/data/classifications",
            "/api/data/labels"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                success = response.status_code in [200, 422]
                error_msg = None if success else f"Status: {response.status_code}"
                self.log_result(f"Data Classification {endpoint}", success, error_msg)
            except Exception as e:
                self.log_result(f"Data Classification {endpoint}", False, str(e))
    
    def test_security_headers(self):
        """Test OWASP security headers"""
        try:
            response = self.client.get("/")
            headers = response.headers
            
            required_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options", 
                "X-XSS-Protection",
                "Strict-Transport-Security",
                "Content-Security-Policy"
            ]
            
            missing_headers = [h for h in required_headers if h not in headers]
            success = len(missing_headers) == 0
            
            error_msg = f"Missing headers: {missing_headers}" if missing_headers else None
            self.log_result("Security Headers", success, error_msg)
            
        except Exception as e:
            self.log_result("Security Headers", False, str(e))
    
    def test_post_endpoints(self):
        """Test POST endpoints with sample data"""
        
        # Test input validation
        try:
            test_data = {
                "input_data": "Test input <script>alert('test')</script>",
                "input_type": "text"
            }
            response = self.client.post("/api/security/validate-input", json=test_data)
            success = response.status_code == 200
            error_msg = None if success else f"Status: {response.status_code}"
            self.log_result("POST Security Input Validation", success, error_msg)
        except Exception as e:
            self.log_result("POST Security Input Validation", False, str(e))
        
        # Test audit log creation
        try:
            log_data = {
                "action": "test_action",
                "resource_type": "test",
                "resource_id": "test123",
                "user_id": "testuser",
                "ip_address": "127.0.0.1",
                "user_agent": "Test Agent"
            }
            response = self.client.post("/api/audit/logs", json=log_data)
            success = response.status_code == 200
            error_msg = None if success else f"Status: {response.status_code}"
            self.log_result("POST Audit Log Creation", success, error_msg)
        except Exception as e:
            self.log_result("POST Audit Log Creation", False, str(e))
        
        # Test access permission check
        try:
            access_data = {
                "user_id": "testuser",
                "resource_type": "test",
                "resource_id": "test123",
                "action": "read"
            }
            response = self.client.post("/api/data/check-access", json=access_data)
            success = response.status_code == 200
            error_msg = None if success else f"Status: {response.status_code}"
            self.log_result("POST Access Permission Check", success, error_msg)
        except Exception as e:
            self.log_result("POST Access Permission Check", False, str(e))
    
    def run_all_tests(self):
        """Run all API endpoint tests"""
        print("🚀 Starting Comprehensive API Endpoint Testing")
        print("=" * 60)
        
        # Test all modules
        self.test_root_endpoint()
        print("\n📊 Testing Sales Module...")
        self.test_sales_endpoints()
        
        print("\n📈 Testing Marketing Module...")
        self.test_marketing_endpoints()
        
        print("\n🎧 Testing Support Module...")
        self.test_support_endpoints()
        
        print("\n👑 Testing Super Admin Module...")
        self.test_superadmin_endpoints()
        
        print("\n🔒 Testing Security & Compliance...")
        self.test_compliance_endpoints()
        self.test_security_endpoints()
        self.test_audit_endpoints()
        self.test_data_classification_endpoints()
        
        print("\n🛡️ Testing Security Features...")
        self.test_security_headers()
        
        print("\n📝 Testing POST Endpoints...")
        self.test_post_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        print(f"📊 Total: {self.test_results['passed'] + self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\n🚨 ERRORS:")
            for error in self.test_results['errors']:
                print(f"   • {error}")
        
        success_rate = (self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed'])) * 100
        print(f"\n🎯 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 Excellent! API endpoints are working well!")
        elif success_rate >= 75:
            print("👍 Good! Most endpoints are working properly.")
        else:
            print("⚠️  Some issues found. Review the errors above.")
        
        return success_rate >= 75

def main():
    """Main test runner"""
    try:
        tester = APIEndpointTester()
        success = tester.run_all_tests()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Critical error during testing: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)