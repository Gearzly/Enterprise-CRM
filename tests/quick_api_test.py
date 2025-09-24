#!/usr/bin/env python3
"""
Quick API Endpoint Test
"""
import requests
import json

base_url = 'http://localhost:8000'

def test_api():
    print('🚀 Testing CRM API Endpoints')
    print('=' * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f'{base_url}/')
        if response.status_code == 200:
            print('✅ Root endpoint: Working')
            data = response.json()
            print(f'   API Version: {data.get("version", "Unknown")}')
            print(f'   Available modules: {len(data.get("modules", {}))}')
        else:
            print(f'❌ Root endpoint: Status {response.status_code}')
    except Exception as e:
        print(f'❌ Root endpoint: Error - {e}')
        return
    
    # Test main endpoints
    endpoints = [
        ('/sales/leads?skip=0&limit=5', 'Sales Leads'),
        ('/sales/opportunities?skip=0&limit=5', 'Sales Opportunities'),
        ('/marketing/campaigns?skip=0&limit=5', 'Marketing Campaigns'),
        ('/support/tickets?skip=0&limit=5', 'Support Tickets'),
        ('/api/compliance/retention/policies', 'Retention Policies'),
        ('/api/security/rate-limits', 'Rate Limits'),
        ('/api/audit/logs?skip=0&limit=5', 'Audit Logs'),
        ('/api/data/classifications', 'Data Classifications'),
        ('/api/security/config', 'Security Config')
    ]
    
    passed = 1  # Root endpoint
    failed = 0
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'{base_url}{endpoint}')
            if response.status_code == 200:
                print(f'✅ {name}: {endpoint}')
                passed += 1
            else:
                print(f'❌ {name}: {endpoint} (Status: {response.status_code})')
                failed += 1
        except Exception as e:
            print(f'❌ {name}: {endpoint} (Error: {str(e)[:40]}...)')
            failed += 1
    
    # Test security headers
    try:
        response = requests.get(f'{base_url}/')
        headers = response.headers
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options', 
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]
        
        print('\n🛡️ Security Headers:')
        for header in security_headers:
            if header in headers:
                print(f'✅ {header}: Present')
            else:
                print(f'❌ {header}: Missing')
                
    except Exception as e:
        print(f'❌ Security headers test failed: {e}')
    
    # Test POST endpoint
    try:
        audit_data = {
            'action': 'api_test',
            'resource_type': 'test',
            'resource_id': 'test123',
            'user_id': 'testuser',
            'ip_address': '127.0.0.1',
            'user_agent': 'Test Agent'
        }
        response = requests.post(f'{base_url}/api/audit/logs', json=audit_data)
        if response.status_code == 200:
            print('\n✅ POST Audit Log Creation: Working')
            passed += 1
        else:
            print(f'\n❌ POST Audit Log Creation: Status {response.status_code}')
            failed += 1
    except Exception as e:
        print(f'\n❌ POST Audit Log Creation: Error {e}')
        failed += 1
    
    print(f'\n📊 Final Results:')
    print(f'✅ Passed: {passed}')
    print(f'❌ Failed: {failed}')
    print(f'🎯 Success Rate: {(passed/(passed+failed)*100):.1f}%')
    
    if passed >= failed * 2:
        print('🎉 API is working well!')
    else:
        print('⚠️ Some endpoints need attention')

if __name__ == '__main__':
    test_api()