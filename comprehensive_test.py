#!/usr/bin/env python3
import requests
import time

def comprehensive_endpoint_test():
    print('🔍 COMPREHENSIVE CRM ENDPOINT TESTING')
    print('=' * 60)
    
    base_url = 'http://localhost:8001'
    
    # Test categories
    test_results = {
        'Main API & Dashboards': {
            'endpoints': ['/', '/marketing/', '/sales/', '/support/'],
            'results': []
        },
        'Our Fixed Endpoints (Root Endpoints Added)': {
            'endpoints': [
                '/marketing/automation/',  # Fixed: Added root endpoint
                '/marketing/analytics/',   # Fixed: Added root endpoint  
                '/marketing/email/',       # Fixed: Added root endpoint
                '/support/knowledge-base/' # Fixed: Added root endpoint
            ],
            'results': []
        },
        'SuperAdmin Endpoints': {
            'endpoints': [
                '/api/superadmin/',
                '/api/superadmin/organizations/',
                '/api/superadmin/settings/'
            ],
            'results': []
        },
        'Other Marketing Endpoints': {
            'endpoints': [
                '/marketing/campaigns/',
                '/marketing/leads/',
                '/marketing/social-media/',
                '/marketing/content/'
            ],
            'results': []
        },
        'Support Endpoints': {
            'endpoints': [
                '/support/tickets/',
                '/support/help-desk/',
                '/support/training/'
            ],
            'results': []
        }
    }
    
    overall_working = 0
    overall_total = 0
    newly_fixed_working = 0
    
    for category, data in test_results.items():
        print(f'\n🧪 Testing {category}:')
        print('-' * 40)
        
        category_working = 0
        
        for endpoint in data['endpoints']:
            overall_total += 1
            try:
                response = requests.get(f'{base_url}{endpoint}', timeout=5)
                
                if response.status_code == 200:
                    status_icon = '✅'
                    status_text = 'SUCCESS'
                    category_working += 1
                    overall_working += 1
                    
                    # Track newly fixed endpoints specifically
                    if category == 'Our Fixed Endpoints (Root Endpoints Added)':
                        newly_fixed_working += 1
                        
                    # Get message from response
                    try:
                        data_response = response.json()
                        message = data_response.get('message', 'No message')
                        print(f'{status_icon} {endpoint} - {status_text} - {message}')
                    except:
                        print(f'{status_icon} {endpoint} - {status_text}')
                        
                elif response.status_code == 422:
                    print(f'⚠️  {endpoint} - 422 (Parameter Error) - Needs path parameter fix')
                elif response.status_code == 404:
                    print(f'❌ {endpoint} - 404 (Not Found) - Router or endpoint missing')
                else:
                    print(f'⚠️  {endpoint} - {response.status_code} (Other Error)')
                    
                data['results'].append({
                    'endpoint': endpoint,
                    'status': response.status_code,
                    'working': response.status_code == 200
                })
                
            except requests.exceptions.ConnectionError:
                print(f'💔 {endpoint} - Connection Error (Server not responding)')
                data['results'].append({
                    'endpoint': endpoint,
                    'status': 'Connection Error',
                    'working': False
                })
            except Exception as e:
                print(f'💥 {endpoint} - Error: {str(e)}')
                data['results'].append({
                    'endpoint': endpoint,
                    'status': f'Error: {str(e)}',
                    'working': False
                })
        
        print(f'   Category Results: {category_working}/{len(data["endpoints"])} working')
    
    # Summary
    print('\n' + '=' * 60)
    print('📊 COMPREHENSIVE TEST RESULTS SUMMARY')
    print('=' * 60)
    
    print(f'Overall Success Rate: {overall_working}/{overall_total} ({(overall_working/overall_total)*100:.1f}%)')
    print(f'Our Fixed Endpoints: {newly_fixed_working}/4 working')
    
    print('\n🎯 PRIORITY ACTIONS NEEDED:')
    if newly_fixed_working >= 3:
        print('🎉 EXCELLENT! Most of our root endpoint fixes are working!')
    elif newly_fixed_working >= 2:
        print('📈 GOOD PROGRESS! Most fixes working, investigate remaining issues')
    else:
        print('⚠️  CRITICAL: Root endpoint fixes not working - deep investigation needed')
    
    # SuperAdmin analysis
    superadmin_working = sum(1 for result in test_results['SuperAdmin Endpoints']['results'] 
                           if result.get('working', False))
    if superadmin_working == 0:
        print('🔧 SuperAdmin: Fix path parameter issues (422 errors)')
    
    # Additional routers analysis
    other_working = sum(1 for result in test_results['Other Marketing Endpoints']['results'] 
                       if result.get('working', False))
    if other_working < len(test_results['Other Marketing Endpoints']['endpoints']):
        print('🔧 Marketing: Apply root endpoint pattern to remaining routers')
    
    support_working = sum(1 for result in test_results['Support Endpoints']['results'] 
                         if result.get('working', False))
    if support_working < len(test_results['Support Endpoints']['endpoints']):
        print('🔧 Support: Apply root endpoint pattern to remaining routers')

if __name__ == "__main__":
    comprehensive_endpoint_test()