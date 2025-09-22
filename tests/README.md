# CRM System Tests

This directory contains comprehensive tests for the Enterprise CRM System.

## Test Structure

- `test_superadmin.py` - Tests for the Super Admin module
- `test_sales.py` - Tests for the Sales module
- `test_marketing.py` - Tests for the Marketing module
- `test_support.py` - Tests for the Support module
- `test_auth.py` - Tests for the Authentication system
- `test_integration.py` - Integration tests between modules
- `run_all_tests.py` - Main test runner

## Running Tests

1. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install backend dependencies:
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

3. Start the CRM backend server:
   ```bash
   cd ../backend
   python start_server.py
   ```

4. Run all tests:
   ```bash
   python run_all_tests.py
   ```

5. Run individual test suites:
   ```bash
   python test_superadmin.py
   python test_sales.py
   python test_marketing.py
   python test_support.py
   python test_auth.py
   python test_integration.py
   ```

## Test Coverage

The tests cover:

- ✅ Super Admin module endpoints
- ✅ Sales module endpoints
- ✅ Marketing module endpoints
- ✅ Support module endpoints
- ✅ Authentication system endpoints
- ✅ Integration between Super Admin and other modules
- ✅ Configuration synchronization between modules

Each test verifies that endpoints are accessible and return the expected HTTP status codes.

## Authentication System Tests

The authentication tests specifically verify:

- OAuth 2.0 token endpoints
- OpenID Connect support
- MFA (Multi-Factor Authentication) endpoints
- WebAuthn registration and authentication
- Session management
- Device fingerprinting

Note: Some authentication endpoints may return validation errors (422) when called without proper parameters, which is expected behavior.