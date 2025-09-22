#!/usr/bin/env python3
"""
Test suite for the Marketing module
"""
import requests
import sys
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/marketing"

def test_marketing_campaigns():
    """Test Marketing Campaigns endpoints"""
    print("Testing Marketing Campaigns endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/campaigns/",
        f"{BASE_URL}{API_PREFIX}/campaigns/templates",
        f"{BASE_URL}{API_PREFIX}/campaigns/ab-tests",
        f"{BASE_URL}{API_PREFIX}/campaigns/config/statuses",
        f"{BASE_URL}{API_PREFIX}/campaigns/config/types",
        f"{BASE_URL}{API_PREFIX}/campaigns/config/ab-test-metrics",
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
    
    print(f"Marketing Campaigns: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_leads():
    """Test Marketing Leads endpoints"""
    print("Testing Marketing Leads endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/leads/",
        f"{BASE_URL}{API_PREFIX}/leads/config/statuses",
        f"{BASE_URL}{API_PREFIX}/leads/config/sources",
        f"{BASE_URL}{API_PREFIX}/leads/config/score-rule-types",
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
    
    print(f"Marketing Leads: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_email():
    """Test Marketing Email endpoints"""
    print("Testing Marketing Email endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/email/",
        f"{BASE_URL}{API_PREFIX}/email/config/statuses",
        f"{BASE_URL}{API_PREFIX}/email/config/template-categories",
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
    
    print(f"Marketing Email: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_social_media():
    """Test Marketing Social Media endpoints"""
    print("Testing Marketing Social Media endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/social-media/",
        f"{BASE_URL}{API_PREFIX}/social-media/config/platforms",
        f"{BASE_URL}{API_PREFIX}/social-media/config/post-statuses",
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
    
    print(f"Marketing Social Media: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_content():
    """Test Marketing Content endpoints"""
    print("Testing Marketing Content endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/content/",
        f"{BASE_URL}{API_PREFIX}/content/config/statuses",
        f"{BASE_URL}{API_PREFIX}/content/config/types",
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
    
    print(f"Marketing Content: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_analytics():
    """Test Marketing Analytics endpoints"""
    print("Testing Marketing Analytics endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/analytics/",
        f"{BASE_URL}{API_PREFIX}/analytics/config/report-types",
        f"{BASE_URL}{API_PREFIX}/analytics/config/attribution-models",
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
    
    print(f"Marketing Analytics: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_automation():
    """Test Marketing Automation endpoints"""
    print("Testing Marketing Automation endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/automation/",
        f"{BASE_URL}{API_PREFIX}/automation/config/workflow-statuses",
        f"{BASE_URL}{API_PREFIX}/automation/config/trigger-types",
        f"{BASE_URL}{API_PREFIX}/automation/config/action-types",
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
    
    print(f"Marketing Automation: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_segmentation():
    """Test Marketing Segmentation endpoints"""
    print("Testing Marketing Segmentation endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/segmentation/",
        f"{BASE_URL}{API_PREFIX}/segmentation/config/segment-types",
        f"{BASE_URL}{API_PREFIX}/segmentation/config/criteria-types",
        f"{BASE_URL}{API_PREFIX}/segmentation/config/logical-operators",
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
    
    print(f"Marketing Segmentation: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_events():
    """Test Marketing Events endpoints"""
    print("Testing Marketing Events endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/events/",
        f"{BASE_URL}{API_PREFIX}/events/config/statuses",
        f"{BASE_URL}{API_PREFIX}/events/config/types",
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
    
    print(f"Marketing Events: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_partners():
    """Test Marketing Partners endpoints"""
    print("Testing Marketing Partners endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/partners/",
        f"{BASE_URL}{API_PREFIX}/partners/config/statuses",
        f"{BASE_URL}{API_PREFIX}/partners/config/types",
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
    
    print(f"Marketing Partners: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_resources():
    """Test Marketing Resources endpoints"""
    print("Testing Marketing Resources endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/resources/",
        f"{BASE_URL}{API_PREFIX}/resources/config/statuses",
        f"{BASE_URL}{API_PREFIX}/resources/config/categories",
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
    
    print(f"Marketing Resources: {passed}/{total} tests passed\n")
    return passed, total

def test_marketing_cdp():
    """Test Marketing CDP endpoints"""
    print("Testing Marketing CDP endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/cdp/",
        f"{BASE_URL}{API_PREFIX}/cdp/config/data-source-types",
        f"{BASE_URL}{API_PREFIX}/cdp/config/identity-resolution-statuses",
        f"{BASE_URL}{API_PREFIX}/cdp/config/sync-frequencies",
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
    
    print(f"Marketing CDP: {passed}/{total} tests passed\n")
    return passed, total

def main():
    """Test all Marketing module endpoints"""
    print("Testing Marketing module endpoints...\n")
    
    # Test each submodule
    camp_passed, camp_total = test_marketing_campaigns()
    lead_passed, lead_total = test_marketing_leads()
    email_passed, email_total = test_marketing_email()
    sm_passed, sm_total = test_marketing_social_media()
    cont_passed, cont_total = test_marketing_content()
    anal_passed, anal_total = test_marketing_analytics()
    auto_passed, auto_total = test_marketing_automation()
    seg_passed, seg_total = test_marketing_segmentation()
    event_passed, event_total = test_marketing_events()
    part_passed, part_total = test_marketing_partners()
    res_passed, res_total = test_marketing_resources()
    cdp_passed, cdp_total = test_marketing_cdp()
    
    # Calculate overall results
    passed = (camp_passed + lead_passed + email_passed + sm_passed + cont_passed + 
              anal_passed + auto_passed + seg_passed + event_passed + part_passed + 
              res_passed + cdp_passed)
    total = (camp_total + lead_total + email_total + sm_total + cont_total + 
             anal_total + auto_total + seg_total + event_total + part_total + 
             res_total + cdp_total)
    
    print(f"\nMarketing Module Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All Marketing tests passed! ✅")
        return 0
    else:
        print("Some Marketing tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())