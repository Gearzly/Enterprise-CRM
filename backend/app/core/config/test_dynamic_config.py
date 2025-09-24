import unittest
from unittest.mock import patch, MagicMock
from app.core.config.dynamic_config import (
    get_sales_default, 
    get_marketing_default, 
    get_support_default,
    clear_config_cache
)

class TestDynamicConfig(unittest.TestCase):
    
    def setUp(self):
        # Clear cache before each test
        clear_config_cache()
    
    @patch('app.core.config.dynamic_config.get_config_value')
    def test_get_sales_default_returns_dynamic_value(self, mock_get_config):
        # Mock get_config_value to return a dynamic value
        mock_get_config.return_value = "Dynamic Status"
        
        # Test that we get the dynamic value
        result = get_sales_default("lead_status")
        self.assertEqual(result, "Dynamic Status")
        
        # Verify get_config_value was called with correct parameters
        mock_get_config.assert_called_once_with("sales.lead_status", None)
    
    @patch('app.core.config.dynamic_config.get_config_value')
    def test_get_sales_default_returns_default_when_no_dynamic_value(self, mock_get_config):
        # Mock get_config_value to return None
        mock_get_config.return_value = None
        
        # Test that we get the default value
        result = get_sales_default("lead_status")
        self.assertEqual(result, "New")  # Default value from the function
    
    @patch('app.core.config.dynamic_config.get_config_value')
    def test_get_marketing_default_returns_dynamic_value(self, mock_get_config):
        # Mock get_config_value to return a dynamic value
        mock_get_config.return_value = "Active"
        
        # Test that we get the dynamic value
        result = get_marketing_default("campaign_status")
        self.assertEqual(result, "Active")
        
        # Verify get_config_value was called with correct parameters
        mock_get_config.assert_called_once_with("marketing.campaign_status", None)
    
    @patch('app.core.config.dynamic_config.get_config_value')
    def test_get_support_default_returns_dynamic_value(self, mock_get_config):
        # Mock get_config_value to return a dynamic value
        mock_get_config.return_value = "High"
        
        # Test that we get the dynamic value
        result = get_support_default("ticket_priority")
        self.assertEqual(result, "High")
        
        # Verify get_config_value was called with correct parameters
        mock_get_config.assert_called_once_with("support.ticket_priority", None)

if __name__ == '__main__':
    unittest.main()