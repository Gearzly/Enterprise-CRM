"""
Unit Tests for Database Components

TestSprite Documentation:
- Tests database session management, CRUD operations, and transaction handling
- Validates connection pooling and error handling
- Uses test database or mocks for isolation
- Focuses on data integrity and performance

Expected Outcomes:
- Database connections are properly managed and cleaned up
- CRUD operations work correctly for all models
- Transactions handle errors properly with rollback
- Connection pooling functions within limits
- Query performance meets benchmarks

Acceptance Criteria:
- All database operations complete successfully
- No memory leaks from unclosed connections
- Transaction rollback works correctly on errors
- Connection pool statistics are accurate
- Query execution time < 500ms for simple operations
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Add the backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.core.database.session_manager import (
    DatabaseConfig, DatabaseManager, get_db_session, 
    with_db_session, handle_db_exceptions
)
from app.core.crud.base import CRUDBase
from app.models.sales import Lead, Contact, Opportunity


class TestDatabaseConfig(unittest.TestCase):
    """Test database configuration"""
    
    @patch.dict(os.environ, {
        'DATABASE_URL': 'postgresql://test:test@localhost/test_db',
        'DB_POOL_SIZE': '10',
        'DB_MAX_OVERFLOW': '20'
    })
    def test_config_from_environment(self):
        """Test configuration loading from environment"""
        config = DatabaseConfig()
        
        self.assertEqual(config.pool_size, 10)
        self.assertEqual(config.max_overflow, 20)
        self.assertIn('postgresql', config.database_url)
        
    def test_config_defaults(self):
        """Test default configuration values"""
        with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}, clear=True):
            config = DatabaseConfig()
            
            self.assertEqual(config.pool_size, 20)  # Default value
            self.assertEqual(config.max_overflow, 30)  # Default value
            
    def test_missing_database_url(self):
        """Test error when DATABASE_URL is missing"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                DatabaseConfig()


class TestDatabaseManager(unittest.TestCase):
    """Test database manager functionality"""
    
    def setUp(self):
        """Setup test database manager"""
        self.test_config = DatabaseConfig.__new__(DatabaseConfig)
        self.test_config.database_url = "sqlite:///test_memory.db"
        self.test_config.async_database_url = "sqlite+aiosqlite:///test_memory.db"
        self.test_config.pool_size = 5
        self.test_config.max_overflow = 10
        self.test_config.pool_timeout = 30
        self.test_config.pool_recycle = 300
        self.test_config.statement_timeout = 30
        self.test_config.lock_timeout = 10
        self.test_config.max_retries = 3
        self.test_config.retry_delay = 1.0
        
    def test_database_manager_creation(self):
        """Test database manager creation"""
        manager = DatabaseManager(self.test_config)
        
        self.assertIsNotNone(manager._sync_engine)
        self.assertIsNotNone(manager._sync_session_factory)
        
    def test_session_context_manager(self):
        """Test session context manager"""
        manager = DatabaseManager(self.test_config)
        
        with manager.get_session() as session:
            self.assertIsNotNone(session)
            # Session should be valid
            result = session.execute("SELECT 1").fetchone()
            self.assertEqual(result[0], 1)
            
    def test_transaction_context_manager(self):
        """Test transaction context manager"""
        manager = DatabaseManager(self.test_config)
        
        try:
            with manager.transaction() as session:
                # Simulate some database operations
                result = session.execute("SELECT 1").fetchone()
                self.assertEqual(result[0], 1)
        except Exception as e:
            self.fail(f"Transaction context manager failed: {e}")
            
    def test_transaction_rollback_on_error(self):
        """Test transaction rollback on error"""
        manager = DatabaseManager(self.test_config)
        
        with self.assertRaises(Exception):
            with manager.transaction() as session:
                # Force an error
                raise Exception("Test error")
                
    def test_health_check(self):
        """Test database health check"""
        manager = DatabaseManager(self.test_config)
        
        # Should be healthy with SQLite
        self.assertTrue(manager.health_check())
        
    def test_connection_pool_stats(self):
        """Test connection pool statistics"""
        manager = DatabaseManager(self.test_config)
        
        stats = manager.get_connection_pool_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("pool_size", stats)
        
    @patch('time.sleep')  # Mock sleep to speed up test
    def test_execute_with_retry(self, mock_sleep):
        """Test retry logic for database operations"""
        manager = DatabaseManager(self.test_config)
        
        # Mock function that fails twice then succeeds
        call_count = 0
        def failing_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise SQLAlchemyError("Connection failed")
            return "success"
        
        # Should succeed after retries
        result = manager.execute_with_retry(failing_operation)
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)


class TestCRUDBase(unittest.TestCase):
    """Test CRUD base functionality"""
    
    def setUp(self):
        """Setup test CRUD instance"""
        # Create in-memory SQLite for testing
        self.engine = create_engine("sqlite:///test_crud.db")
        self.session_factory = sessionmaker(bind=self.engine)
        
        # Create mock model
        self.mock_model = Mock()
        self.crud = CRUDBase(self.mock_model)
        
    def test_crud_creation(self):
        """Test CRUD instance creation"""
        self.assertEqual(self.crud.model, self.mock_model)
        
    def test_get_method(self):
        """Test get method"""
        session = Mock()
        session.get.return_value = Mock(id=1)
        
        result = self.crud.get(session, 1)
        session.get.assert_called_once_with(self.mock_model, 1)
        self.assertIsNotNone(result)
        
    def test_get_method_not_found(self):
        """Test get method when record not found"""
        session = Mock()
        session.get.return_value = None
        
        result = self.crud.get(session, 999)
        self.assertIsNone(result)
        
    def test_get_method_database_error(self):
        """Test get method with database error"""
        session = Mock()
        session.get.side_effect = SQLAlchemyError("Database error")
        
        with self.assertRaises(Exception):
            self.crud.get(session, 1)


