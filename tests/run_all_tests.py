#!/usr/bin/env python3
"""
Main test runner for the Enterprise CRM System
"""
import sys
import subprocess
import os

def run_test_script(script_name):
    """Run a test script and return the result"""
    try:
        print(f"\n{'='*60}")
        print(f"Running {script_name}")
        print('='*60)
        
        # Change to the tests directory
        tests_dir = os.path.join(os.path.dirname(__file__))
        result = subprocess.run([sys.executable, os.path.join(tests_dir, script_name)], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False

def main():
    """Run all test suites"""
    print("Enterprise CRM System - Test Runner")
    print("="*60)
    
    test_scripts = [
        "test_superadmin.py",
        "test_sales.py",
        "test_marketing.py",
        "test_support.py",
        "test_integration.py"
    ]
    
    passed_tests = 0
    total_tests = len(test_scripts)
    
    for script in test_scripts:
        if run_test_script(script):
            passed_tests += 1
        else:
            print(f"⚠️  {script} failed or encountered issues")
    
    print("\n" + "="*60)
    print("FINAL TEST RESULTS")
    print("="*60)
    print(f"Passed: {passed_tests}/{total_tests} test suites")
    
    if passed_tests == total_tests:
        print("🎉 All test suites completed successfully! ✅")
        return 0
    else:
        print("❌ Some test suites failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())