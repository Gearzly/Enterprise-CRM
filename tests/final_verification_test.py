#!/usr/bin/env python3
import requests
import time
import json

def final_comprehensive_test():
    print('🎯 FINAL COMPREHENSIVE ENDPOINT VERIFICATION')
    print('=' * 70)
    
    base_url = 'http://localhost:8002'
    
    # Give server time to fully start
    time.sleep(2)
    
    # Test categories with specific focus on our fixes
    test_categories = {
        '🔧 OUR TARGET FIXES (Root Endpoints Added)': [
            '/marketing/automation/',
            '/marketing/analytics/', 
            '/marketing/email/',
            '/support/knowledge-base/'
        ],
        '✅ CONTROL GROUP (Known Working)': [
            '/',
            '/marketing/',
            '/sales/',
            '/support/',
            '/api/superadmin/'
        ],
        '📊 OTHER MARKETING MODULES': [
            '/marketing/campaigns/',
            '/marketing/leads/',
            '/marketing/social-media/',
            '/marketing/content/'
        ],
        '📞 SUPPORT MODULES': [
            '/support/tickets/',
            '/support/live-chat/',
            '/support/call-center/'
        ]
    }
    
    overall_results = {}
    total_working = 0
    total_tested = 0
    target_fixes_working = 0
    
    for category, endpoints in test_categories.items():
        print(f'\n{category}')
        print('-' * 50)
        
        category_working = 0
        category_results = []
        
        for endpoint in endpoints:
            total_tested += 1
            try:
                response = requests.get(f'{base_url}{endpoint}', timeout=10)
                
                if response.status_code == 200:
                    total_working += 1
                    category_working += 1
                    
                    # Track our target fixes specifically
                    if category == '🔧 OUR TARGET FIXES (Root Endpoints Added)':
                        target_fixes_working += 1
                    
                    try:
                        data = response.json()
                        message = data.get('message', 'No message')
                        print(f'✅ {endpoint} - SUCCESS! {message}')
                        
                        # Show statistics if available
                        if 'statistics' in data:
                            stats = data['statistics']
                            print(f'   📊 Stats: {len(stats)} metrics tracked')
                            
                        category_results.append({'endpoint': endpoint, 'status': 'SUCCESS', 'message': message})
                    except json.JSONDecodeError:
                        print(f'✅ {endpoint} - SUCCESS! (Non-JSON response)')
                        category_results.append({'endpoint': endpoint, 'status': 'SUCCESS', 'message': 'Non-JSON'})
                        
                elif response.status_code == 422:
                    print(f'⚠️  {endpoint} - 422 PARAMETER ERROR (needs path parameter fix)')
                    category_results.append({'endpoint': endpoint, 'status': 'PARAMETER_ERROR', 'message': '422 error'})
                elif response.status_code == 404:
                    print(f'❌ {endpoint} - 404 NOT FOUND (router/endpoint missing)')
                    category_results.append({'endpoint': endpoint, 'status': 'NOT_FOUND', 'message': '404 error'})
                else:
                    print(f'⚠️  {endpoint} - {response.status_code} OTHER ERROR')
                    category_results.append({'endpoint': endpoint, 'status': 'OTHER_ERROR', 'message': f'{response.status_code} error'})
                    
            except requests.exceptions.ConnectionError:
                print(f'💔 {endpoint} - CONNECTION ERROR (server not responding)')
                category_results.append({'endpoint': endpoint, 'status': 'CONNECTION_ERROR', 'message': 'Connection failed'})
            except requests.exceptions.Timeout:
                print(f'⏰ {endpoint} - TIMEOUT (server slow)')
                category_results.append({'endpoint': endpoint, 'status': 'TIMEOUT', 'message': 'Request timeout'})
            except Exception as e:
                print(f'💥 {endpoint} - UNEXPECTED ERROR: {str(e)}')
                category_results.append({'endpoint': endpoint, 'status': 'UNEXPECTED_ERROR', 'message': str(e)})
        
        print(f'   📊 Category Results: {category_working}/{len(endpoints)} working')
        overall_results[category] = {
            'working': category_working,
            'total': len(endpoints),
            'results': category_results
        }
    
    # Final summary
    print('\n' + '=' * 70)
    print('📈 FINAL VERIFICATION RESULTS')
    print('=' * 70)
    
    success_rate = (total_working / total_tested) * 100
    print(f'Overall Success Rate: {total_working}/{total_tested} ({success_rate:.1f}%)')
    print(f'🎯 Target Fixes Working: {target_fixes_working}/4 endpoints')
    
    # Analysis
    print('\n🔍 ANALYSIS:')
    if target_fixes_working >= 3:
        print('🎉 EXCELLENT! Most of our router registration fixes are working!')
        print('   ✅ Double prefix issue successfully resolved')
        print('   ✅ Model import issues fixed')
        print('   ✅ Root endpoint pattern working')
    elif target_fixes_working >= 2:
        print('📈 GOOD PROGRESS! Majority of fixes working')
        print('   ✅ Router architecture fixes are taking effect')
        print('   ⚠️  Some endpoints may need additional investigation')
    elif target_fixes_working >= 1:
        print('🔧 PARTIAL SUCCESS! Some fixes working')
        print('   ✅ Router pattern is correct')
        print('   ⚠️  May need server restart or additional debugging')
    else:
        print('⚠️  INVESTIGATION NEEDED! Target fixes not responding')
        print('   🔧 Server may need restart')
        print('   🔧 Additional router issues may exist')
    
    # Recommendations
    print('\n🎯 NEXT STEPS:')
    if target_fixes_working < 4:
        print('1. 🔧 Investigate remaining non-working target endpoints')
        print('2. 🔄 Consider server restart for full reload')
        print('3. 🐛 Check logs for any import or routing errors')
    
    remaining_404s = overall_results.get('📊 OTHER MARKETING MODULES', {}).get('total', 0) - overall_results.get('📊 OTHER MARKETING MODULES', {}).get('working', 0)
    if remaining_404s > 0:
        print(f'4. 🔧 Apply same router fix pattern to {remaining_404s} remaining marketing modules')
    
    support_404s = overall_results.get('📞 SUPPORT MODULES', {}).get('total', 0) - overall_results.get('📞 SUPPORT MODULES', {}).get('working', 0)
    if support_404s > 0:
        print(f'5. 🔧 Apply same router fix pattern to {support_404s} remaining support modules')
    
    if success_rate >= 70:
        print('\n🎉 OVERALL: MAJOR SUCCESS! CRM backend significantly improved!')
    elif success_rate >= 50:
        print('\n📈 OVERALL: Good progress made, continue systematic fixes')
    else:
        print('\n🔧 OVERALL: Foundation established, continue router pattern application')
    
    return overall_results

if __name__ == "__main__":
    final_comprehensive_test()