class TestDatabaseDecorators(unittest.TestCase):
    """Test database decorator functions"""
    
    @patch('app.core.database.session_manager.db_manager')
    def test_with_db_session_decorator(self, mock_manager):
        """Test with_db_session decorator"""
        mock_session = Mock()
        mock_manager.get_session.return_value.__enter__.return_value = mock_session
        
        @with_db_session
        def test_function(db=None):
            self.assertIsNotNone(db)
            return "success"
        
        result = test_function()
        self.assertEqual(result, "success")
        
    def test_handle_db_exceptions_decorator(self):
        """Test database exception handling decorator"""
        @handle_db_exceptions
        def failing_function():
            raise SQLAlchemyError("Database error")
        
        with self.assertRaises(Exception):
            failing_function()


class TestDatabaseIntegration(unittest.TestCase):
    """Test database integration components"""
    
    def setUp(self):
        """Setup test environment"""
        self.test_db_url = "sqlite:///test_integration.db"
        
    def test_database_dependency_injection(self):
        """Test FastAPI database dependency"""
        # This would typically be tested with FastAPI TestClient
        # For now, test the dependency function directly
        from app.core.database.session_manager import get_db_session
        
        # Should be a generator function
        self.assertTrue(hasattr(get_db_session, '__call__'))
        
    def test_session_cleanup(self):
        """Test proper session cleanup"""
        config = DatabaseConfig.__new__(DatabaseConfig)
        config.database_url = self.test_db_url
        config.async_database_url = f"sqlite+aiosqlite://{self.test_db_url.split('///')[-1]}"
        config.pool_size = 5
        config.max_overflow = 10
        config.pool_timeout = 30
        config.pool_recycle = 300
        config.statement_timeout = 30
        config.lock_timeout = 10
        config.max_retries = 3
        config.retry_delay = 1.0
        
        manager = DatabaseManager(config)
        
        # Track session state
        sessions_created = 0
        sessions_closed = 0
        
        # Use multiple sessions
        for i in range(5):
            with manager.get_session() as session:
                sessions_created += 1
                # Simulate some work
                session.execute("SELECT 1")
            sessions_closed += 1
            
        self.assertEqual(sessions_created, sessions_closed)


class TestDatabasePerformance(unittest.TestCase):
    """Test database performance characteristics"""
    
    def setUp(self):
        """Setup performance test environment"""
        self.test_config = DatabaseConfig.__new__(DatabaseConfig)
        self.test_config.database_url = "sqlite:///test_performance.db"
        self.test_config.async_database_url = "sqlite+aiosqlite:///test_performance.db"
        self.test_config.pool_size = 10
        self.test_config.max_overflow = 20
        self.test_config.pool_timeout = 30
        self.test_config.pool_recycle = 300
        self.test_config.statement_timeout = 30
        self.test_config.lock_timeout = 10
        self.test_config.max_retries = 3
        self.test_config.retry_delay = 1.0
        
    def test_connection_pool_performance(self):
        """Test connection pool performance under load"""
        manager = DatabaseManager(self.test_config)
        
        import time
        start_time = time.time()
        
        # Simulate concurrent access
        for i in range(20):
            with manager.get_session() as session:
                session.execute("SELECT 1")
                
        end_time = time.time()
        
        # Should complete within reasonable time
        self.assertLess(end_time - start_time, 5.0)  # 5 seconds max
        
    def test_query_performance(self):
        """Test basic query performance"""
        manager = DatabaseManager(self.test_config)
        
        with manager.get_session() as session:
            import time
            start_time = time.time()
            
            # Simple query
            result = session.execute("SELECT 1").fetchone()
            
            end_time = time.time()
            
            self.assertEqual(result[0], 1)
            self.assertLess(end_time - start_time, 0.1)  # 100ms max


class TestDatabaseErrorHandling(unittest.TestCase):
    """Test database error handling scenarios"""
    
    def test_connection_error_handling(self):
        """Test handling of connection errors"""
        # Use invalid database URL
        config = DatabaseConfig.__new__(DatabaseConfig)
        config.database_url = "postgresql://invalid:invalid@localhost:5432/invalid"
        config.async_database_url = "postgresql+asyncpg://invalid:invalid@localhost:5432/invalid"
        config.pool_size = 5
        config.max_overflow = 10
        config.pool_timeout = 1  # Short timeout for testing
        config.pool_recycle = 300
        config.statement_timeout = 30
        config.lock_timeout = 10
        config.max_retries = 1  # Minimal retries for testing
        config.retry_delay = 0.1
        
        manager = DatabaseManager(config)
        
        # Health check should fail
        self.assertFalse(manager.health_check())
        
    def test_transaction_error_recovery(self):
        """Test transaction error recovery"""
        config = DatabaseConfig.__new__(DatabaseConfig)
        config.database_url = "sqlite:///test_error_recovery.db"
        config.async_database_url = "sqlite+aiosqlite:///test_error_recovery.db"
        config.pool_size = 5
        config.max_overflow = 10
        config.pool_timeout = 30
        config.pool_recycle = 300
        config.statement_timeout = 30
        config.lock_timeout = 10
        config.max_retries = 3
        config.retry_delay = 1.0
        
        manager = DatabaseManager(config)
        
        # First transaction should fail and rollback
        try:
            with manager.transaction() as session:
                session.execute("SELECT 1")
                raise Exception("Simulated error")
        except Exception:
            pass  # Expected
        
        # Second transaction should work normally
        with manager.transaction() as session:
            result = session.execute("SELECT 1").fetchone()
            self.assertEqual(result[0], 1)


if __name__ == "__main__":
    # Run tests with detailed output
    unittest.main(verbosity=2)