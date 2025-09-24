#!/usr/bin/env python3
"""
System-wide endpoint test for CRM backend - Port 8000
This script will test ALL endpoints and identify 404 errors for fixing
"""
import requests
import time
from typing import List, Dict, Tuple

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

def test_endpoint(endpoint: str) -> Tuple[str, int, Dict]:
    """Test a single endpoint and return status"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
        return endpoint, response.status_code, data
    except requests.exceptions.Timeout:
        return endpoint, 408, {"error": "timeout"}
    except requests.exceptions.ConnectionError:
        return endpoint, 503, {"error": "connection_error"}
    except Exception as e:
        return endpoint, 500, {"error": str(e)}

def print_test_results(endpoints: List[str], category: str):
    """Test a category of endpoints and print results"""
    print(f"\n🔍 {category}")
    print("-" * 60)
    
    working = 0
    not_found_endpoints = []
    
    for endpoint in endpoints:
        path, status, data = test_endpoint(endpoint)
        
        if status == 200:
            message = data.get('message', data.get('detail', 'Success'))
            print(f"✅ {path} - SUCCESS! {message}")
            working += 1
        elif status == 404:
            print(f"❌ {path} - 404 NOT FOUND (needs router fix)")
            not_found_endpoints.append(path)
        elif status == 422:
            print(f"⚠️  {path} - 422 UNPROCESSABLE ENTITY (parameter issue)")
        elif status == 500:
            print(f"💥 {path} - 500 INTERNAL SERVER ERROR")
        else:
            print(f"❓ {path} - Status: {status}")
    
    print(f"   📊 Category Results: {working}/{len(endpoints)} working")
    return working, not_found_endpoints

def main():
    print("🌐 SYSTEM-WIDE ENDPOINT TESTING ON PORT 8000")
    print("=" * 70)
    
    # Core endpoints
    core_endpoints = [
        "/",
        "/docs",
        "/openapi.json"
    ]
    
    # Main module endpoints
    main_module_endpoints = [
        "/sales/",
        "/marketing/", 
        "/support/",
        "/api/superadmin/"
    ]
    
    # Marketing sub-modules (our fixes and remaining)
    marketing_endpoints = [
        "/marketing/automation/",     # ✅ Fixed
        "/marketing/analytics/",      # ✅ Fixed  
        "/marketing/email/",         # ✅ Fixed
        "/marketing/campaigns/",     # ❌ Needs fix
        "/marketing/leads/",         # ❌ Needs fix
        "/marketing/social-media/",  # ❌ Needs fix
        "/marketing/content/"        # ❌ Needs fix
    ]
    
    # Support sub-modules  
    support_endpoints = [
        "/support/knowledge-base/",  # ✅ Fixed
        "/support/tickets/",         # ❌ Needs fix
        "/support/live-chat/",       # ❌ Needs fix
        "/support/call-center/",     # ❌ Needs fix
        "/support/feedback/",        # ❌ Needs fix
        "/support/sla/",            # ❌ Needs fix
        "/support/asset/"           # ❌ Needs fix
    ]
    
    # Sales sub-modules
    sales_endpoints = [
        "/sales/opportunities/",
        "/sales/leads/", 
        "/sales/accounts/",
        "/sales/contacts/",
        "/sales/quotes/",
        "/sales/orders/",
        "/sales/contracts/",
        "/sales/forecasting/",
        "/sales/territory/",
        "/sales/performance/",
        "/sales/commission/"
    ]
    
    # SuperAdmin sub-modules
    superadmin_endpoints = [
        "/api/superadmin/users/",
        "/api/superadmin/roles/",
        "/api/superadmin/permissions/",
        "/api/superadmin/audit/",
        "/api/superadmin/system/",
        "/api/superadmin/monitoring/",
        "/api/superadmin/backup/",
        "/api/superadmin/integration/",
        "/api/superadmin/configuration/",
        "/api/superadmin/security/"
    ]
    
    # Test all categories
    total_working = 0
    total_endpoints = 0
    all_404_endpoints = []
    
    categories = [
        (core_endpoints, "CORE ENDPOINTS"),
        (main_module_endpoints, "MAIN MODULE ENDPOINTS"), 
        (marketing_endpoints, "MARKETING SUB-MODULES"),
        (support_endpoints, "SUPPORT SUB-MODULES"),
        (sales_endpoints, "SALES SUB-MODULES"),
        (superadmin_endpoints, "SUPERADMIN SUB-MODULES")
    ]
    
    for endpoints, category in categories:
        working, not_found = print_test_results(endpoints, category)
        total_working += working
        total_endpoints += len(endpoints)
        all_404_endpoints.extend(not_found)
    
    # Final summary
    print("\n" + "=" * 70)
    print("📈 SYSTEM-WIDE TEST RESULTS")
    print("=" * 70)
    print(f"Overall Success Rate: {total_working}/{total_endpoints} ({total_working/total_endpoints*100:.1f}%)")
    
    if all_404_endpoints:
        print(f"\n🔧 ENDPOINTS NEEDING ROUTER FIXES ({len(all_404_endpoints)} total):")
        print("-" * 50)
        for endpoint in all_404_endpoints:
            print(f"❌ {endpoint}")
        
        print(f"\n📋 RECOMMENDED FIXES:")
        print("1. Apply the same router registration pattern we used successfully")
        print("2. Add prefix to individual router definitions") 
        print("3. Remove prefix from main router include_router calls")
        print("4. Add root endpoint (/) with dashboard data")
        print("5. Fix any missing import issues")
    else:
        print("\n🎉 ALL ENDPOINTS WORKING! No 404 fixes needed.")

if __name__ == "__main__":
    main()