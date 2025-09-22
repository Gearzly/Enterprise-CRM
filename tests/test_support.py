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

def main():
    """Test all Support module endpoints"""
    print("Testing Support module endpoints...\n")
    
    # Test each submodule
    tick_passed, tick_total = test_support_tickets()
    kb_passed, kb_total = test_support_knowledge_base()
    inter_passed, inter_total = test_support_interactions()
    
    # Calculate overall results
    passed = tick_passed + kb_passed + inter_passed
    total = tick_total + kb_total + inter_total
    
    print(f"\nSupport Module Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All Support tests passed! ✅")
        return 0
    else:
        print("Some Support tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())