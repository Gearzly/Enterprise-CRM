#!/usr/bin/env python3
"""
Integration test suite for Super Admin module and all other modules
"""
import requests
import sys
import json

BASE_URL = "http://localhost:8000"
SUPERADMIN_PREFIX = "/api/superadmin"
SALES_PREFIX = "/sales"
MARKETING_PREFIX = "/marketing"

def test_sales_config_integration():
    """Test integration between Super Admin Sales Config and Sales module"""
    print("Testing Sales Configuration Integration...")
    
    # Get sales configuration from Super Admin
    superadmin_endpoints = [
        f"{BASE_URL}{SUPERADMIN_PREFIX}/sales-config/key/lead_statuses",
        f"{BASE_URL}{SUPERADMIN_PREFIX}/sales-config/key/lead_sources",
        f"{BASE_URL}{SUPERADMIN_PREFIX}/sales-config/key/opportunity_stages",
        f"{BASE_URL}{SUPERADMIN_PREFIX}/sales-config/key/quotation_statuses",
    ]
    
    # Get sales configuration from Sales module
    sales_endpoints = [
        f"{BASE_URL}{SALES_PREFIX}/leads/config/statuses",
        f"{BASE_URL}{SALES_PREFIX}/leads/config/sources",
        f"{BASE_URL}{SALES_PREFIX}/opportunities/config/stages",
        f"{BASE_URL}{SALES_PREFIX}/quotations/config/statuses",
    ]
    
    passed = 0
    total = len(superadmin_endpoints) + len(sales_endpoints)
    
    # Test Super Admin endpoints
    for endpoint in superadmin_endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"✓ {endpoint} - Status: {response.status_code}")
                passed += 1
            else:
                print(f"✗ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {endpoint} - Error: {e}")
    
    # Test Sales module endpoints
    for endpoint in sales_endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"✓ {endpoint} - Status: {response.status_code}")
                passed += 1
            else:
                print(f"✗ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {endpoint} - Error: {e}")
    
    print(f"Sales Config Integration: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_config_integration():
    """Test integration between Super Admin Marketing Config and Marketing module"""
    print("Testing Marketing Configuration Integration...")
    
    # Get marketing configuration from Super Admin
    superadmin_endpoints = [
        f"{BASE_URL}{SUPERADMIN_PREFIX}/marketing-config/key/campaign_statuses",
        f"{BASE_URL}{SUPERADMIN_PREFIX}/marketing-config/key/campaign_types",
        f"{BASE_URL}{SUPERADMIN_PREFIX}/marketing-config/key/lead_statuses",
        f"{BASE_URL}{SUPERADMIN_PREFIX}/marketing-config/key/lead_sources",
    ]
    
    # Get marketing configuration from Marketing module
    marketing_endpoints = [
        f"{BASE_URL}{MARKETING_PREFIX}/campaigns/config/statuses",
        f"{BASE_URL}{MARKETING_PREFIX}/campaigns/config/types",
        f"{BASE_URL}{MARKETING_PREFIX}/leads/config/statuses",
        f"{BASE_URL}{MARKETING_PREFIX}/leads/config/sources",
    ]
    
    passed = 0
    total = len(superadmin_endpoints) + len(marketing_endpoints)
    
    # Test Super Admin endpoints
    for endpoint in superadmin_endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"✓ {endpoint} - Status: {response.status_code}")
                passed += 1
            else:
                print(f"✗ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {endpoint} - Error: {e}")
    
    # Test Marketing module endpoints
    for endpoint in marketing_endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"✓ {endpoint} - Status: {response.status_code}")
                passed += 1
            else:
                print(f"✗ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {endpoint} - Error: {e}")
    
    print(f"Marketing Config Integration: {passed}/{total} tests passed\n")
    return passed, total

def test_module_assignment_integration():
    """Test module assignment integration"""
    print("Testing Module Assignment Integration...")
    
    endpoints = [
        f"{BASE_URL}{SUPERADMIN_PREFIX}/modules/",
        f"{BASE_URL}{SUPERADMIN_PREFIX}/modules/assignments/",
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"✓ {endpoint} - Status: {response.status_code}")
                passed += 1
            else:
                print(f"✗ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {endpoint} - Error: {e}")
    
    print(f"Module Assignment Integration: {passed}/{total} tests passed\n")
    return passed, total

def test_organization_integration():
    """Test organization integration"""
    print("Testing Organization Integration...")
    
    endpoints = [
        f"{BASE_URL}{SUPERADMIN_PREFIX}/organizations/",
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"✓ {endpoint} - Status: {response.status_code}")
                passed += 1
            else:
                print(f"✗ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {endpoint} - Error: {e}")
    
    print(f"Organization Integration: {passed}/{total} tests passed\n")
    return passed, total

def main():
    """Test integration between Super Admin and all other modules"""
    print("Testing Super Admin integration with all modules...\n")
    
    # Test each integration
    sales_passed, sales_total = test_sales_config_integration()
    marketing_passed, marketing_total = test_marketing_config_integration()
    module_passed, module_total = test_module_assignment_integration()
    org_passed, org_total = test_organization_integration()
    
    # Calculate overall results
    passed = sales_passed + marketing_passed + module_passed + org_passed
    total = sales_total + marketing_total + module_total + org_total
    
    print(f"\nIntegration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All integration tests passed! ✅")
        return 0
    else:
        print("Some integration tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())