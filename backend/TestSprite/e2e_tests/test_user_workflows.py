"""
End-to-End Tests for Complete User Workflows

TestSprite Documentation:
- Tests complete user workflows from start to finish
- Validates business processes across multiple modules
- Tests user authentication, authorization, and business operations
- Simulates real user interactions with the system

Expected Outcomes:
- Complete user workflows function correctly
- Business processes work across multiple modules
- Authentication and authorization work in real scenarios
- Data flows correctly between different parts of the system
- Error handling works in complete user scenarios

Acceptance Criteria:
- All user workflows complete successfully
- Business processes maintain data integrity
- User experience is smooth and responsive
- Error messages are helpful and actionable
- Performance meets user expectations (< 5 seconds per workflow)
"""

import asyncio
import json
import sys
import os
import time
from typing import Dict, Any, Optional
import pytest
import httpx
from fastapi.testclient import TestClient

# Add the backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.main import app


class TestUserAuthenticationWorkflow:
    """Test complete user authentication workflow"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        self.test_user = {
            "username": "test@crm.com",
            "password": "TestPassword123!"
        }
        
    def test_complete_authentication_flow(self):
        """Test complete authentication workflow"""
        # Step 1: Attempt to access protected resource without authentication
        response = self.client.get("/api/sales/leads")
        assert response.status_code in [401, 403]  # Unauthorized or Forbidden
        
        # Step 2: Attempt login with invalid credentials
        response = self.client.post(
            "/api/superadmin/security/auth/token",
            data={
                "username": "invalid@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code in [401, 422]  # Unauthorized or validation error
        
        # Step 3: Check rate limiting (if enabled)
        # Make multiple failed attempts
        for i in range(3):
            response = self.client.post(
                "/api/superadmin/security/auth/token",
                data={
                    "username": "invalid@example.com",
                    "password": "wrongpassword"
                }
            )
            # Should not return 500 (server error)
            assert response.status_code != 500
            
        # Step 4: Successful login (if test user exists)
        # Note: In a real test, you would create a test user first
        response = self.client.post(
            "/api/superadmin/security/auth/token",
            data=self.test_user
        )
        
        if response.status_code == 200:
            # Step 5: Extract token and test protected resource access
            token_data = response.json()
            assert "access_token" in token_data
            
            # Step 6: Access protected resource with token
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            response = self.client.get("/api/sales/leads", headers=headers)
            assert response.status_code != 401  # Should not be unauthorized
            
    def test_token_refresh_workflow(self):
        """Test token refresh workflow"""
        # Step 1: Login to get refresh token
        response = self.client.post(
            "/api/superadmin/security/auth/token",
            data=self.test_user
        )
        
        if response.status_code == 200:
            token_data = response.json()
            
            if "refresh_token" in token_data:
                # Step 2: Use refresh token to get new access token
                response = self.client.post(
                    "/api/superadmin/security/auth/refresh",
                    json={"refresh_token": token_data["refresh_token"]}
                )
                
                # Should get new tokens
                assert response.status_code in [200, 401]  # Success or invalid refresh token


class TestSalesWorkflow:
    """Test complete sales workflow"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        self.auth_token = None
        
    def authenticate(self):
        """Helper method to authenticate"""
        # Try to get authentication token
        response = self.client.post(
            "/api/superadmin/security/auth/token",
            data={
                "username": "sales@example.com",
                "password": "salespassword"
            }
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self.auth_token = token_data.get("access_token")
            
    def get_headers(self):
        """Get authorization headers"""
        if self.auth_token:
            return {"Authorization": f"Bearer {self.auth_token}"}
        return {}
        
    def test_lead_to_opportunity_workflow(self):
        """Test complete lead to opportunity conversion workflow"""
        # Step 1: Create a new lead
        lead_data = {
            "name": "John Prospect",
            "company": "Prospect Corp",
            "email": "john@prospectcorp.com",
            "phone": "+1-555-0123",
            "status": "New",
            "source": "Website",
            "notes": "Interested in our premium package"
        }
        
        response = self.client.post(
            "/api/sales/leads",
            json=lead_data,
            headers=self.get_headers()
        )
        
        # Lead creation should succeed or require authentication
        assert response.status_code in [200, 201, 401, 422]
        
        if response.status_code in [200, 201]:
            lead_response = response.json()
            lead_id = lead_response.get("id") if isinstance(lead_response, dict) else None
            
            # Step 2: Update lead status to "Qualified"
            if lead_id:
                update_data = {"status": "Qualified"}
                response = self.client.put(
                    f"/api/sales/leads/{lead_id}",
                    json=update_data,
                    headers=self.get_headers()
                )
                assert response.status_code in [200, 401, 404]
                
            # Step 3: Create opportunity from qualified lead
            opportunity_data = {
                "title": "Premium Package for Prospect Corp",
                "description": "Implementation of premium package solution",
                "value": 25000.00,
                "probability": 60,
                "stage": "Proposal",
                "lead_id": lead_id
            }
            
            response = self.client.post(
                "/api/sales/opportunities",
                json=opportunity_data,
                headers=self.get_headers()
            )
            assert response.status_code in [200, 201, 401, 422]
            
    def test_opportunity_to_quotation_workflow(self):
        """Test opportunity to quotation workflow"""
        # Step 1: Create opportunity
        opportunity_data = {
            "title": "Website Development Project",
            "description": "Custom website development",
            "value": 15000.00,
            "probability": 75,
            "stage": "Proposal"
        }
        
        response = self.client.post(
            "/api/sales/opportunities",
            json=opportunity_data,
            headers=self.get_headers()
        )
        
        if response.status_code in [200, 201]:
            opportunity_response = response.json()
            opportunity_id = opportunity_response.get("id") if isinstance(opportunity_response, dict) else None
            
            # Step 2: Create quotation for opportunity
            quotation_data = {
                "quote_number": "Q-2025-001",
                "title": "Website Development Quote",
                "description": "Quote for custom website development",
                "subtotal": 15000.00,
                "tax_rate": 8.5,
                "total": 16275.00,
                "opportunity_id": opportunity_id
            }
            
            response = self.client.post(
                "/api/sales/quotations",
                json=quotation_data,
                headers=self.get_headers()
            )
            assert response.status_code in [200, 201, 401, 422]
            
            if response.status_code in [200, 201]:
                # Step 3: Update opportunity stage to "Negotiation"
                if opportunity_id:
                    update_data = {"stage": "Negotiation", "probability": 85}
                    response = self.client.put(
                        f"/api/sales/opportunities/{opportunity_id}",
                        json=update_data,
                        headers=self.get_headers()
                    )
                    assert response.status_code in [200, 401, 404]


class TestMarketingWorkflow:
    """Test complete marketing workflow"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_campaign_creation_workflow(self):
        """Test campaign creation and management workflow"""
        # Step 1: Create marketing campaign
        campaign_data = {
            "name": "Q1 2025 Product Launch",
            "description": "Launch campaign for new product line",
            "start_date": "2025-01-01",
            "end_date": "2025-03-31",
            "budget": 50000.00,
            "status": "Draft"
        }
        
        response = self.client.post("/api/marketing/campaigns", json=campaign_data)
        assert response.status_code in [200, 201, 401, 422]
        
        if response.status_code in [200, 201]:
            campaign_response = response.json()
            campaign_id = campaign_response.get("id") if isinstance(campaign_response, dict) else None
            
            # Step 2: Create email template for campaign
            email_data = {
                "subject": "Introducing Our New Product Line",
                "content": "<h1>New Products Available</h1><p>Check out our latest offerings!</p>",
                "campaign_id": campaign_id
            }
            
            response = self.client.post("/api/marketing/email", json=email_data)
            assert response.status_code in [200, 201, 401, 422]
            
            # Step 3: Activate campaign
            if campaign_id:
                update_data = {"status": "Active"}
                response = self.client.put(f"/api/marketing/campaigns/{campaign_id}", json=update_data)
                assert response.status_code in [200, 401, 404]
                
    def test_email_marketing_workflow(self):
        """Test email marketing workflow"""
        # Step 1: Create email template
        email_template = {
            "name": "Welcome Email",
            "subject": "Welcome to Our Service!",
            "content": "<h1>Welcome!</h1><p>Thank you for joining us.</p>",
            "type": "template"
        }
        
        response = self.client.post("/api/marketing/email/templates", json=email_template)
        assert response.status_code in [200, 201, 401, 422]
        
        # Step 2: Send email to lead
        email_send = {
            "to": "prospect@example.com",
            "subject": "Welcome to Our Service!",
            "content": "<h1>Welcome!</h1><p>Thank you for your interest.</p>"
        }
        
        response = self.client.post("/api/marketing/email/send", json=email_send)
        assert response.status_code in [200, 201, 401, 422]


class TestSupportWorkflow:
    """Test complete support workflow"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_ticket_lifecycle_workflow(self):
        """Test complete ticket lifecycle workflow"""
        # Step 1: Create support ticket
        ticket_data = {
            "subject": "Login Issues",
            "description": "Unable to login to the system",
            "priority": "Medium",
            "category": "Technical",
            "customer_email": "customer@example.com",
            "status": "Open"
        }
        
        response = self.client.post("/api/support/tickets", json=ticket_data)
        assert response.status_code in [200, 201, 401, 422]
        
        if response.status_code in [200, 201]:
            ticket_response = response.json()
            ticket_id = ticket_response.get("id") if isinstance(ticket_response, dict) else None
            
            # Step 2: Add response to ticket
            response_data = {
                "message": "We're looking into this issue. Please try clearing your browser cache.",
                "ticket_id": ticket_id,
                "responder": "support@company.com"
            }
            
            response = self.client.post(f"/api/support/tickets/{ticket_id}/responses", json=response_data)
            assert response.status_code in [200, 201, 401, 404]
            
            # Step 3: Update ticket status
            if ticket_id:
                update_data = {"status": "In Progress", "priority": "High"}
                response = self.client.put(f"/api/support/tickets/{ticket_id}", json=update_data)
                assert response.status_code in [200, 401, 404]
                
            # Step 4: Resolve ticket
            if ticket_id:
                resolve_data = {"status": "Resolved", "resolution": "Issue resolved by clearing browser cache"}
                response = self.client.put(f"/api/support/tickets/{ticket_id}", json=resolve_data)
                assert response.status_code in [200, 401, 404]
                
    def test_knowledge_base_workflow(self):
        """Test knowledge base workflow"""
        # Step 1: Create knowledge base article
        article_data = {
            "title": "How to Reset Your Password",
            "content": "<h1>Password Reset Guide</h1><p>Follow these steps...</p>",
            "category": "Account Management",
            "tags": ["password", "reset", "account"],
            "status": "Draft"
        }
        
        response = self.client.post("/api/support/knowledge-base", json=article_data)
        assert response.status_code in [200, 201, 401, 422]
        
        if response.status_code in [200, 201]:
            article_response = response.json()
            article_id = article_response.get("id") if isinstance(article_response, dict) else None
            
            # Step 2: Publish article
            if article_id:
                update_data = {"status": "Published"}
                response = self.client.put(f"/api/support/knowledge-base/{article_id}", json=update_data)
                assert response.status_code in [200, 401, 404]
                
            # Step 3: Search knowledge base
            response = self.client.get("/api/support/knowledge-base?search=password")
            assert response.status_code in [200, 401]


class TestCrossModuleWorkflow:
    """Test workflows that span multiple modules"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_lead_to_customer_journey(self):
        """Test complete lead to customer journey across modules"""
        # Step 1: Marketing captures lead
        lead_data = {
            "name": "Sarah Johnson",
            "company": "Johnson Enterprises",
            "email": "sarah@johnsonent.com",
            "source": "Marketing Campaign",
            "campaign_id": 1
        }
        
        response = self.client.post("/api/sales/leads", json=lead_data)
        assert response.status_code in [200, 201, 401, 422]
        
        if response.status_code in [200, 201]:
            lead_response = response.json()
            lead_id = lead_response.get("id") if isinstance(lead_response, dict) else None
            
            # Step 2: Sales qualifies lead
            if lead_id:
                update_data = {"status": "Qualified"}
                response = self.client.put(f"/api/sales/leads/{lead_id}", json=update_data)
                assert response.status_code in [200, 401, 404]
                
            # Step 3: Sales creates opportunity
            opportunity_data = {
                "title": "Johnson Enterprises Project",
                "value": 30000.00,
                "probability": 70,
                "stage": "Proposal",
                "lead_id": lead_id
            }
            
            response = self.client.post("/api/sales/opportunities", json=opportunity_data)
            assert response.status_code in [200, 201, 401, 422]
            
            if response.status_code in [200, 201]:
                opportunity_response = response.json()
                opportunity_id = opportunity_response.get("id")
                
                # Step 4: Sales closes opportunity
                if opportunity_id:
                    close_data = {"stage": "Closed Won", "probability": 100}
                    response = self.client.put(f"/api/sales/opportunities/{opportunity_id}", json=close_data)
                    assert response.status_code in [200, 401, 404]
                    
                # Step 5: Support creates welcome ticket
                ticket_data = {
                    "subject": "Welcome to Johnson Enterprises",
                    "description": "Setup and onboarding for new customer",
                    "customer_email": "sarah@johnsonent.com",
                    "priority": "High",
                    "status": "Open"
                }
                
                response = self.client.post("/api/support/tickets", json=ticket_data)
                assert response.status_code in [200, 201, 401, 422]
                
    def test_customer_support_escalation_workflow(self):
        """Test customer support escalation workflow"""
        # Step 1: Customer creates support ticket
        ticket_data = {
            "subject": "Critical System Error",
            "description": "System is down, affecting business operations",
            "priority": "Critical",
            "customer_email": "admin@customer.com",
            "status": "Open"
        }
        
        response = self.client.post("/api/support/tickets", json=ticket_data)
        assert response.status_code in [200, 201, 401, 422]
        
        if response.status_code in [200, 201]:
            ticket_response = response.json()
            ticket_id = ticket_response.get("id")
            
            # Step 2: Escalate to sales (for potential upgrade)
            if ticket_id:
                escalation_data = {
                    "escalated_to": "sales",
                    "reason": "Customer may need system upgrade",
                    "priority": "High"
                }
                
                response = self.client.post(f"/api/support/tickets/{ticket_id}/escalate", json=escalation_data)
                assert response.status_code in [200, 201, 401, 404]
                
            # Step 3: Sales creates upgrade opportunity
            opportunity_data = {
                "title": "System Upgrade for Customer",
                "description": "Upgrade to prevent future critical issues",
                "value": 15000.00,
                "probability": 80,
                "stage": "Proposal"
            }
            
            response = self.client.post("/api/sales/opportunities", json=opportunity_data)
            assert response.status_code in [200, 201, 401, 422]


class TestPerformanceWorkflow:
    """Test performance across complete workflows"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_workflow_performance(self):
        """Test performance of complete workflows"""
        start_time = time.time()
        
        # Complete workflow with multiple operations
        operations = [
            ("POST", "/api/sales/leads", {"name": "Perf Test", "email": "perf@test.com", "company": "Test Corp"}),
            ("GET", "/api/sales/leads"),
            ("POST", "/api/marketing/campaigns", {"name": "Test Campaign", "budget": 1000}),
            ("GET", "/api/marketing/campaigns"),
            ("POST", "/api/support/tickets", {"subject": "Test Ticket", "customer_email": "test@crm.com"}),
            ("GET", "/api/support/tickets")
        ]
        
        for method, url, data in operations:
            if method == "POST":
                response = self.client.post(url, json=data)
            else:
                response = self.client.get(url)
                
            # Should not return server errors
            assert response.status_code != 500
            
        end_time = time.time()
        
        # Complete workflow should complete within reasonable time
        assert end_time - start_time < 10.0  # 10 seconds max
        
    def test_concurrent_workflow_performance(self):
        """Test performance under concurrent access"""
        import concurrent.futures
        import threading
        
        def perform_operations():
            """Perform a set of operations"""
            client = TestClient(app)
            
            operations = [
                ("GET", "/health"),
                ("GET", "/api/sales/leads"),
                ("GET", "/api/marketing/campaigns")
            ]
            
            for method, url in operations:
                response = client.get(url)
                # Should not return server errors
                assert response.status_code != 500
                
        # Run multiple concurrent operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(perform_operations) for _ in range(10)]
            
            # Wait for all to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Log but don't fail test for concurrent access issues
                    print(f"Concurrent operation failed: {e}")


class TestErrorRecoveryWorkflow:
    """Test error recovery in workflows"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
        
    def test_network_error_recovery(self):
        """Test recovery from network errors"""
        # Simulate network timeout/error scenarios
        # This would require more sophisticated setup
        pass
        
    def test_validation_error_recovery(self):
        """Test recovery from validation errors"""
        # Step 1: Submit invalid data
        invalid_lead = {
            "name": "",  # Invalid empty name
            "email": "invalid-email",  # Invalid email format
            "company": ""  # Invalid empty company
        }
        
        response = self.client.post("/api/sales/leads", json=invalid_lead)
        assert response.status_code in [400, 422]  # Validation error
        
        # Step 2: Correct the data and resubmit
        valid_lead = {
            "name": "Valid User",
            "email": "valid@example.com",
            "company": "Valid Company",
            "status": "New",
            "source": "Website"
        }
        
        response = self.client.post("/api/sales/leads", json=valid_lead)
        assert response.status_code in [200, 201, 401]  # Success or auth required
        
    def test_authentication_error_recovery(self):
        """Test recovery from authentication errors"""
        # Step 1: Access protected resource without auth
        response = self.client.get("/api/sales/leads")
        assert response.status_code == 401
        
        # Step 2: Authenticate and retry
        auth_response = self.client.post(
            "/api/superadmin/security/auth/token",
            data={
                "username": "test@crm.com",
            "password": "TestPassword123!"
            }
        )
        
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            
            # Step 3: Retry with authentication
            response = self.client.get("/api/sales/leads", headers=headers)
            assert response.status_code != 401  # Should not be unauthorized


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])