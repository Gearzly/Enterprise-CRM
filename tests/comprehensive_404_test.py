#!/usr/bin/env python3

import requests
import time

def test_all_endpoints():
    """Comprehensive 404 detection test"""
    
    print("🔍 COMPREHENSIVE 404 DETECTION TEST")
    print("=" * 60)
    
    BASE_URL = 'http://localhost:8000'
    
    # All endpoints to test systematically
    endpoints = {
        'Core': [
            '/',
            '/docs',
            '/openapi.json'
        ],
        'Main Modules': [
            '/sales/',
            '/marketing/',
            '/support/',
            '/superadmin/'
        ],
        'Sales Modules': [
            '/sales/activities/',
            '/sales/contacts/',
            '/sales/leads/',
            '/sales/opportunities/',
            '/sales/quotations/',
            '/sales/reports/',
            '/sales/targets/'
        ],
        'Marketing Modules': [
            '/marketing/automation/',
            '/marketing/analytics/',
            '/marketing/email/',
            '/marketing/campaigns/',
            '/marketing/leads/',
            '/marketing/social-media/',
            '/marketing/content/',
            '/marketing/segmentation/',
            '/marketing/events/',
            '/marketing/partners/',
            '/marketing/resources/',
            '/marketing/cdp/'
        ],
        'Support Modules': [
            '/support/tickets/',
            '/support/knowledge-base/',
            '/support/interactions/',
            '/support/live-chat/',
            '/support/call-center/',
            '/support/social-support/',
            '/support/feedback/',
            '/support/sla/',
            '/support/asset/',
            '/support/remote/',
            '/support/community/',
            '/support/reporting/',
            '/support/automation/',
            '/support/mobile/',
            '/support/integration/',
            '/support/language/'
        ]
    }
    
    all_404s = []
    all_working = []
    
    for category, category_endpoints in endpoints.items():
        print(f'\n🔍 {category.upper()}')
        print('-' * 50)
        
        working = 0
        not_found = 0
        
        for endpoint in category_endpoints:
            try:
                response = requests.get(f'{BASE_URL}{endpoint}', timeout=5)
                if response.status_code == 200:
                    print(f'✅ {endpoint:30} - OK')
                    working += 1
                    all_working.append(endpoint)
                elif response.status_code == 404:
                    print(f'❌ {endpoint:30} - 404 NOT FOUND')
                    not_found += 1
                    all_404s.append(endpoint)
                else:
                    print(f'⚠️  {endpoint:30} - Status {response.status_code}')
            except requests.exceptions.Timeout:
                print(f'⏱️  {endpoint:30} - TIMEOUT')
            except Exception as e:
                print(f'💥 {endpoint:30} - ERROR: {str(e)[:20]}')
        
        total = working + not_found
        if total > 0:
            success_rate = (working / total * 100)
            print(f'   📊 Category Results: {working}/{total} working ({success_rate:.1f}%)')
    
    print(f'\n📊 FINAL SUMMARY:')
    print(f'   ✅ Working endpoints: {len(all_working)}')
    print(f'   ❌ 404 endpoints: {len(all_404s)}')
    
    if all_404s:
        print(f'\n🚨 404 ENDPOINTS TO FIX:')
        for endpoint in all_404s:
            print(f'   - {endpoint}')
    else:
        print(f'\n🎉 NO 404 ERRORS FOUND!')
    
    return all_404s, all_working

if __name__ == "__main__":
    not_found, working = test_all_endpoints()