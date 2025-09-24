#!/usr/bin/env python3
import requests
import time

def test_endpoints():
    print('🧪 Testing Our Fixed Endpoints on Port 8001:')
    print('=' * 50)
    
    time.sleep(1)
    
    endpoints = [
        '/marketing/automation/',
        '/marketing/analytics/', 
        '/marketing/email/',
        '/support/knowledge-base/',
        '/marketing/',
        '/'
    ]
    
    success_count = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8001{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f'✅ {endpoint} - SUCCESS!')
                data = response.json()
                if 'message' in data:
                    print(f'   Message: {data["message"]}')
                success_count += 1
            else:
                print(f'❌ {endpoint} - Status: {response.status_code}')
        except Exception as e:
            print(f'❌ {endpoint} - Error: {str(e)}')
    
    print('=' * 50)
    print(f'Results: {success_count}/{len(endpoints)} endpoints working')
    
    if success_count >= 4:
        print('🎉 MAJOR SUCCESS! Most endpoints are working!')
    elif success_count >= 2:
        print('📈 Good progress!')
    else:
        print('⚠️ Need more investigation')

if __name__ == "__main__":
    test_endpoints()