"""
Simple API Endpoint Test Script
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from app.main import app

def test_api_endpoints():
    """Test all API endpoints"""
    client = TestClient(app)
    
    print("🚀 Testing CRM API Endpoints")
    print("=" * 50)
    
    # Test results
    passed = 0
    failed = 0
    
    # Test cases: (endpoint, expected_status, description)
    test_cases = [
        ("/", 200, "Root endpoint"),
        ("/sales/leads", 200, "Sales leads"),
        ("/sales/opportunities", 200, "Sales opportunities"),
        ("/sales/contacts", 200, "Sales contacts"),
        ("/sales/activities", 200, "Sales activities"),
        ("/sales/quotations", 200, "Sales quotations"),
        ("/sales/targets", 200, "Sales targets"),
        ("/sales/reports", 200, "Sales reports"),
        ("/marketing/campaigns", 200, "Marketing campaigns"),
        ("/marketing/leads", 200, "Marketing leads"),
        ("/marketing/email", 200, "Email marketing"),
        ("/marketing/social", 200, "Social media"),
        ("/marketing/content", 200, "Content management"),
        ("/marketing/analytics", 200, "Marketing analytics"),
        ("/marketing/automation", 200, "Marketing automation"),
        ("/marketing/segmentation", 200, "Customer segmentation"),
        ("/marketing/events", 200, "Event management"),
        ("/marketing/partners", 200, "Partner management"),
        ("/marketing/resources", 200, "Resource management"),
        ("/marketing/cdp", 200, "Customer Data Platform"),
        ("/support/tickets", 200, "Support tickets"),
        ("/support/knowledge", 200, "Knowledge base"),
        ("/support/automation", 200, "Support automation"),
        ("/support/sla", 200, "SLA management"),
        ("/support/reporting", 200, "Support reporting"),
        ("/api/superadmin/users", 200, "Super admin users"),
        ("/api/compliance/retention/policies", 200, "Data retention policies"),
        ("/api/compliance/deletion/requests", 200, "Data deletion requests"),
        ("/api/compliance/consent/templates", 200, "Consent templates"),
        ("/api/security/rate-limits", 200, "Rate limits"),
        ("/api/security/config", 200, "Security config"),
        ("/api/audit/logs", 200, "Audit logs"),
        ("/api/data/classifications", 200, "Data classifications"),
    ]
    
    for endpoint, expected_status, description in test_cases:
        try:
            response = client.get(endpoint)
            if response.status_code == expected_status:
                print(f"✅ {description}: {endpoint}")
                passed += 1
            else:
                print(f"❌ {description}: {endpoint} (Status: {response.status_code})")
                failed += 1
        except Exception as e:
            print(f"❌ {description}: {endpoint} (Error: {str(e)})")
            failed += 1
    
    # Test POST endpoints
    print("\n📝 Testing POST Endpoints...")
    
    # Test input validation
    try:
        test_data = {
            "input_data": "Test input <script>alert('xss')</script>",
            "input_type": "text"
        }
        response = client.post("/api/security/validate-input", json=test_data)
        if response.status_code == 200:
            print("✅ Input validation endpoint")
            passed += 1
        else:
            print(f"❌ Input validation endpoint (Status: {response.status_code})")
            failed += 1
    except Exception as e:
        print(f"❌ Input validation endpoint (Error: {str(e)})")
        failed += 1
    
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
        response = client.post("/api/audit/logs", json=log_data)
        if response.status_code == 200:
            print("✅ Audit log creation")
            passed += 1
        else:
            print(f"❌ Audit log creation (Status: {response.status_code})")
            failed += 1
    except Exception as e:
        print(f"❌ Audit log creation (Error: {str(e)})")
        failed += 1
    
    # Test security headers
    try:
        response = client.get("/")
        headers = response.headers
        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy"
        ]
        
        missing_headers = [h for h in required_headers if h not in headers]
        if not missing_headers:
            print("✅ Security headers present")
            passed += 1
        else:
            print(f"❌ Missing security headers: {missing_headers}")
            failed += 1
    except Exception as e:
        print(f"❌ Security headers test (Error: {str(e)})")
        failed += 1
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total: {passed + failed}")
    
    success_rate = (passed / (passed + failed)) * 100 if (passed + failed) > 0 else 0
    print(f"🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 Excellent! API endpoints are working well!")
    elif success_rate >= 75:
        print("👍 Good! Most endpoints are working properly.")
    else:
        print("⚠️  Some issues found. Please check the failed endpoints.")
    
    return success_rate >= 75

if __name__ == "__main__":
    success = test_api_endpoints()
    sys.exit(0 if success else 1)