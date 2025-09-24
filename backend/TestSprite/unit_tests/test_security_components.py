"""
Unit Tests for Security Components

TestSprite Documentation:
- Tests individual security functions and classes in isolation
- Validates input sanitization, authentication, and encryption components
- Uses mocks for external dependencies (Redis, database)
- Focuses on security vulnerability prevention

Expected Outcomes:
- All security functions return expected results for valid inputs
- Invalid inputs are properly rejected with appropriate errors
- Encryption/decryption functions work correctly
- Password hashing and validation functions are secure
- Rate limiting logic functions correctly

Acceptance Criteria:
- 100% test coverage for critical security functions
- All edge cases and error conditions tested
- No security vulnerabilities exposed through testing
- Performance within acceptable limits (< 100ms per test)
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import pytest
from datetime import datetime, timedelta

# Add the backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import security components
from app.core.security.input_sanitization import (
    InputSanitizer, SanitizationType, SanitizedStr,
    sanitize_text_field, sanitize_email_field
)
from app.core.security.rate_limiting import (
    RateLimiter, RateLimitRule, RateLimitStrategy, RateLimitScope
)
from app.core.middleware.auth_middleware import (
    Permission, Role, ROLE_PERMISSIONS, has_permission
)
from app.core.memory.bounded_collections import (
    BoundedLRUCache, BoundedSet, BoundedList, EvictionPolicy
)


class TestInputSanitization(unittest.TestCase):
    """Test input sanitization functions"""
    
    def setUp(self):
        """Setup test data"""
        self.sanitizer = InputSanitizer()
        
    def test_sanitize_text_basic(self):
        """Test basic text sanitization"""
        # Valid text
        result = self.sanitizer.sanitize_text("Hello World")
        self.assertEqual(result, "Hello World")
        
        # Text with HTML
        result = self.sanitizer.sanitize_text("<script>alert('xss')</script>")
        self.assertNotIn("<script>", result)
        
    def test_sanitize_text_edge_cases(self):
        """Test text sanitization edge cases"""
        # Empty string
        result = self.sanitizer.sanitize_text("")
        self.assertEqual(result, "")
        
        # None input should raise error
        with self.assertRaises(ValueError):
            self.sanitizer.sanitize_text(None)
            
        # Very long string
        long_text = "A" * 10000
        result = self.sanitizer.sanitize_text(long_text, max_length=100)
        self.assertEqual(len(result), 100)
        
    def test_sanitize_html(self):
        """Test HTML sanitization"""
        # Safe HTML
        safe_html = "<p>Hello <strong>World</strong></p>"
        result = self.sanitizer.sanitize_html(safe_html)
        self.assertIn("<p>", result)
        self.assertIn("<strong>", result)
        
        # Dangerous HTML
        dangerous_html = "<script>alert('xss')</script><p>Content</p>"
        result = self.sanitizer.sanitize_html(dangerous_html)
        self.assertNotIn("<script>", result)
        self.assertIn("<p>", result)
        
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        valid_emails = [
            "test@crm.com",
            "user.name@domain.co.uk",
            "test+tag@example.org"
        ]
        for email in valid_emails:
            result = self.sanitizer.validate_email(email)
            self.assertIsInstance(result, str)
            
        # Invalid emails
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            ""
        ]
        for email in invalid_emails:
            with self.assertRaises(ValueError):
                self.sanitizer.validate_email(email)
                
    def test_validate_url(self):
        """Test URL validation"""
        # Valid URLs
        valid_urls = [
            "https://example.com",
            "http://localhost:8000",
            "https://subdomain.example.com/path"
        ]
        for url in valid_urls:
            result = self.sanitizer.validate_url(url)
            self.assertIsInstance(result, str)
            
        # Invalid URLs
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # FTP not supported
            ""
        ]
        for url in invalid_urls:
            with self.assertRaises(ValueError):
                self.sanitizer.validate_url(url)
                
    def test_detect_sql_injection(self):
        """Test SQL injection detection"""
        # Safe queries
        safe_queries = [
            "SELECT name FROM users",
            "normal search term"
        ]
        for query in safe_queries:
            result = self.sanitizer.detect_sql_injection(query)
            self.assertFalse(result)
            
        # Malicious queries
        malicious_queries = [
            "1 OR 1=1",
            "'; DROP TABLE users; --",
            "UNION SELECT password FROM users"
        ]
        for query in malicious_queries:
            result = self.sanitizer.detect_sql_injection(query)
            self.assertTrue(result)
            
    def test_sanitized_str(self):
        """Test SanitizedStr class"""
        # Text sanitization
        sanitized = SanitizedStr("<script>alert('xss')</script>", SanitizationType.TEXT)
        self.assertNotIn("<script>", sanitized)
        
        # Email sanitization
        sanitized = SanitizedStr("TEST@CRM.COM", SanitizationType.EMAIL)
        self.assertEqual(sanitized, "test@crm.com")


class TestRateLimiting(unittest.TestCase):
    """Test rate limiting functionality"""
    
    def setUp(self):
        """Setup test data"""
        self.rule = RateLimitRule(
            requests=5,
            window_seconds=60,
            strategy=RateLimitStrategy.SLIDING_WINDOW
        )
        
    @patch('app.core.security.rate_limiting.redis.from_url')
    def test_rate_limiter_creation(self, mock_redis):
        """Test rate limiter creation"""
        mock_redis.return_value.ping.return_value = True
        
        limiter = RateLimiter(self.rule, use_redis=False)
        self.assertIsInstance(limiter, RateLimiter)
        self.assertEqual(limiter.rule.requests, 5)
        
    @patch('app.core.security.rate_limiting.redis.from_url')
    def test_rate_limiting_within_limit(self, mock_redis):
        """Test requests within rate limit"""
        mock_redis.return_value.ping.return_value = True
        
        limiter = RateLimiter(self.rule, use_redis=False)
        
        # First request should be allowed
        allowed, info = limiter.check_rate_limit("test_client")
        self.assertTrue(allowed)
        self.assertIn("requests_remaining", info)
        
    @patch('app.core.security.rate_limiting.redis.from_url')
    def test_rate_limiting_exceed_limit(self, mock_redis):
        """Test requests exceeding rate limit"""
        mock_redis.return_value.ping.return_value = True
        
        # Create a very restrictive rule
        restrictive_rule = RateLimitRule(requests=1, window_seconds=60)
        limiter = RateLimiter(restrictive_rule, use_redis=False)
        
        # First request allowed
        allowed, _ = limiter.check_rate_limit("test_client")
        self.assertTrue(allowed)
        
        # Second request should be denied
        allowed, info = limiter.check_rate_limit("test_client")
        self.assertFalse(allowed)
        self.assertIn("retry_after", info)
        
    def test_rate_limit_rule_validation(self):
        """Test rate limit rule validation"""
        # Valid rule
        rule = RateLimitRule(requests=10, window_seconds=60)
        self.assertEqual(rule.requests, 10)
        self.assertEqual(rule.window_seconds, 60)
        
        # Rule with burst multiplier
        rule = RateLimitRule(requests=10, window_seconds=60, burst_multiplier=2.0)
        self.assertEqual(rule.burst_multiplier, 2.0)


class TestAuthenticationMiddleware(unittest.TestCase):
    """Test authentication middleware components"""
    
    def test_permission_enum(self):
        """Test permission enumeration"""
        self.assertIsInstance(Permission.SUPERADMIN_READ, Permission)
        self.assertIsInstance(Permission.SALES_WRITE, Permission)
        
    def test_role_enum(self):
        """Test role enumeration"""
        self.assertIsInstance(Role.SUPERADMIN, Role)
        self.assertIsInstance(Role.SALES_MANAGER, Role)
        
    def test_role_permissions_mapping(self):
        """Test role to permissions mapping"""
        # Superadmin should have all permissions
        superadmin_perms = ROLE_PERMISSIONS[Role.SUPERADMIN]
        self.assertIn(Permission.SUPERADMIN_READ, superadmin_perms)
        self.assertIn(Permission.SALES_WRITE, superadmin_perms)
        
        # Sales rep should have limited permissions
        sales_rep_perms = ROLE_PERMISSIONS[Role.SALES_REP]
        self.assertIn(Permission.SALES_READ, sales_rep_perms)
        self.assertNotIn(Permission.SUPERADMIN_DELETE, sales_rep_perms)
        
    def test_has_permission_function(self):
        """Test permission checking function"""
        # Mock user with superadmin role
        mock_user = Mock()
        mock_user.role = Role.SUPERADMIN.value
        
        # Should have superadmin permissions
        self.assertTrue(has_permission(mock_user, Permission.SUPERADMIN_READ))
        
        # Mock user with sales rep role
        mock_user.role = Role.SALES_REP.value
        
        # Should not have superadmin permissions
        self.assertFalse(has_permission(mock_user, Permission.SUPERADMIN_DELETE))


class TestBoundedCollections(unittest.TestCase):
    """Test bounded memory collections"""
    
    def test_bounded_lru_cache(self):
        """Test LRU cache functionality"""
        cache = BoundedLRUCache(max_size=3)
        
        # Add items within limit
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.size(), 3)
        
        # Add item beyond limit (should evict oldest)
        cache.put("key4", "value4")
        self.assertEqual(cache.size(), 3)
        self.assertIsNone(cache.get("key1"))  # Should be evicted
        
    def test_bounded_lru_cache_ttl(self):
        """Test LRU cache with TTL"""
        cache = BoundedLRUCache(max_size=10, ttl_seconds=1)
        
        cache.put("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        
        # Simulate TTL expiration
        import time
        time.sleep(1.1)
        self.assertIsNone(cache.get("key1"))
        
    def test_bounded_set(self):
        """Test bounded set functionality"""
        bounded_set = BoundedSet(max_size=3)
        
        # Add items within limit
        bounded_set.add("item1")
        bounded_set.add("item2")
        bounded_set.add("item3")
        
        self.assertTrue("item1" in bounded_set)
        self.assertEqual(len(bounded_set), 3)
        
        # Add item beyond limit
        bounded_set.add("item4")
        self.assertEqual(len(bounded_set), 3)
        self.assertFalse("item1" in bounded_set)  # Should be evicted
        
    def test_bounded_list(self):
        """Test bounded list functionality"""
        bounded_list = BoundedList(max_size=3)
        
        # Add items within limit
        bounded_list.append("item1")
        bounded_list.append("item2")
        bounded_list.append("item3")
        
        self.assertEqual(len(bounded_list), 3)
        
        # Add item beyond limit (circular buffer)
        bounded_list.append("item4")
        self.assertEqual(len(bounded_list), 3)
        
        # Check if items are correctly managed
        items = list(bounded_list)
        self.assertEqual(len(items), 3)
        self.assertIn("item4", items)
        
    def test_cache_stats(self):
        """Test cache statistics"""
        cache = BoundedLRUCache(max_size=10)
        
        # Initial stats
        stats = cache.get_stats()
        self.assertEqual(stats["hits"], 0)
        self.assertEqual(stats["misses"], 0)
        
        # Add and access items
        cache.put("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        
        stats = cache.get_stats()
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 1)


class TestSecurityUtilities(unittest.TestCase):
    """Test security utility functions"""
    
    def test_memory_estimation(self):
        """Test memory size estimation"""
        cache = BoundedLRUCache(max_size=10, max_memory_mb=1)
        
        # Test with different data types
        test_data = [
            "small string",
            "a much longer string with more content",
            {"key": "value", "number": 123},
            [1, 2, 3, 4, 5]
        ]
        
        for data in test_data:
            size = cache._estimate_size(data)
            self.assertIsInstance(size, int)
            self.assertGreater(size, 0)
            
    def test_error_handling(self):
        """Test error handling in security components"""
        sanitizer = InputSanitizer()
        
        # Test with invalid types
        with self.assertRaises(ValueError):
            sanitizer.sanitize_text(123)  # Not a string
            
        with self.assertRaises(ValueError):
            sanitizer.validate_email(None)  # None value


if __name__ == "__main__":
    # Run tests with detailed output
    unittest.main(verbosity=2)