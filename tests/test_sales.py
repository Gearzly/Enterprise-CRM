#!/usr/bin/env python3
"""
Test suite for the Sales module
"""
import requests
import sys
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/sales"

def test_sales_activities():
    """Test Sales Activities endpoints"""
    print("Testing Sales Activities endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/activities",
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
    
    print(f"Sales Activities: {passed}/{total} tests passed\n")
    return passed, total

def test_sales_contacts():
    """Test Sales Contacts endpoints"""
    print("Testing Sales Contacts endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/contacts",
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
    
    print(f"Sales Contacts: {passed}/{total} tests passed\n")
    return passed, total

def test_sales_leads():
    """Test Sales Leads endpoints"""
    print("Testing Sales Leads endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/leads",
        f"{BASE_URL}{API_PREFIX}/leads/config/statuses",
        f"{BASE_URL}{API_PREFIX}/leads/config/sources",
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
    
    print(f"Sales Leads: {passed}/{total} tests passed\n")
    return passed, total

def test_sales_opportunities():
    """Test Sales Opportunities endpoints"""
    print("Testing Sales Opportunities endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/opportunities",
        f"{BASE_URL}{API_PREFIX}/opportunities/config/stages",
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
    
    print(f"Sales Opportunities: {passed}/{total} tests passed\n")
    return passed, total

def test_sales_quotations():
    """Test Sales Quotations endpoints"""
    print("Testing Sales Quotations endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/quotations",
        f"{BASE_URL}{API_PREFIX}/quotations/config/statuses",
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
    
    print(f"Sales Quotations: {passed}/{total} tests passed\n")
    return passed, total

def test_sales_reports():
    """Test Sales Reports endpoints"""
    print("Testing Sales Reports endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/reports/sales",
        f"{BASE_URL}{API_PREFIX}/reports/sales/metrics",
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
    
    print(f"Sales Reports: {passed}/{total} tests passed\n")
    return passed, total

def test_sales_targets():
    """Test Sales Targets endpoints"""
    print("Testing Sales Targets endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/targets",
        f"{BASE_URL}{API_PREFIX}/forecasts",
        f"{BASE_URL}{API_PREFIX}/config/forecast_factors",
        f"{BASE_URL}{API_PREFIX}/config/target_periods",
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
    
    print(f"Sales Targets: {passed}/{total} tests passed\n")
    return passed, total

def main():
    """Test all Sales module endpoints"""
    print("Testing Sales module endpoints...\n")
    
    # Test each submodule
    act_passed, act_total = test_sales_activities()
    con_passed, con_total = test_sales_contacts()
    lead_passed, lead_total = test_sales_leads()
    opp_passed, opp_total = test_sales_opportunities()
    quo_passed, quo_total = test_sales_quotations()
    rep_passed, rep_total = test_sales_reports()
    tar_passed, tar_total = test_sales_targets()
    
    # Calculate overall results
    passed = act_passed + con_passed + lead_passed + opp_passed + quo_passed + rep_passed + tar_passed
    total = act_total + con_total + lead_total + opp_total + quo_total + rep_total + tar_total
    
    print(f"\nSales Module Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All Sales tests passed! ✅")
        return 0
    else:
        print("Some Sales tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())