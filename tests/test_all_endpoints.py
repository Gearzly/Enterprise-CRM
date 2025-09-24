#!/usr/bin/env python3
"""
Comprehensive Test script for the SaaS CRM Backend endpoints
Tests all modules: Sales, Marketing, Support, SuperAdmin, Compliance, Security, Audit, Data Classification
"""
import requests
import sys
import json
from typing import List, Dict, Any

BASE_URL = "http://localhost:8001"

def test_endpoint(url, method="GET", expected_status=200, data=None):
    """Test a single endpoint with specified HTTP method"""
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url)
        else:
            print(f"✗ {url} - Unsupported method: {method}")
            return False
            
        if response.status_code == expected_status:
            print(f"✓ {method} {url} - Status: {response.status_code}")
            return True
        else:
            print(f"✗ {method} {url} - Status: {response.status_code}, Expected: {expected_status}")
            if response.status_code != 404:  # Don't show content for 404s
                try:
                    error_content = response.json()
                    print(f"  Error: {error_content}")
                except:
                    print(f"  Response: {response.text[:200]}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ {method} {url} - Connection Error: {e}")
        return False

def main():
    """Test all CRM system endpoints comprehensively"""
    print("Testing SaaS CRM Backend - All Endpoints\n")
    print(f"Base URL: {BASE_URL}")
    print("=" * 50)
    
    # Core endpoints
    core_endpoints = [
        f"{BASE_URL}/",
    ]
    
    # Sales Module endpoints
    sales_endpoints = [
        f"{BASE_URL}/sales/",
        f"{BASE_URL}/sales/activity/",
        f"{BASE_URL}/sales/contact/",
        f"{BASE_URL}/sales/lead/",
        f"{BASE_URL}/sales/opportunity/",
        f"{BASE_URL}/sales/quotation/",
        f"{BASE_URL}/sales/report/",
        f"{BASE_URL}/sales/target/",
        # Configuration endpoints
        f"{BASE_URL}/sales/activity/config/types",
        f"{BASE_URL}/sales/activity/config/statuses",
        f"{BASE_URL}/sales/contact/config/types",
        f"{BASE_URL}/sales/lead/config/statuses",
        f"{BASE_URL}/sales/lead/config/sources",
        f"{BASE_URL}/sales/opportunity/config/stages",
        f"{BASE_URL}/sales/quotation/config/statuses",
        f"{BASE_URL}/sales/report/config/types",
        f"{BASE_URL}/sales/report/config/statuses",
        f"{BASE_URL}/sales/target/config/types",
    ]
    
    # Marketing Module endpoints
    marketing_endpoints = [
        f"{BASE_URL}/marketing/",
        f"{BASE_URL}/marketing/campaigns/",
        f"{BASE_URL}/marketing/leads/",
        f"{BASE_URL}/marketing/email/lists",
        f"{BASE_URL}/marketing/email/subscribers",
        f"{BASE_URL}/marketing/email/templates",
        f"{BASE_URL}/marketing/email/campaigns",
        f"{BASE_URL}/marketing/email/sequences",
        f"{BASE_URL}/marketing/email/sequence-steps",
        f"{BASE_URL}/marketing/email/config/statuses",
        f"{BASE_URL}/marketing/email/config/template-categories",
        f"{BASE_URL}/marketing/social-media/",
        f"{BASE_URL}/marketing/content/",
        f"{BASE_URL}/marketing/analytics/",
        f"{BASE_URL}/marketing/automation/",
        f"{BASE_URL}/marketing/segmentation/",
        f"{BASE_URL}/marketing/events/",
        f"{BASE_URL}/marketing/partners/",
        f"{BASE_URL}/marketing/resources/",
        f"{BASE_URL}/marketing/cdp/",
    ]
    
    # Support Module endpoints
    support_endpoints = [
        f"{BASE_URL}/support/",
        f"{BASE_URL}/support/tickets/",
        f"{BASE_URL}/support/tickets/slas",
        f"{BASE_URL}/support/tickets/config/priorities",
        f"{BASE_URL}/support/tickets/config/statuses",
        f"{BASE_URL}/support/tickets/config/channels",
        f"{BASE_URL}/support/knowledge-base/",
        f"{BASE_URL}/support/interactions/",
        f"{BASE_URL}/support/live-chat/",
        f"{BASE_URL}/support/call-center/",
        f"{BASE_URL}/support/social-support/",
        f"{BASE_URL}/support/feedback/",
        f"{BASE_URL}/support/sla/",
        f"{BASE_URL}/support/asset/",
        f"{BASE_URL}/support/remote/",
        f"{BASE_URL}/support/community/",
        f"{BASE_URL}/support/reporting/",
        f"{BASE_URL}/support/automation/",
        f"{BASE_URL}/support/mobile/",
        f"{BASE_URL}/support/integration/",
        f"{BASE_URL}/support/language/",
    ]
    
    # Super Admin Module endpoints
    superadmin_endpoints = [
        f"{BASE_URL}/api/superadmin/",
        f"{BASE_URL}/api/superadmin/organizations",
        f"{BASE_URL}/api/superadmin/security",
        f"{BASE_URL}/api/superadmin/settings",
        f"{BASE_URL}/api/superadmin/modules",
        f"{BASE_URL}/api/superadmin/sales-config",
        f"{BASE_URL}/api/superadmin/marketing-config",
        f"{BASE_URL}/api/superadmin/support-config",
    ]
    
    # Core API endpoints (Compliance, Security, Audit, Data Classification)
    core_api_endpoints = [
        f"{BASE_URL}/api/compliance/retention",
        f"{BASE_URL}/api/compliance/deletion",
        f"{BASE_URL}/api/compliance/consent",
        f"{BASE_URL}/api/security/",
        f"{BASE_URL}/api/security/validate",
        f"{BASE_URL}/api/security/threats",
        f"{BASE_URL}/api/audit/",
        f"{BASE_URL}/api/audit/logs",
        f"{BASE_URL}/api/data/",
        f"{BASE_URL}/api/data/classification",
    ]
    
    # Test categories
    test_categories = [
        ("Core", core_endpoints),
        ("Sales", sales_endpoints), 
        ("Marketing", marketing_endpoints),
        ("Support", support_endpoints),
        ("Super Admin", superadmin_endpoints),
        ("Core APIs", core_api_endpoints),
    ]
    
    total_passed = 0
    total_tests = 0
    results = {}
    
    for category_name, endpoints in test_categories:
        print(f"\n📋 Testing {category_name} Module ({len(endpoints)} endpoints)")
        print("-" * 40)
        
        passed = 0
        for endpoint in endpoints:
            if test_endpoint(endpoint):
                passed += 1
            total_tests += 1
        
        total_passed += passed
        results[category_name] = f"{passed}/{len(endpoints)}"
        print(f"\n{category_name} Results: {passed}/{len(endpoints)} passed")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 50)
    
    for category, result in results.items():
        print(f"{category:15}: {result}")
    
    print(f"\nOverall: {total_passed}/{total_tests} tests passed")
    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! CRM system is responding correctly! ✅")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} tests failed! Check the endpoints above. ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())