#!/usr/bin/env python3
import requests
import sys

def test_endpoint_fixes():
    base_url = 'http://localhost:8001'
    
    # Test endpoints we added root paths to
    endpoints = [
        '/marketing/automation/',
        '/marketing/analytics/', 
        '/support/knowledge-base/',
        '/marketing/email/'
    ]
    
    print('Testing Fixed Root Endpoints:')
    print('=' * 50)
    
    working = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'{base_url}{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f'✅ {endpoint} - WORKING')
                working += 1
            else:
                print(f'❌ {endpoint} - Status: {response.status_code}')
        except Exception as e:
            print(f'❌ {endpoint} - Error: Connection failed')
    
    print('=' * 50)
    print(f'Results: {working}/{len(endpoints)} endpoints working')
    
    if working == len(endpoints):
        print('🎉 ALL FIXES SUCCESSFUL!')
    elif working > 0:
        print(f'📈 Partial success: {working} endpoints fixed')
    else:
        print('⚠️ Fixes need more work')

if __name__ == '__main__':
    test_endpoint_fixes()