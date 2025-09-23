#!/usr/bin/env python3
"""
Test suite for the Support module
"""
import requests
import sys
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/support"

def test_support_tickets():
    """Test Support Tickets endpoints"""
    print("Testing Support Tickets endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/tickets",
        f"{BASE_URL}{API_PREFIX}/tickets/config/priorities",
        f"{BASE_URL}{API_PREFIX}/tickets/config/statuses",
        f"{BASE_URL}{API_PREFIX}/tickets/config/channels",
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
    
    print(f"Support Tickets: {passed}/{total} tests passed\n")
    return passed, total

def test_support_knowledge_base():
    """Test Support Knowledge Base endpoints"""
    print("Testing Support Knowledge Base endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/knowledge-base",
        f"{BASE_URL}{API_PREFIX}/knowledge-base/articles",
        f"{BASE_URL}{API_PREFIX}/knowledge-base/categories",
        f"{BASE_URL}{API_PREFIX}/knowledge-base/config/categories",
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
    
    print(f"Support Knowledge Base: {passed}/{total} tests passed\n")
    return passed, total

def test_support_interactions():
    """Test Support Interactions endpoints"""
    print("Testing Support Interactions endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/interactions",
        f"{BASE_URL}{API_PREFIX}/interactions/config/types",
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
    
    print(f"Support Interactions: {passed}/{total} tests passed\n")
    return passed, total

def test_support_live_chat():
    """Test Support Live Chat endpoints"""
    print("Testing Support Live Chat endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/live-chat",
        f"{BASE_URL}{API_PREFIX}/live-chat/sessions",
        f"{BASE_URL}{API_PREFIX}/live-chat/config/statuses",
        f"{BASE_URL}{API_PREFIX}/live-chat/config/priorities",
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
    
    print(f"Support Live Chat: {passed}/{total} tests passed\n")
    return passed, total

def test_support_call_center():
    """Test Support Call Center endpoints"""
    print("Testing Support Call Center endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/call-center",
        f"{BASE_URL}{API_PREFIX}/call-center/calls",
        f"{BASE_URL}{API_PREFIX}/call-center/queues",
        f"{BASE_URL}{API_PREFIX}/call-center/config/directions",
        f"{BASE_URL}{API_PREFIX}/call-center/config/statuses",
        f"{BASE_URL}{API_PREFIX}/call-center/config/priorities",
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
    
    print(f"Support Call Center: {passed}/{total} tests passed\n")
    return passed, total

def test_support_social_support():
    """Test Support Social Support endpoints"""
    print("Testing Support Social Support endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/social-support",
        f"{BASE_URL}{API_PREFIX}/social-support/inquiries",
        f"{BASE_URL}{API_PREFIX}/social-support/templates",
        f"{BASE_URL}{API_PREFIX}/social-support/config/platforms",
        f"{BASE_URL}{API_PREFIX}/social-support/config/sentiments",
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
    
    print(f"Support Social Support: {passed}/{total} tests passed\n")
    return passed, total

def test_support_feedback():
    """Test Support Feedback endpoints"""
    print("Testing Support Feedback endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/feedback",
        f"{BASE_URL}{API_PREFIX}/feedback/surveys",
        f"{BASE_URL}{API_PREFIX}/feedback/config/types",
        f"{BASE_URL}{API_PREFIX}/feedback/config/categories",
        f"{BASE_URL}{API_PREFIX}/feedback/config/statuses",
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
    
    print(f"Support Feedback: {passed}/{total} tests passed\n")
    return passed, total

def test_support_sla():
    """Test Support SLA endpoints"""
    print("Testing Support SLA endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/sla",
        f"{BASE_URL}{API_PREFIX}/sla/breaches",
        f"{BASE_URL}{API_PREFIX}/sla/config/types",
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
    
    print(f"Support SLA: {passed}/{total} tests passed\n")
    return passed, total

def test_support_asset():
    """Test Support Asset endpoints"""
    print("Testing Support Asset endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/asset",
        f"{BASE_URL}{API_PREFIX}/asset/warranties",
        f"{BASE_URL}{API_PREFIX}/asset/maintenance",
        f"{BASE_URL}{API_PREFIX}/asset/config/types",
        f"{BASE_URL}{API_PREFIX}/asset/config/statuses",
        f"{BASE_URL}{API_PREFIX}/asset/config/warranty-statuses",
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
    
    print(f"Support Asset: {passed}/{total} tests passed\n")
    return passed, total

def test_support_remote():
    """Test Support Remote endpoints"""
    print("Testing Support Remote endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/remote",
        f"{BASE_URL}{API_PREFIX}/remote/sessions",
        f"{BASE_URL}{API_PREFIX}/remote/tools",
        f"{BASE_URL}{API_PREFIX}/remote/config/session-types",
        f"{BASE_URL}{API_PREFIX}/remote/config/platforms",
        f"{BASE_URL}{API_PREFIX}/remote/config/statuses",
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
    
    print(f"Support Remote: {passed}/{total} tests passed\n")
    return passed, total

def test_support_community():
    """Test Support Community endpoints"""
    print("Testing Support Community endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/community",
        f"{BASE_URL}{API_PREFIX}/community/categories",
        f"{BASE_URL}{API_PREFIX}/community/posts",
        f"{BASE_URL}{API_PREFIX}/community/config/post-types",
        f"{BASE_URL}{API_PREFIX}/community/config/post-statuses",
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
    
    print(f"Support Community: {passed}/{total} tests passed\n")
    return passed, total

def test_support_reporting():
    """Test Support Reporting endpoints"""
    print("Testing Support Reporting endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/reporting",
        f"{BASE_URL}{API_PREFIX}/reporting/reports",
        f"{BASE_URL}{API_PREFIX}/reporting/dashboards",
        f"{BASE_URL}{API_PREFIX}/reporting/config/report-types",
        f"{BASE_URL}{API_PREFIX}/reporting/config/frequencies",
        f"{BASE_URL}{API_PREFIX}/reporting/config/statuses",
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
    
    print(f"Support Reporting: {passed}/{total} tests passed\n")
    return passed, total

def test_support_automation():
    """Test Support Automation endpoints"""
    print("Testing Support Automation endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/automation",
        f"{BASE_URL}{API_PREFIX}/automation/rules",
        f"{BASE_URL}{API_PREFIX}/automation/workflows",
        f"{BASE_URL}{API_PREFIX}/automation/config/automation-types",
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
    
    print(f"Support Automation: {passed}/{total} tests passed\n")
    return passed, total

def test_support_mobile():
    """Test Support Mobile endpoints"""
    print("Testing Support Mobile endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/mobile",
        f"{BASE_URL}{API_PREFIX}/mobile/devices",
        f"{BASE_URL}{API_PREFIX}/mobile/tickets",
        f"{BASE_URL}{API_PREFIX}/mobile/config/device-types",
        f"{BASE_URL}{API_PREFIX}/mobile/config/app-types",
        f"{BASE_URL}{API_PREFIX}/mobile/config/ticket-statuses",
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
    
    print(f"Support Mobile: {passed}/{total} tests passed\n")
    return passed, total

def test_support_integration():
    """Test Support Integration endpoints"""
    print("Testing Support Integration endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/integration",
        f"{BASE_URL}{API_PREFIX}/integration/mappings",
        f"{BASE_URL}{API_PREFIX}/integration/logs",
        f"{BASE_URL}{API_PREFIX}/integration/config/types",
        f"{BASE_URL}{API_PREFIX}/integration/config/platforms",
        f"{BASE_URL}{API_PREFIX}/integration/config/statuses",
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
    
    print(f"Support Integration: {passed}/{total} tests passed\n")
    return passed, total

def test_support_language():
    """Test Support Language endpoints"""
    print("Testing Support Language endpoints...")
    
    endpoints = [
        f"{BASE_URL}{API_PREFIX}/language",
        f"{BASE_URL}{API_PREFIX}/language/languages",
        f"{BASE_URL}{API_PREFIX}/language/ui",
        f"{BASE_URL}{API_PREFIX}/language/config/languages",
        f"{BASE_URL}{API_PREFIX}/language/config/statuses",
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
    
    print(f"Support Language: {passed}/{total} tests passed\n")
    return passed, total

def main():
    """Test all Support module endpoints"""
    print("Testing Support module endpoints...\n")
    
    # Test each submodule
    tick_passed, tick_total = test_support_tickets()
    kb_passed, kb_total = test_support_knowledge_base()
    inter_passed, inter_total = test_support_interactions()
    live_chat_passed, live_chat_total = test_support_live_chat()
    call_center_passed, call_center_total = test_support_call_center()
    social_passed, social_total = test_support_social_support()
    feedback_passed, feedback_total = test_support_feedback()
    sla_passed, sla_total = test_support_sla()
    asset_passed, asset_total = test_support_asset()
    remote_passed, remote_total = test_support_remote()
    community_passed, community_total = test_support_community()
    reporting_passed, reporting_total = test_support_reporting()
    automation_passed, automation_total = test_support_automation()
    mobile_passed, mobile_total = test_support_mobile()
    integration_passed, integration_total = test_support_integration()
    language_passed, language_total = test_support_language()
    
    # Calculate overall results
    passed = (tick_passed + kb_passed + inter_passed + live_chat_passed + 
              call_center_passed + social_passed + feedback_passed + sla_passed +
              asset_passed + remote_passed + community_passed + reporting_passed +
              automation_passed + mobile_passed + integration_passed + language_passed)
    total = (tick_total + kb_total + inter_total + live_chat_total + 
             call_center_total + social_total + feedback_total + sla_total +
             asset_total + remote_total + community_total + reporting_total +
             automation_total + mobile_total + integration_total + language_total)
    
    print(f"\nSupport Module Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All Support tests passed! ✅")
        return 0
    else:
        print("Some Support tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())