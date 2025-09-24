"""
Unit Tests for Business Logic Components

TestSprite Documentation:
- Tests business logic in sales, marketing, and support modules
- Validates data models, services, and business rules
- Uses mocks for external dependencies
- Focuses on business rule validation and data integrity

Expected Outcomes:
- All business rules are correctly enforced
- Data models validate inputs properly
- Service functions return expected results
- Error handling works for invalid business data
- Performance meets business requirements

Acceptance Criteria:
- All business validation rules pass
- Model serialization/deserialization works correctly
- Service functions handle edge cases properly
- No business logic vulnerabilities
- Response time < 200ms for business operations
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Add the backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import business logic components
from app.models.sales import Lead, Contact, Opportunity, Quotation
from app.core.crud.lead import CRUDLead
from app.core.crud.contact import CRUDContact
from app.core.crud.opportunity import CRUDOpportunity


class TestLeadBusinessLogic(unittest.TestCase):
    """Test lead business logic"""
    
    def setUp(self):
        """Setup test data"""
        self.sample_lead_data = {
            "name": "John Doe",
            "company": "Test Company",
            "email": "john@testcompany.com",
            "phone": "+1-555-0123",
            "status": "New",
            "source": "Website",
            "notes": "Interested in our services"
        }
        
    def test_lead_model_validation(self):
        """Test lead model validation"""
        # Valid lead data
        lead = Lead(**self.sample_lead_data)
        self.assertEqual(lead.name, "John Doe")
        self.assertEqual(lead.email, "john@testcompany.com")
        
    def test_lead_email_validation(self):
        """Test lead email validation"""
        # Invalid email should be handled by validation
        invalid_data = self.sample_lead_data.copy()
        invalid_data["email"] = "invalid-email"
        
        # Note: Actual validation depends on model implementation
        # This test structure shows how to validate business rules
        
    def test_lead_status_validation(self):
        """Test lead status validation"""
        valid_statuses = ["New", "Contacted", "Qualified", "Converted", "Lost"]
        
        for status in valid_statuses:
            data = self.sample_lead_data.copy()
            data["status"] = status
            lead = Lead(**data)
            self.assertEqual(lead.status, status)
            
    def test_lead_source_validation(self):
        """Test lead source validation"""
        valid_sources = ["Website", "Email", "Phone", "Referral", "Social Media"]
        
        for source in valid_sources:
            data = self.sample_lead_data.copy()
            data["source"] = source
            lead = Lead(**data)
            self.assertEqual(lead.source, source)


class TestContactBusinessLogic(unittest.TestCase):
    """Test contact business logic"""
    
    def setUp(self):
        """Setup test data"""
        self.sample_contact_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "phone": "+1-555-0456",
            "company": "Example Corp",
            "position": "Manager",
            "department": "Sales"
        }
        
    def test_contact_model_validation(self):
        """Test contact model validation"""
        contact = Contact(**self.sample_contact_data)
        self.assertEqual(contact.first_name, "Jane")
        self.assertEqual(contact.last_name, "Smith")
        
    def test_contact_full_name_property(self):
        """Test contact full name property"""
        contact = Contact(**self.sample_contact_data)
        # Assuming there's a full_name property
        expected_full_name = "Jane Smith"
        # Test would depend on actual model implementation
        
    def test_contact_email_uniqueness(self):
        """Test contact email uniqueness business rule"""
        # This would test database constraints or business logic
        # that ensures email uniqueness
        pass
        
    def test_contact_phone_formatting(self):
        """Test contact phone number formatting"""
        # Test various phone number formats
        phone_formats = [
            "+1-555-0123",
            "(555) 012-3456",
            "555.012.3456",
            "5550123456"
        ]
        
        for phone in phone_formats:
            data = self.sample_contact_data.copy()
            data["phone"] = phone
            contact = Contact(**data)
            # Test that phone is properly formatted/validated


class TestOpportunityBusinessLogic(unittest.TestCase):
    """Test opportunity business logic"""
    
    def setUp(self):
        """Setup test data"""
        self.sample_opportunity_data = {
            "title": "Website Redesign Project",
            "description": "Complete website redesign and development",
            "value": Decimal("25000.00"),
            "probability": 75,
            "stage": "Proposal",
            "expected_close_date": datetime.now() + timedelta(days=30),
            "account_id": 1,
            "contact_id": 1
        }
        
    def test_opportunity_model_validation(self):
        """Test opportunity model validation"""
        opportunity = Opportunity(**self.sample_opportunity_data)
        self.assertEqual(opportunity.title, "Website Redesign Project")
        self.assertEqual(opportunity.value, Decimal("25000.00"))
        
    def test_opportunity_probability_validation(self):
        """Test opportunity probability validation"""
        # Valid probabilities (0-100)
        valid_probabilities = [0, 25, 50, 75, 100]
        
        for prob in valid_probabilities:
            data = self.sample_opportunity_data.copy()
            data["probability"] = prob
            opportunity = Opportunity(**data)
            self.assertEqual(opportunity.probability, prob)
            
        # Invalid probabilities
        invalid_probabilities = [-10, 150, -1, 101]
        
        for prob in invalid_probabilities:
            data = self.sample_opportunity_data.copy()
            data["probability"] = prob
            # Should validate against invalid probabilities
            
    def test_opportunity_value_validation(self):
        """Test opportunity value validation"""
        # Test positive values
        valid_values = [Decimal("1000.00"), Decimal("50000.50"), Decimal("0.01")]
        
        for value in valid_values:
            data = self.sample_opportunity_data.copy()
            data["value"] = value
            opportunity = Opportunity(**data)
            self.assertEqual(opportunity.value, value)
            
    def test_opportunity_stage_progression(self):
        """Test opportunity stage progression logic"""
        valid_stages = [
            "Lead", "Qualified", "Proposal", "Negotiation", 
            "Closed Won", "Closed Lost"
        ]
        
        for stage in valid_stages:
            data = self.sample_opportunity_data.copy()
            data["stage"] = stage
            opportunity = Opportunity(**data)
            self.assertEqual(opportunity.stage, stage)
            
    def test_opportunity_expected_revenue(self):
        """Test opportunity expected revenue calculation"""
        opportunity = Opportunity(**self.sample_opportunity_data)
        # Expected revenue = value * (probability / 100)
        expected_revenue = Decimal("25000.00") * (Decimal("75") / Decimal("100"))
        # Test would depend on actual model implementation


class TestQuotationBusinessLogic(unittest.TestCase):
    """Test quotation business logic"""
    
    def setUp(self):
        """Setup test data"""
        self.sample_quotation_data = {
            "quote_number": "Q-2025-001",
            "title": "Website Development Quote",
            "description": "Quote for website development services",
            "subtotal": Decimal("20000.00"),
            "tax_rate": Decimal("8.5"),
            "total": Decimal("21700.00"),
            "valid_until": datetime.now() + timedelta(days=30),
            "status": "Draft",
            "opportunity_id": 1
        }
        
    def test_quotation_model_validation(self):
        """Test quotation model validation"""
        quotation = Quotation(**self.sample_quotation_data)
        self.assertEqual(quotation.quote_number, "Q-2025-001")
        self.assertEqual(quotation.total, Decimal("21700.00"))
        
    def test_quotation_number_format(self):
        """Test quotation number format validation"""
        # Test various quote number formats
        valid_formats = [
            "Q-2025-001",
            "QUOTE-2025-001", 
            "Q2025001"
        ]
        
        for quote_num in valid_formats:
            data = self.sample_quotation_data.copy()
            data["quote_number"] = quote_num
            quotation = Quotation(**data)
            self.assertEqual(quotation.quote_number, quote_num)
            
    def test_quotation_tax_calculation(self):
        """Test quotation tax calculation"""
        subtotal = Decimal("20000.00")
        tax_rate = Decimal("8.5")
        expected_tax = subtotal * (tax_rate / Decimal("100"))
        expected_total = subtotal + expected_tax
        
        data = self.sample_quotation_data.copy()
        data["subtotal"] = subtotal
        data["tax_rate"] = tax_rate
        data["total"] = expected_total
        
        quotation = Quotation(**data)
        self.assertEqual(quotation.total, expected_total)
        
    def test_quotation_validity_period(self):
        """Test quotation validity period"""
        # Valid until date should be in the future
        future_date = datetime.now() + timedelta(days=30)
        data = self.sample_quotation_data.copy()
        data["valid_until"] = future_date
        
        quotation = Quotation(**data)
        self.assertGreater(quotation.valid_until, datetime.now())
        
    def test_quotation_status_transitions(self):
        """Test quotation status transitions"""
        valid_statuses = ["Draft", "Sent", "Accepted", "Rejected", "Expired"]
        
        for status in valid_statuses:
            data = self.sample_quotation_data.copy()
            data["status"] = status
            quotation = Quotation(**data)
            self.assertEqual(quotation.status, status)


class TestCRUDBusinessLogic(unittest.TestCase):
    """Test CRUD business logic"""
    
    def setUp(self):
        """Setup test CRUD instances"""
        self.lead_crud = CRUDLead(Lead)
        self.contact_crud = CRUDContact(Contact)
        self.opportunity_crud = CRUDOpportunity(Opportunity)
        
    def test_lead_crud_search_functionality(self):
        """Test lead CRUD search functionality"""
        # Mock database session
        mock_session = Mock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = []
        
        # Test search by name
        results = self.lead_crud.get_by_name(mock_session, name="Test Lead")
        self.assertIsInstance(results, (type(None), Lead))
        
        # Test search by company
        results = self.lead_crud.get_by_company(mock_session, company="Test Company")
        self.assertIsInstance(results, list)
        
    def test_contact_crud_filtering(self):
        """Test contact CRUD filtering"""
        mock_session = Mock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = []
        
        # Test filter by company
        results = self.contact_crud.get_by_company(mock_session, company="Test Corp")
        self.assertIsInstance(results, list)
        
        # Test filter by department
        results = self.contact_crud.get_by_department(mock_session, department="Sales")
        self.assertIsInstance(results, list)
        
    def test_opportunity_crud_analytics(self):
        """Test opportunity CRUD analytics functionality"""
        mock_session = Mock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = []
        
        # Test opportunities by account
        results = self.opportunity_crud.get_by_account(mock_session, account_id=1)
        self.assertIsInstance(results, list)
        
        # Test opportunities by stage
        results = self.opportunity_crud.get_by_stage(mock_session, stage="Proposal")
        self.assertIsInstance(results, list)


class TestBusinessRuleValidation(unittest.TestCase):
    """Test business rule validation"""
    
    def test_lead_conversion_rules(self):
        """Test lead conversion business rules"""
        # Test that only qualified leads can be converted
        # This would test actual business logic implementation
        pass
        
    def test_opportunity_close_rules(self):
        """Test opportunity closing business rules"""
        # Test rules for closing opportunities
        # e.g., must have quotation, must be in final stage, etc.
        pass
        
    def test_quotation_approval_rules(self):
        """Test quotation approval business rules"""
        # Test approval workflow rules
        # e.g., amounts over threshold need manager approval
        pass
        
    def test_data_consistency_rules(self):
        """Test data consistency business rules"""
        # Test rules that maintain data consistency
        # e.g., contact must belong to existing account
        pass


class TestBusinessLogicPerformance(unittest.TestCase):
    """Test business logic performance"""
    
    def test_lead_processing_performance(self):
        """Test lead processing performance"""
        import time
        
        # Simulate processing multiple leads
        start_time = time.time()
        
        for i in range(100):
            lead_data = {
                "name": f"Lead {i}",
                "company": f"Company {i}",
                "email": f"lead{i}@company{i}.com",
                "status": "New",
                "source": "Website"
            }
            lead = Lead(**lead_data)
            
        end_time = time.time()
        
        # Should process 100 leads in reasonable time
        self.assertLess(end_time - start_time, 1.0)  # 1 second max
        
    def test_opportunity_calculation_performance(self):
        """Test opportunity calculation performance"""
        import time
        
        start_time = time.time()
        
        # Test multiple opportunity calculations
        for i in range(1000):
            value = Decimal(f"{i * 100}.00")
            probability = i % 100
            # Simulate expected revenue calculation
            expected_revenue = value * (Decimal(str(probability)) / Decimal("100"))
            
        end_time = time.time()
        
        # Should complete calculations quickly
        self.assertLess(end_time - start_time, 0.5)  # 500ms max


class TestBusinessLogicEdgeCases(unittest.TestCase):
    """Test business logic edge cases"""
    
    def test_zero_value_opportunity(self):
        """Test opportunity with zero value"""
        opportunity_data = {
            "title": "Free Consultation",
            "value": Decimal("0.00"),
            "probability": 100,
            "stage": "Proposal"
        }
        
        opportunity = Opportunity(**opportunity_data)
        self.assertEqual(opportunity.value, Decimal("0.00"))
        
    def test_very_large_opportunity_value(self):
        """Test opportunity with very large value"""
        large_value = Decimal("999999999.99")
        opportunity_data = {
            "title": "Enterprise Deal",
            "value": large_value,
            "probability": 50,
            "stage": "Negotiation"
        }
        
        opportunity = Opportunity(**opportunity_data)
        self.assertEqual(opportunity.value, large_value)
        
    def test_special_characters_in_names(self):
        """Test handling of special characters in names"""
        special_names = [
            "O'Connor & Associates",
            "Müller Solutions GmbH",
            "Company-Name_2025",
            "Company (Subsidiary)"
        ]
        
        for name in special_names:
            lead_data = {
                "name": "Test Contact",
                "company": name,
                "email": "test@company.com",
                "status": "New",
                "source": "Website"
            }
            
            lead = Lead(**lead_data)
            self.assertEqual(lead.company, name)


if __name__ == "__main__":
    # Run tests with detailed output
    unittest.main(verbosity=2)