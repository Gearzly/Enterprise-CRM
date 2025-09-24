"""
Comprehensive test suite for Security and Compliance API endpoints
"""
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.core.database import engine, SessionLocal
from app.models.compliance import DataRetentionPolicy, DeletionRequest, ConsentTemplate, ConsentRecord
from app.models.audit import AuditLog
from app.models.data_classification import DataClassification, DataLabel
from app.models.security import SecretConfig, CertificateConfig, KeyRotationConfig
import json

# Test client setup
client = TestClient(app)

class TestComplianceEndpoints:
    """Test GDPR/HIPAA Compliance endpoints"""
    
    def test_create_data_retention_policy(self):
        """Test creating a data retention policy"""
        policy_data = {
            "name": "Customer Data Retention",
            "description": "Retention policy for customer personal data",
            "data_type": "customer_data",
            "retention_period_days": 2555,  # 7 years
            "jurisdiction": "EU",
            "legal_basis": "GDPR Article 6(1)(b)",
            "is_active": True
        }
        
        response = client.post("/api/compliance/retention/policies", json=policy_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == policy_data["name"]
        assert data["retention_period_days"] == policy_data["retention_period_days"]
        return data["id"]
    
    def test_get_retention_policies(self):
        """Test retrieving all retention policies"""
        response = client.get("/api/compliance/retention/policies")
        assert response.status_code == 200
        policies = response.json()
        assert isinstance(policies, list)
    
    def test_create_deletion_request(self):
        """Test creating a data deletion request"""
        deletion_data = {
            "user_id": "user123",
            "email": "user@example.com",
            "data_types": ["personal_info", "transaction_history"],
            "reason": "User requested account deletion",
            "requested_by": "user123"
        }
        
        response = client.post("/api/compliance/deletion/requests", json=deletion_data)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == deletion_data["user_id"]
        assert data["status"] == "pending"
        return data["id"]
    
    def test_get_deletion_requests(self):
        """Test retrieving deletion requests"""
        response = client.get("/api/compliance/deletion/requests")
        assert response.status_code == 200
        requests = response.json()
        assert isinstance(requests, list)
    
    def test_create_consent_template(self):
        """Test creating a consent template"""
        template_data = {
            "name": "Marketing Communications",
            "description": "Consent for marketing emails and newsletters",
            "purpose": "marketing",
            "legal_basis": "GDPR Article 6(1)(a)",
            "data_types": ["email", "preferences"],
            "retention_period": "24 months",
            "is_active": True
        }
        
        response = client.post("/api/compliance/consent/templates", json=template_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == template_data["name"]
        assert data["purpose"] == template_data["purpose"]
        return data["id"]
    
    def test_create_consent_record(self):
        """Test creating a consent record"""
        template_id = self.test_create_consent_template()
        
        consent_data = {
            "user_id": "user123",
            "template_id": template_id,
            "consent_given": True,
            "consent_method": "web_form",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 Test Browser"
        }
        
        response = client.post("/api/compliance/consent/records", json=consent_data)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == consent_data["user_id"]
        assert data["consent_given"] == consent_data["consent_given"]

class TestSecurityEndpoints:
    """Test OWASP Security endpoints"""
    
    def test_validate_input(self):
        """Test input validation endpoint"""
        test_data = {
            "input_data": "Valid test input <script>alert('xss')</script>",
            "input_type": "text"
        }
        
        response = client.post("/api/security/validate-input", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "sanitized_input" in data
        assert "<script>" not in data["sanitized_input"]
    
    def test_security_headers(self):
        """Test that security headers are properly set"""
        response = client.get("/")
        headers = response.headers
        
        # Check for OWASP security headers
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        assert "X-XSS-Protection" in headers
        assert "Strict-Transport-Security" in headers
        assert "Content-Security-Policy" in headers
    
    def test_rate_limiting_info(self):
        """Test rate limiting configuration endpoint"""
        response = client.get("/api/security/rate-limits")
        assert response.status_code == 200
        data = response.json()
        assert "limits" in data
    
    def test_security_config(self):
        """Test security configuration endpoint"""
        response = client.get("/api/security/config")
        assert response.status_code == 200
        data = response.json()
        assert "csp_policy" in data
        assert "security_headers" in data

class TestAuditLoggingEndpoints:
    """Test Audit Logging endpoints"""
    
    def test_create_audit_log(self):
        """Test creating an audit log entry"""
        log_data = {
            "action": "user_login",
            "resource_type": "user",
            "resource_id": "user123",
            "user_id": "user123",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 Test Browser",
            "additional_data": {"login_method": "password"}
        }
        
        response = client.post("/api/audit/logs", json=log_data)
        assert response.status_code == 200
        data = response.json()
        assert data["action"] == log_data["action"]
        assert data["user_id"] == log_data["user_id"]
        return data["id"]
    
    def test_get_audit_logs(self):
        """Test retrieving audit logs"""
        response = client.get("/api/audit/logs")
        assert response.status_code == 200
        logs = response.json()
        assert isinstance(logs, list)
    
    def test_search_audit_logs(self):
        """Test searching audit logs"""
        # Create a test log first
        self.test_create_audit_log()
        
        response = client.get("/api/audit/logs/search?action=user_login")
        assert response.status_code == 200
        logs = response.json()
        assert isinstance(logs, list)
    
    def test_verify_log_integrity(self):
        """Test log integrity verification"""
        log_id = self.test_create_audit_log()
        
        response = client.get(f"/api/audit/logs/{log_id}/verify")
        assert response.status_code == 200
        data = response.json()
        assert "is_valid" in data

class TestDataClassificationEndpoints:
    """Test Data Classification endpoints"""
    
    def test_create_data_classification(self):
        """Test creating a data classification"""
        classification_data = {
            "name": "Personal Identifiable Information",
            "description": "Data that can identify an individual",
            "level": "HIGH",
            "handling_requirements": ["encryption", "access_control", "audit_logging"],
            "retention_period": "7 years",
            "access_controls": ["authenticated_users", "data_protection_officer"]
        }
        
        response = client.post("/api/data/classifications", json=classification_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == classification_data["name"]
        assert data["level"] == classification_data["level"]
        return data["id"]
    
    def test_get_classifications(self):
        """Test retrieving data classifications"""
        response = client.get("/api/data/classifications")
        assert response.status_code == 200
        classifications = response.json()
        assert isinstance(classifications, list)
    
    def test_create_data_label(self):
        """Test creating a data label"""
        classification_id = self.test_create_data_classification()
        
        label_data = {
            "resource_type": "user",
            "resource_id": "user123",
            "classification_id": classification_id,
            "applied_by": "admin",
            "metadata": {"source": "user_registration"}
        }
        
        response = client.post("/api/data/labels", json=label_data)
        assert response.status_code == 200
        data = response.json()
        assert data["resource_type"] == label_data["resource_type"]
        assert data["classification_id"] == classification_id
    
    def test_check_access_permission(self):
        """Test checking data access permissions"""
        response = client.post("/api/data/check-access", json={
            "user_id": "user123",
            "resource_type": "user",
            "resource_id": "user123",
            "action": "read"
        })
        assert response.status_code == 200
        data = response.json()
        assert "allowed" in data

class TestProductionSecurityEndpoints:
    """Test Production Security endpoints"""
    
    def test_create_secret_config(self):
        """Test creating a secret configuration"""
        secret_data = {
            "name": "database_password",
            "description": "Database connection password",
            "environment": "production",
            "secret_type": "password",
            "rotation_enabled": True,
            "rotation_interval_days": 90
        }
        
        response = client.post("/api/security/secrets", json=secret_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == secret_data["name"]
        assert data["rotation_enabled"] == secret_data["rotation_enabled"]
        return data["id"]
    
    def test_get_secret_configs(self):
        """Test retrieving secret configurations"""
        response = client.get("/api/security/secrets")
        assert response.status_code == 200
        secrets = response.json()
        assert isinstance(secrets, list)
    
    def test_create_certificate_config(self):
        """Test creating a certificate configuration"""
        cert_data = {
            "name": "api_ssl_cert",
            "description": "SSL certificate for API endpoints",
            "certificate_type": "SSL",
            "environment": "production",
            "auto_renewal": True,
            "notification_days": 30
        }
        
        response = client.post("/api/security/certificates", json=cert_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == cert_data["name"]
        assert data["auto_renewal"] == cert_data["auto_renewal"]
        return data["id"]
    
    def test_get_certificate_configs(self):
        """Test retrieving certificate configurations"""
        response = client.get("/api/security/certificates")
        assert response.status_code == 200
        certificates = response.json()
        assert isinstance(certificates, list)
    
    def test_create_key_rotation_config(self):
        """Test creating a key rotation configuration"""
        rotation_data = {
            "name": "api_encryption_key",
            "description": "Encryption key for API data",
            "key_type": "AES256",
            "rotation_interval_days": 180,
            "auto_rotation": True,
            "backup_count": 3
        }
        
        response = client.post("/api/security/key-rotation", json=rotation_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == rotation_data["name"]
        assert data["auto_rotation"] == rotation_data["auto_rotation"]
        return data["id"]
    
    def test_get_key_rotation_configs(self):
        """Test retrieving key rotation configurations"""
        response = client.get("/api/security/key-rotation")
        assert response.status_code == 200
        configs = response.json()
        assert isinstance(configs, list)

class TestIntegrationScenarios:
    """Test integration scenarios across multiple endpoints"""
    
    def test_complete_data_lifecycle(self):
        """Test complete data lifecycle with classification, audit, and compliance"""
        # 1. Create data classification
        classification_data = {
            "name": "Test PII Data",
            "description": "Test personal data",
            "level": "HIGH",
            "handling_requirements": ["encryption", "audit_logging"],
            "retention_period": "5 years",
            "access_controls": ["authenticated_users"]
        }
        
        response = client.post("/api/data/classifications", json=classification_data)
        assert response.status_code == 200
        classification_id = response.json()["id"]
        
        # 2. Create audit log for data creation
        log_data = {
            "action": "data_create",
            "resource_type": "customer",
            "resource_id": "customer123",
            "user_id": "admin",
            "ip_address": "192.168.1.1",
            "user_agent": "Test Agent",
            "additional_data": {"classification_id": classification_id}
        }
        
        response = client.post("/api/audit/logs", json=log_data)
        assert response.status_code == 200
        
        # 3. Apply data label
        label_data = {
            "resource_type": "customer",
            "resource_id": "customer123",
            "classification_id": classification_id,
            "applied_by": "admin",
            "metadata": {"lifecycle_test": True}
        }
        
        response = client.post("/api/data/labels", json=label_data)
        assert response.status_code == 200
        
        # 4. Check access permissions
        response = client.post("/api/data/check-access", json={
            "user_id": "admin",
            "resource_type": "customer",
            "resource_id": "customer123",
            "action": "read"
        })
        assert response.status_code == 200
        assert response.json()["allowed"] is True
    
    def test_compliance_workflow(self):
        """Test complete compliance workflow"""
        # 1. Create retention policy
        policy_data = {
            "name": "Test Data Policy",
            "description": "Test retention policy",
            "data_type": "test_data",
            "retention_period_days": 365,
            "jurisdiction": "US",
            "legal_basis": "Business requirement",
            "is_active": True
        }
        
        response = client.post("/api/compliance/retention/policies", json=policy_data)
        assert response.status_code == 200
        
        # 2. Create consent template
        template_data = {
            "name": "Test Consent",
            "description": "Test consent template",
            "purpose": "testing",
            "legal_basis": "GDPR Article 6(1)(a)",
            "data_types": ["test_data"],
            "retention_period": "12 months",
            "is_active": True
        }
        
        response = client.post("/api/compliance/consent/templates", json=template_data)
        assert response.status_code == 200
        template_id = response.json()["id"]
        
        # 3. Record consent
        consent_data = {
            "user_id": "testuser123",
            "template_id": template_id,
            "consent_given": True,
            "consent_method": "api_test",
            "ip_address": "192.168.1.1",
            "user_agent": "Test Agent"
        }
        
        response = client.post("/api/compliance/consent/records", json=consent_data)
        assert response.status_code == 200
        
        # 4. Create deletion request
        deletion_data = {
            "user_id": "testuser123",
            "email": "testuser@example.com",
            "data_types": ["test_data"],
            "reason": "User requested deletion",
            "requested_by": "testuser123"
        }
        
        response = client.post("/api/compliance/deletion/requests", json=deletion_data)
        assert response.status_code == 200

# Test runner function
def run_security_compliance_tests():
    """Run all security and compliance tests"""
    import subprocess
    import sys
    
    try:
        # Run pytest on this specific test file
        result = subprocess.run([
            sys.executable, "-m", "pytest", __file__, "-v", "--tb=short"
        ], capture_output=True, text=True, cwd="d:/CRM")
        
        print("Test Results:")
        print("=" * 50)
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    run_security_compliance_tests()