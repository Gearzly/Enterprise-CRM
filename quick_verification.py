#!/usr/bin/env python3

import requests
import time

def test_endpoints_quickly():
    """Quick endpoint verification test"""
    
    print("🎯 QUICK ROUTER VERIFICATION TEST")
    print("=" * 50)
    
    BASE_URL = 'http://localhost:8000'
    
    # Critical endpoints we fixed
    test_endpoints = [
        # Core
        ('/', 'Core API'),
        
        # Main modules
        ('/sales/', 'Sales Dashboard'),
        ('/marketing/', 'Marketing Dashboard'), 
        ('/support/', 'Support Dashboard'),
        
        # Marketing (confirmed working)
        ('/marketing/campaigns/', 'Marketing Campaigns'),
        ('/marketing/leads/', 'Marketing Leads'),
        ('/marketing/email/', 'Marketing Email'),
        ('/marketing/automation/', 'Marketing Automation'),
        
        # Support (should be working)
        ('/support/tickets/', 'Support Tickets'),
        ('/support/interactions/', 'Support Interactions'),
        ('/support/automation/', 'Support Automation'),
        ('/support/reporting/', 'Support Reporting'),
        
        # Sales (needs verification)
        ('/sales/opportunities/', 'Sales Opportunities'),
        ('/sales/leads/', 'Sales Leads'),
        ('/sales/contacts/', 'Sales Contacts'),
        ('/sales/quotations/', 'Sales Quotations'),
        ('/sales/targets/', 'Sales Targets'),
        ('/sales/reports/', 'Sales Reports')
    ]
    
    working = 0
    failed = 0
    
    for endpoint, name in test_endpoints:
        try:
            response = requests.get(f'{BASE_URL}{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f'✅ {endpoint:25} - {name} - OK')
                working += 1
            elif response.status_code == 404:
                print(f'❌ {endpoint:25} - {name} - NOT FOUND')
                failed += 1
            else:
                print(f'⚠️  {endpoint:25} - {name} - Status {response.status_code}')
                failed += 1
        except requests.exceptions.Timeout:
            print(f'⏱️  {endpoint:25} - {name} - TIMEOUT')
            failed += 1
        except Exception as e:
            print(f'💥 {endpoint:25} - {name} - ERROR: {str(e)[:30]}')
            failed += 1
    
    total = working + failed
    success_rate = (working / total * 100) if total > 0 else 0
    
    print(f'\n📊 RESULTS SUMMARY:')
    print(f'   Working: {working}')
    print(f'   Failed:  {failed}')
    print(f'   Total:   {total}')
    print(f'   Success Rate: {success_rate:.1f}%')
    
    if success_rate >= 90:
        print('🎉 EXCELLENT! Router fixes are working great!')
    elif success_rate >= 75:
        print('📈 GOOD! Most router fixes successful!')
    elif success_rate >= 50:
        print('⚠️  PARTIAL: Some issues remain...')
    else:
        print('❌ NEEDS WORK: Multiple issues detected')
    
    return working, failed

if __name__ == "__main__":
    test_endpoints_quickly()