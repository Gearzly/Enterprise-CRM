#!/usr/bin/env python3
"""
Test script for the SaaS CRM Backend endpoints
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(url, expected_status=200):
    """Test a single endpoint"""
    try:
        response = requests.get(url)
        if response.status_code == expected_status:
            print(f"✓ {url} - Status: {response.status_code}")
            return True
        else:
            print(f"✗ {url} - Status: {response.status_code}, Expected: {expected_status}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ {url} - Error: {e}")
        return False

def main():
    """Test all endpoints"""
    print("Testing SaaS CRM Backend endpoints...\n")
    
    endpoints = [
        f"{BASE_URL}/",
        f"{BASE_URL}/sales/",
        f"{BASE_URL}/sales/contacts",
        f"{BASE_URL}/sales/leads",
        f"{BASE_URL}/sales/opportunities",
        f"{BASE_URL}/sales/activities",
        f"{BASE_URL}/sales/quotations",
        f"{BASE_URL}/sales/reports/sales",
        f"{BASE_URL}/sales/reports/sales/metrics",
        f"{BASE_URL}/sales/targets",
        f"{BASE_URL}/sales/forecasts",
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint in endpoints:
        if test_endpoint(endpoint):
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! ✅")
        return 0
    else:
        print("Some tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())