#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_endpoint(url, description):
    """Test a single endpoint and return result"""
    try:
        response = requests.get(url, timeout=10)
        status = "✅ WORKING" if response.status_code == 200 else f"❌ {response.status_code}"
        return f"{status} - {url} - {description}"
    except requests.exceptions.RequestException as e:
        return f"❌ ERROR - {url} - {description} - {str(e)}"

def main():
    print("🔧 TESTING FINAL 404 FIXES")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test the three previously failing endpoints
    endpoints_to_test = [
        ("/support/social-support/", "Support Social Support"),
        ("/support/remote/", "Support Remote"),
        ("/support/community/", "Support Community"),
    ]
    
    print(f"\n📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Testing {len(endpoints_to_test)} endpoints that were previously failing...")
    
    results = []
    working_count = 0
    
    for endpoint, description in endpoints_to_test:
        url = f"{base_url}{endpoint}"
        result = test_endpoint(url, description)
        results.append(result)
        print(f"   {result}")
        
        if "✅ WORKING" in result:
            working_count += 1
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   ✅ Working: {working_count}/{len(endpoints_to_test)}")
    print(f"   ❌ Still failing: {len(endpoints_to_test) - working_count}")
    
    if working_count == len(endpoints_to_test):
        print(f"\n🎉 SUCCESS! All previously failing endpoints are now working!")
    else:
        print(f"\n⚠️  Still have {len(endpoints_to_test) - working_count} failing endpoints that need attention.")
    
    return working_count == len(endpoints_to_test)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)