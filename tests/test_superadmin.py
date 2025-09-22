#!/usr/bin/env python3
"""
Test suite for the Super Admin module
"""
import requests
import sys
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/superadmin"

def test_superadmin_organizations():
    """Test Super Admin Organizations endpoints"""
    print("Testing Super Admin Organizations endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/organizations/",
        f"{BASE_URL}{API_PREFIX}/organizations/categories",
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
    
    print(f"Super Admin Organizations: {passed}/{total} tests passed\n")
    return passed, total

def test_superadmin_security():
    """Test Super Admin Security endpoints"""
    print("Testing Super Admin Security endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/security/roles",
        f"{BASE_URL}{API_PREFIX}/security/permissions",
        f"{BASE_URL}{API_PREFIX}/security/policies",
        f"{BASE_URL}{API_PREFIX}/security/users",
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
    
    print(f"Super Admin Security: {passed}/{total} tests passed\n")
    return passed, total

def test_superadmin_settings():
    """Test Super Admin Settings endpoints"""
    print("Testing Super Admin Settings endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/settings/",
        f"{BASE_URL}{API_PREFIX}/settings/categories",
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
    
    print(f"Super Admin Settings: {passed}/{total} tests passed\n")
    return passed, total

def test_superadmin_modules():
    """Test Super Admin Modules endpoints"""
    print("Testing Super Admin Modules endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/modules/",
        f"{BASE_URL}{API_PREFIX}/modules/assignments/",
        f"{BASE_URL}{API_PREFIX}/modules/categories",
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
    
    print(f"Super Admin Modules: {passed}/{total} tests passed\n")
    return passed, total

def test_superadmin_sales_config():
    """Test Super Admin Sales Configuration endpoints"""
    print("Testing Super Admin Sales Configuration endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/sales-config/",
        f"{BASE_URL}{API_PREFIX}/sales-config/categories",
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
    
    print(f"Super Admin Sales Config: {passed}/{total} tests passed\n")
    return passed, total

def test_superadmin_marketing_config():
    """Test Super Admin Marketing Configuration endpoints"""
    print("Testing Super Admin Marketing Configuration endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/marketing-config/",
        f"{BASE_URL}{API_PREFIX}/marketing-config/categories",
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
    
    print(f"Super Admin Marketing Config: {passed}/{total} tests passed\n")
    return passed, total

def main():
    """Test all Super Admin endpoints"""
    print("Testing Super Admin module endpoints...\n")
    
    # Test each submodule
    org_passed, org_total = test_superadmin_organizations()
    sec_passed, sec_total = test_superadmin_security()
    set_passed, set_total = test_superadmin_settings()
    mod_passed, mod_total = test_superadmin_modules()
    sales_passed, sales_total = test_superadmin_sales_config()
    marketing_passed, marketing_total = test_superadmin_marketing_config()
    
    # Calculate overall results
    passed = org_passed + sec_passed + set_passed + mod_passed + sales_passed + marketing_passed
    total = org_total + sec_total + set_total + mod_total + sales_total + marketing_total
    
    print(f"\nSuper Admin Module Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All Super Admin tests passed! ✅")
        return 0
    else:
        print("Some Super Admin tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())