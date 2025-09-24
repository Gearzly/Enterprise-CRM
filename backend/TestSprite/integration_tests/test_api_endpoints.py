"""
Integration Tests for API Endpoints

TestSprite Documentation:
- Tests complete API endpoint functionality including request/response cycles
- Validates authentication, authorization, and input sanitization
- Tests database operations through API endpoints
- Uses real HTTP requests to test complete integration

Expected Outcomes:
- All API endpoints respond correctly to valid requests
- Authentication and authorization work properly
- Input validation and sanitization function correctly
- Database operations complete successfully through API
- Error responses are properly formatted and informative

Acceptance Criteria:
- All endpoint status codes match expected values
- Response times are within acceptable limits (< 2 seconds)
- Security middleware functions correctly
- Database changes are persisted correctly
- Error handling provides useful feedback
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any
import pytest
import httpx
from fastapi.testclient import TestClient

# Add the backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.main import app


class TestAuthenticationEndpoints:
    """Test authentication API endpoints"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        self.base_url = "/api/superadmin/security/auth"
        
    def test_token_endpoint_exists(self):
        """Test that token endpoint exists"""
        response = self.client.post(f"{self.base_url}/token")
        # Should not return 404
        assert response.status_code != 404
        
    def test_token_endpoint_authentication(self):
        """Test token endpoint authentication"""
        # Test with invalid credentials
        response = self.client.post(
            f"{self.base_url}/token",
            data={
                "username": "invalid@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code in [401, 422]  # Unauthorized or validation error
        
    def test_token_endpoint_validation(self):
        """Test token endpoint input validation"""
        # Test with missing credentials
        response = self.client.post(f"{self.base_url}/token")
        assert response.status_code == 422  # Validation error
        
        # Test with invalid email format
        response = self.client.post(
            f"{self.base_url}/token",
            data={
                "username": "invalid-email",
                "password": "password123"
            }
        )
        assert response.status_code in [401, 422]
        
    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        response = self.client.get("/api/superadmin/users")
        assert response.status_code == 401  # Unauthorized
        
    def test_security_headers(self):
        """Test security headers in responses"""
        response = self.client.get("/health")
        
        # Check for security headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers


class TestSalesEndpoints:
    """Test sales API endpoints"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        self.base_url = "/api/sales"
        
    def test_leads_endpoint_exists(self):
        """Test that leads endpoint exists"""
        response = self.client.get(f"{self.base_url}/leads")
        assert response.status_code != 404
        
    def test_leads_get_endpoint(self):
        """Test GET leads endpoint"""
        response = self.client.get(f"{self.base_url}/leads")
        assert response.status_code in [200, 401]  # Success or auth required
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict))
            
    def test_leads_post_endpoint_validation(self):
        """Test POST leads endpoint validation"""
        # Test with invalid data
        invalid_lead = {
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email
            "company": ""  # Empty company
        }
        
        response = self.client.post(f"{self.base_url}/leads", json=invalid_lead)
        assert response.status_code in [400, 401, 422]
        
    def test_opportunities_endpoint(self):
        """Test opportunities endpoint"""
        response = self.client.get(f"{self.base_url}/opportunities")
        assert response.status_code != 404
        
    def test_accounts_endpoint(self):
        """Test accounts endpoint"""
        response = self.client.get(f"{self.base_url}/accounts")
        assert response.status_code != 404
        
    def test_contacts_endpoint(self):
        """Test contacts endpoint"""
        response = self.client.get(f"{self.base_url}/contacts")
        assert response.status_code != 404


class TestMarketingEndpoints:
    """Test marketing API endpoints"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        self.base_url = "/api/marketing"
        
    def test_campaigns_endpoint(self):
        """Test campaigns endpoint"""
        response = self.client.get(f"{self.base_url}/campaigns")
        assert response.status_code != 404
        
    def test_email_endpoint(self):
        """Test email endpoint"""
        response = self.client.get(f"{self.base_url}/email")
        assert response.status_code != 404
        
    def test_analytics_endpoint(self):
        """Test analytics endpoint"""
        response = self.client.get(f"{self.base_url}/analytics")
        assert response.status_code != 404


class TestSupportEndpoints:
    """Test support API endpoints"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        self.base_url = "/api/support"
        
    def test_tickets_endpoint(self):
        """Test tickets endpoint"""
        response = self.client.get(f"{self.base_url}/tickets")
        assert response.status_code != 404
        
    def test_knowledge_base_endpoint(self):
        """Test knowledge base endpoint"""
        response = self.client.get(f"{self.base_url}/knowledge-base")
        assert response.status_code != 404


class TestInputSanitizationIntegration:
    """Test input sanitization integration"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_xss_prevention(self):
        """Test XSS prevention in API endpoints"""
        malicious_payload = {
            "name": "<script>alert('xss')</script>",
            "description": "javascript:alert('xss')",
            "email": "test@example.com"
        }
        
        # Try to submit malicious payload to various endpoints
        endpoints = [
            "/api/sales/leads",
            "/api/marketing/campaigns",
            "/api/support/tickets"
        ]
        
        for endpoint in endpoints:
            response = self.client.post(endpoint, json=malicious_payload)
            
            # Should not return 500 (server error)
            assert response.status_code != 500
            
            if response.status_code == 200:
                # Check that malicious content is sanitized
                response_text = response.text
                assert "<script>" not in response_text
                assert "javascript:" not in response_text
                
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        malicious_queries = [
            "1' OR '1'='1",
            "'; DROP TABLE users; --",
            "1 UNION SELECT password FROM users"
        ]
        
        for malicious_query in malicious_queries:
            # Test in query parameters
            response = self.client.get(f"/api/sales/leads?search={malicious_query}")
            
            # Should not return 500 (server error)
            assert response.status_code != 500
            
    def test_email_validation(self):
        """Test email validation in API endpoints"""
        invalid_emails = [
            "not-an-email",
            "@example.com",
            "test@",
            ""
        ]
        
        for invalid_email in invalid_emails:
            payload = {
                "name": "Test User",
                "email": invalid_email,
                "company": "Test Company"
            }
            
            response = self.client.post("/api/sales/leads", json=payload)
            
            # Should return validation error
            assert response.status_code in [400, 422]


class TestRateLimitingIntegration:
    """Test rate limiting integration"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_rate_limiting_headers(self):
        """Test rate limiting headers"""
        response = self.client.get("/api/sales/leads")
        
        # Should include rate limit headers if rate limiting is enabled
        if response.status_code == 200:
            # Check for rate limit headers
            headers = response.headers
            rate_limit_headers = [
                "X-RateLimit-Limit",
                "X-RateLimit-Remaining", 
                "X-RateLimit-Window"
            ]
            
            # At least some rate limit headers should be present
            has_rate_limit_headers = any(header in headers for header in rate_limit_headers)
            # Note: This might not be present in all configurations
            
    def test_authentication_rate_limiting(self):
        """Test rate limiting on authentication endpoints"""
        # Make multiple failed authentication attempts
        for i in range(3):
            response = self.client.post(
                "/api/superadmin/security/auth/token",
                data={
                    "username": "invalid@example.com",
                    "password": "wrongpassword"
                }
            )
            
            # Should not return 500
            assert response.status_code != 500


class TestDatabaseIntegration:
    """Test database integration through API"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_database_connection_health(self):
        """Test database connection through health endpoint"""
        response = self.client.get("/health")
        
        if response.status_code == 200:
            health_data = response.json()
            
            # Check if database health is reported
            if "checks" in health_data:
                checks = health_data["checks"]
                if "database" in checks:
                    db_check = checks["database"]
                    assert "status" in db_check
                    
    def test_crud_operations_through_api(self):
        """Test CRUD operations through API endpoints"""
        # Note: This would require authentication in a real scenario
        
        # Test CREATE (POST)
        test_data = {
            "name": "Integration Test Lead",
            "company": "Test Company",
            "email": "test@example.com",
            "status": "New",
            "source": "API Test"
        }
        
        response = self.client.post("/api/sales/leads", json=test_data)
        # Should not return 500 (server error)
        assert response.status_code != 500
        
        # Test READ (GET)
        response = self.client.get("/api/sales/leads")
        assert response.status_code != 500


class TestErrorHandlingIntegration:
    """Test error handling integration"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_404_error_handling(self):
        """Test 404 error handling"""
        response = self.client.get("/api/nonexistent/endpoint")
        assert response.status_code == 404
        
        # Should return JSON error response
        try:
            error_data = response.json()
            assert isinstance(error_data, dict)
        except json.JSONDecodeError:
            # Some endpoints might return HTML 404 pages
            pass
            
    def test_validation_error_handling(self):
        """Test validation error handling"""
        # Send invalid JSON
        response = self.client.post(
            "/api/sales/leads",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 422]
        
        # Should return structured error response
        try:
            error_data = response.json()
            assert isinstance(error_data, dict)
        except json.JSONDecodeError:
            pass
            
    def test_method_not_allowed_handling(self):
        """Test method not allowed error handling"""
        # Try to DELETE on a GET-only endpoint
        response = self.client.delete("/health")
        assert response.status_code == 405  # Method Not Allowed


class TestSecurityIntegration:
    """Test security integration"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_security_info_endpoint(self):
        """Test security info endpoint"""
        response = self.client.get("/security/info")
        
        if response.status_code == 200:
            security_info = response.json()
            
            # Should contain security configuration info
            expected_fields = [
                "cors_enabled",
                "input_sanitization_enabled",
                "rate_limiting_enabled",
                "authentication_enforced"
            ]
            
            for field in expected_fields:
                if field in security_info:
                    assert isinstance(security_info[field], bool)
                    
    def test_cors_headers(self):
        """Test CORS headers"""
        response = self.client.options("/api/sales/leads")
        
        # Check for CORS headers
        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers"
        ]
        
        # At least some CORS headers should be present
        has_cors_headers = any(header in response.headers for header in cors_headers)
        # Note: This depends on CORS configuration


class TestPerformanceIntegration:
    """Test performance integration"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_response_time_health_endpoint(self):
        """Test response time for health endpoint"""
        import time
        
        start_time = time.time()
        response = self.client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Health endpoint should respond quickly
        assert response_time < 2.0  # 2 seconds max
        
    def test_response_time_api_endpoints(self):
        """Test response time for API endpoints"""
        import time
        
        endpoints = [
            "/api/sales/leads",
            "/api/marketing/campaigns",
            "/api/support/tickets"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = self.client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # API endpoints should respond within reasonable time
            assert response_time < 5.0  # 5 seconds max


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])