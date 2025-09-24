import unittest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.sales import Lead as SalesLead
from app.models.marketing import Lead as MarketingLead, Campaign, EmailTemplate, EmailCampaign
from app.models.support import Ticket, SLA

class TestModelsDynamicDefaults(unittest.TestCase):
    
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def tearDown(self):
        self.session.close()
    
    @patch('app.models.sales.get_sales_default')
    def test_sales_lead_dynamic_defaults(self, mock_get_sales_default):
        # Mock the dynamic config to return specific values
        mock_get_sales_default.return_value = 'New'
        
        # Create a new lead without specifying status and source
        lead = SalesLead(name="Test Lead", company="Test Company")
        self.session.add(lead)
        self.session.commit()
        
        # Verify that the dynamic defaults were applied
        self.assertEqual(lead.status, 'New')
        
        # Verify that get_sales_default was called (it will be called for both status and source)
        self.assertGreaterEqual(mock_get_sales_default.call_count, 1)
    
    @patch('app.models.marketing.get_marketing_default')
    def test_marketing_lead_dynamic_defaults(self, mock_get_marketing_default):
        # Mock the dynamic config to return specific values
        mock_get_marketing_default.return_value = 'New'
        
        # Create a new marketing lead without specifying status and source
        lead = MarketingLead(name="Test Lead", company="Test Company")
        self.session.add(lead)
        self.session.commit()
        
        # Verify that the dynamic defaults were applied
        self.assertEqual(lead.status, 'New')
    
    @patch('app.models.marketing.get_marketing_default')
    def test_campaign_dynamic_defaults(self, mock_get_marketing_default):
        # Mock the dynamic config to return specific values
        mock_get_marketing_default.return_value = 'Draft'
        
        # Create a campaign without specifying status
        campaign = Campaign(name="Test Campaign", type="Email")
        self.session.add(campaign)
        
        # Create an email template - this one uses email_category
        with patch('app.models.marketing.get_marketing_default') as mock_get_email_category:
            mock_get_email_category.return_value = 'Newsletter'
            email_template = EmailTemplate(name="Test Template", subject="Test", content="<p>Test</p>")
            self.session.add(email_template)
        
        # Create an email campaign without specifying status
        email_campaign = EmailCampaign(name="Test Email Campaign", subject="Test", template_id=1, list_ids="[]")
        self.session.add(email_campaign)
        
        self.session.commit()
        
        # Verify that the dynamic defaults were applied
        self.assertEqual(campaign.status, 'Draft')
        # We can't easily test email_template.category because it uses a different mock
    
    @patch('app.models.support.get_support_default')
    def test_support_ticket_dynamic_defaults(self, mock_get_support_default):
        # Mock the dynamic config to return specific values
        mock_get_support_default.return_value = 'Medium'
        
        # Create a ticket without specifying priority, status, and channel
        ticket = Ticket(subject="Test Ticket", description="Test Description", customer_id=1, customer_email="test@example.com")
        self.session.add(ticket)
        self.session.commit()
        
        # Verify that the dynamic defaults were applied
        self.assertEqual(ticket.priority, 'Medium')
    
    @patch('app.models.support.get_support_default')
    def test_support_sla_dynamic_defaults(self, mock_get_support_default):
        # Mock the dynamic config to return specific values
        # For SLA, we need to return "Active" to make is_active True
        mock_get_support_default.return_value = 'Active'
        
        # Create an SLA without specifying is_active
        sla = SLA(name="Test SLA", description="Test Description", priority="High", response_time_hours=24, resolution_time_hours=72)
        self.session.add(sla)
        self.session.commit()
        
        # Verify that the dynamic defaults were applied
        # The SLA model uses a lambda that checks if sla_status equals "Active"
        self.assertEqual(sla.is_active, True)  # Because "Active" == "Active"

if __name__ == '__main__':
    unittest.main()