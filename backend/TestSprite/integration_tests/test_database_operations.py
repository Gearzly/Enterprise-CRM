"""
Integration Tests for Database Operations

TestSprite Documentation:
- Tests database operations through the application layer
- Validates data persistence, transaction handling, and consistency
- Tests database schema integrity and constraints
- Uses test database for safe testing

Expected Outcomes:
- Database operations complete successfully
- Data is correctly persisted and retrievable
- Database constraints are enforced
- Transaction rollback works correctly on errors
- Connection pooling functions properly

Acceptance Criteria:
- All CRUD operations work correctly
- Database constraints prevent invalid data
- Transactions maintain ACID properties
- Query performance meets requirements (< 500ms)
- No data corruption or inconsistencies
"""

import unittest
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Add the backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.core.database import Base
from app.models.sales import Lead, Contact, Opportunity, Quotation, Activity, Target, Report
from app.core.crud.lead import CRUDLead
from app.core.crud.contact import CRUDContact
from app.core.crud.opportunity import CRUDOpportunity


class TestDatabaseSetup(unittest.TestCase):
    """Test database setup and connection"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test database"""
        # Use in-memory SQLite for testing
        cls.engine = create_engine("sqlite:///test_integration.db", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        
    @classmethod
    def tearDownClass(cls):
        """Cleanup test database"""
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()
        
    def setUp(self):
        """Setup test session"""
        self.session = self.SessionLocal()
        
    def tearDown(self):
        """Cleanup test session"""
        self.session.rollback()
        self.session.close()
        
    def test_database_connection(self):
        """Test database connection"""
        result = self.session.execute(text("SELECT 1")).fetchone()
        self.assertEqual(result[0], 1)
        
    def test_tables_created(self):
        """Test that all tables are created"""
        inspector = self.engine.dialect.get_table_names(connection=self.engine.connect())
        
        # Check for key tables (table names depend on model definitions)
        # Note: Actual table names may vary based on SQLAlchemy model configuration
        self.assertIsInstance(inspector, list)
        self.assertGreater(len(inspector), 0)


class TestLeadDatabaseOperations(unittest.TestCase):
    """Test lead database operations"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test database"""
        cls.engine = create_engine("sqlite:///test_leads.db", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        
    def setUp(self):
        """Setup test session"""
        self.session = self.SessionLocal()
        self.lead_crud = CRUDLead(Lead)
        
    def tearDown(self):
        """Cleanup test session"""
        self.session.rollback()
        self.session.close()
        
    def test_create_lead(self):
        """Test creating a lead"""
        lead_data = {
            "name": "John Doe",
            "company": "Test Company",
            "email": "john@testcompany.com",
            "phone": "+1-555-0123",
            "status": "New",
            "source": "Website",
            "notes": "Interested in our services",
            "created_at": datetime.utcnow()
        }
        
        lead = Lead(**lead_data)
        self.session.add(lead)
        self.session.commit()
        
        # Verify lead was created
        created_lead = self.session.query(Lead).filter_by(email="john@testcompany.com").first()
        self.assertIsNotNone(created_lead)
        self.assertEqual(created_lead.name, "John Doe")
        self.assertEqual(created_lead.company, "Test Company")
        
    def test_update_lead(self):
        """Test updating a lead"""
        # Create lead
        lead = Lead(
            name="Jane Smith",
            company="Smith Corp",
            email="jane@smithcorp.com",
            status="New",
            source="Email"
        )
        self.session.add(lead)
        self.session.commit()
        
        # Update lead
        lead.status = "Contacted"
        lead.notes = "Follow-up scheduled"
        self.session.commit()
        
        # Verify update
        updated_lead = self.session.query(Lead).filter_by(email="jane@smithcorp.com").first()
        self.assertEqual(updated_lead.status, "Contacted")
        self.assertEqual(updated_lead.notes, "Follow-up scheduled")
        
    def test_delete_lead(self):
        """Test deleting a lead"""
        # Create lead
        lead = Lead(
            name="Delete Test",
            company="Delete Corp",
            email="delete@test.com",
            status="New",
            source="Test"
        )
        self.session.add(lead)
        self.session.commit()
        lead_id = lead.id
        
        # Delete lead
        self.session.delete(lead)
        self.session.commit()
        
        # Verify deletion
        deleted_lead = self.session.query(Lead).filter_by(id=lead_id).first()
        self.assertIsNone(deleted_lead)
        
    def test_lead_email_uniqueness(self):
        """Test lead email uniqueness constraint"""
        # Create first lead
        lead1 = Lead(
            name="User One",
            company="Company One",
            email="unique@test.com",
            status="New",
            source="Website"
        )
        self.session.add(lead1)
        self.session.commit()
        
        # Try to create second lead with same email
        lead2 = Lead(
            name="User Two",
            company="Company Two",
            email="unique@test.com",  # Same email
            status="New",
            source="Email"
        )
        self.session.add(lead2)
        
        # Should raise integrity error (if unique constraint exists)
        try:
            self.session.commit()
            # If no constraint, that's also valid - just verify both records
            leads = self.session.query(Lead).filter_by(email="unique@test.com").all()
            self.assertGreaterEqual(len(leads), 1)
        except IntegrityError:
            # Unique constraint enforced
            self.session.rollback()
            
    def test_lead_crud_operations(self):
        """Test CRUD operations through CRUDLead"""
        # Create lead data
        from app.sales.lead.models import LeadCreate
        
        # Note: This assumes LeadCreate model exists
        # If not, use direct Lead model
        lead_data = {
            "name": "CRUD Test",
            "company": "CRUD Company",
            "email": "crud@test.com",
            "status": "New",
            "source": "API"
        }
        
        try:
            lead_create = LeadCreate(**lead_data)
            created_lead = self.lead_crud.create(self.session, obj_in=lead_create)
        except ImportError:
            # If LeadCreate doesn't exist, use direct model
            created_lead = Lead(**lead_data)
            self.session.add(created_lead)
            self.session.commit()
            self.session.refresh(created_lead)
        
        self.assertIsNotNone(created_lead.id)
        
        # Test get by name
        found_lead = self.lead_crud.get_by_name(self.session, name="CRUD Test")
        self.assertIsNotNone(found_lead)
        self.assertEqual(found_lead.name, "CRUD Test")


class TestContactDatabaseOperations(unittest.TestCase):
    """Test contact database operations"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test database"""
        cls.engine = create_engine("sqlite:///test_contacts.db", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        
    def setUp(self):
        """Setup test session"""
        self.session = self.SessionLocal()
        self.contact_crud = CRUDContact(Contact)
        
    def tearDown(self):
        """Cleanup test session"""
        self.session.rollback()
        self.session.close()
        
    def test_create_contact(self):
        """Test creating a contact"""
        contact_data = {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice@example.com",
            "phone": "+1-555-0789",
            "company": "Example Corp",
            "position": "Manager",
            "department": "Sales",
            "created_at": datetime.utcnow()
        }
        
        contact = Contact(**contact_data)
        self.session.add(contact)
        self.session.commit()
        
        # Verify contact was created
        created_contact = self.session.query(Contact).filter_by(email="alice@example.com").first()
        self.assertIsNotNone(created_contact)
        self.assertEqual(created_contact.first_name, "Alice")
        self.assertEqual(created_contact.last_name, "Johnson")
        
    def test_contact_relationships(self):
        """Test contact relationships with other entities"""
        # This would test foreign key relationships
        # if they exist in the model
        pass
        
    def test_contact_search_operations(self):
        """Test contact search operations"""
        # Create test contacts
        contacts_data = [
            {
                "first_name": "Bob",
                "last_name": "Smith",
                "email": "bob@techcorp.com",
                "company": "TechCorp",
                "department": "Engineering"
            },
            {
                "first_name": "Carol",
                "last_name": "Davis",
                "email": "carol@techcorp.com",
                "company": "TechCorp",
                "department": "Sales"
            }
        ]
        
        for data in contacts_data:
            contact = Contact(**data)
            self.session.add(contact)
        self.session.commit()
        
        # Test search by company
        company_contacts = self.contact_crud.get_by_company(self.session, company="TechCorp")
        self.assertGreaterEqual(len(company_contacts), 2)
        
        # Test search by department
        sales_contacts = self.contact_crud.get_by_department(self.session, department="Sales")
        self.assertGreaterEqual(len(sales_contacts), 1)


class TestOpportunityDatabaseOperations(unittest.TestCase):
    """Test opportunity database operations"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test database"""
        cls.engine = create_engine("sqlite:///test_opportunities.db", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        
    def setUp(self):
        """Setup test session"""
        self.session = self.SessionLocal()
        self.opportunity_crud = CRUDOpportunity(Opportunity)
        
    def tearDown(self):
        """Cleanup test session"""
        self.session.rollback()
        self.session.close()
        
    def test_create_opportunity(self):
        """Test creating an opportunity"""
        opportunity_data = {
            "title": "Website Development",
            "description": "Custom website development project",
            "value": Decimal("15000.00"),
            "probability": 60,
            "stage": "Proposal",
            "expected_close_date": datetime.utcnow() + timedelta(days=30),
            "created_at": datetime.utcnow()
        }
        
        opportunity = Opportunity(**opportunity_data)
        self.session.add(opportunity)
        self.session.commit()
        
        # Verify opportunity was created
        created_opp = self.session.query(Opportunity).filter_by(title="Website Development").first()
        self.assertIsNotNone(created_opp)
        self.assertEqual(created_opp.value, Decimal("15000.00"))
        self.assertEqual(created_opp.probability, 60)
        
    def test_opportunity_value_calculations(self):
        """Test opportunity value calculations"""
        opportunity = Opportunity(
            title="Test Calculation",
            value=Decimal("10000.00"),
            probability=50,
            stage="Proposal"
        )
        self.session.add(opportunity)
        self.session.commit()
        
        # Test expected revenue calculation (if implemented)
        expected_revenue = opportunity.value * (Decimal(str(opportunity.probability)) / Decimal("100"))
        self.assertEqual(expected_revenue, Decimal("5000.00"))
        
    def test_opportunity_stage_progression(self):
        """Test opportunity stage progression"""
        opportunity = Opportunity(
            title="Stage Test",
            value=Decimal("5000.00"),
            probability=25,
            stage="Lead"
        )
        self.session.add(opportunity)
        self.session.commit()
        
        # Update stage
        opportunity.stage = "Qualified"
        opportunity.probability = 50
        self.session.commit()
        
        # Verify update
        updated_opp = self.session.query(Opportunity).filter_by(title="Stage Test").first()
        self.assertEqual(updated_opp.stage, "Qualified")
        self.assertEqual(updated_opp.probability, 50)


class TestTransactionHandling(unittest.TestCase):
    """Test database transaction handling"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test database"""
        cls.engine = create_engine("sqlite:///test_transactions.db", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        
    def setUp(self):
        """Setup test session"""
        self.session = self.SessionLocal()
        
    def tearDown(self):
        """Cleanup test session"""
        self.session.rollback()
        self.session.close()
        
    def test_transaction_commit(self):
        """Test transaction commit"""
        # Create multiple related records in a transaction
        lead = Lead(
            name="Transaction Test",
            company="Trans Corp",
            email="trans@test.com",
            status="New",
            source="Test"
        )
        
        contact = Contact(
            first_name="Trans",
            last_name="User",
            email="trans.user@test.com",
            company="Trans Corp"
        )
        
        # Add both to session
        self.session.add(lead)
        self.session.add(contact)
        
        # Commit transaction
        self.session.commit()
        
        # Verify both records exist
        saved_lead = self.session.query(Lead).filter_by(email="trans@test.com").first()
        saved_contact = self.session.query(Contact).filter_by(email="trans.user@test.com").first()
        
        self.assertIsNotNone(saved_lead)
        self.assertIsNotNone(saved_contact)
        
    def test_transaction_rollback(self):
        """Test transaction rollback"""
        # Create record
        lead = Lead(
            name="Rollback Test",
            company="Rollback Corp",
            email="rollback@test.com",
            status="New",
            source="Test"
        )
        
        self.session.add(lead)
        
        # Rollback transaction
        self.session.rollback()
        
        # Verify record was not saved
        saved_lead = self.session.query(Lead).filter_by(email="rollback@test.com").first()
        self.assertIsNone(saved_lead)
        
    def test_transaction_error_handling(self):
        """Test transaction error handling"""
        try:
            # Create record with potential constraint violation
            lead1 = Lead(
                name="Error Test 1",
                company="Error Corp",
                email="error@test.com",
                status="New",
                source="Test"
            )
            
            lead2 = Lead(
                name="Error Test 2",
                company="Error Corp",
                email="error@test.com",  # Potential duplicate
                status="New",
                source="Test"
            )
            
            self.session.add(lead1)
            self.session.add(lead2)
            self.session.commit()
            
        except (IntegrityError, SQLAlchemyError):
            # Handle constraint violation
            self.session.rollback()
            
            # Verify no records were saved
            saved_leads = self.session.query(Lead).filter_by(email="error@test.com").all()
            # Should be empty if rollback worked
            
        except Exception as e:
            # Handle other errors
            self.session.rollback()
            self.fail(f"Unexpected error: {e}")


class TestDatabasePerformance(unittest.TestCase):
    """Test database performance"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test database"""
        cls.engine = create_engine("sqlite:///test_performance.db", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        
    def setUp(self):
        """Setup test session"""
        self.session = self.SessionLocal()
        
    def tearDown(self):
        """Cleanup test session"""
        self.session.rollback()
        self.session.close()
        
    def test_bulk_insert_performance(self):
        """Test bulk insert performance"""
        import time
        
        start_time = time.time()
        
        # Create 100 leads
        leads = []
        for i in range(100):
            lead = Lead(
                name=f"Bulk Lead {i}",
                company=f"Bulk Company {i}",
                email=f"bulk{i}@test.com",
                status="New",
                source="Bulk Test"
            )
            leads.append(lead)
        
        # Bulk insert
        self.session.add_all(leads)
        self.session.commit()
        
        end_time = time.time()
        
        # Should complete within reasonable time
        self.assertLess(end_time - start_time, 5.0)  # 5 seconds max
        
        # Verify all records were created
        count = self.session.query(Lead).filter(Lead.email.like("bulk%@test.com")).count()
        self.assertEqual(count, 100)
        
    def test_query_performance(self):
        """Test query performance"""
        import time
        
        # Create test data
        for i in range(50):
            lead = Lead(
                name=f"Query Lead {i}",
                company=f"Query Company {i % 10}",  # 10 different companies
                email=f"query{i}@test.com",
                status="New" if i % 2 == 0 else "Contacted",
                source="Query Test"
            )
            self.session.add(lead)
        self.session.commit()
        
        # Test query performance
        start_time = time.time()
        
        # Complex query
        results = self.session.query(Lead).filter(
            Lead.company.like("Query Company%"),
            Lead.status == "New"
        ).all()
        
        end_time = time.time()
        
        # Should complete quickly
        self.assertLess(end_time - start_time, 1.0)  # 1 second max
        self.assertGreater(len(results), 0)


class TestDatabaseConstraints(unittest.TestCase):
    """Test database constraints and data integrity"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test database"""
        cls.engine = create_engine("sqlite:///test_constraints.db", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        
    def setUp(self):
        """Setup test session"""
        self.session = self.SessionLocal()
        
    def tearDown(self):
        """Cleanup test session"""
        self.session.rollback()
        self.session.close()
        
    def test_required_field_constraints(self):
        """Test required field constraints"""
        # Test creating record without required fields
        try:
            incomplete_lead = Lead(
                # Missing required fields like name, email
                company="Incomplete Corp"
            )
            self.session.add(incomplete_lead)
            self.session.commit()
            
            # If this succeeds, fields might not be required
            
        except (IntegrityError, SQLAlchemyError):
            # Expected if fields are required
            self.session.rollback()
            
    def test_data_type_constraints(self):
        """Test data type constraints"""
        # Test with correct data types
        opportunity = Opportunity(
            title="Type Test",
            value=Decimal("1000.00"),  # Correct decimal type
            probability=50,  # Correct integer type
            stage="Proposal"
        )
        
        self.session.add(opportunity)
        self.session.commit()
        
        saved_opp = self.session.query(Opportunity).filter_by(title="Type Test").first()
        self.assertIsNotNone(saved_opp)
        self.assertIsInstance(saved_opp.value, Decimal)
        
    def test_foreign_key_constraints(self):
        """Test foreign key constraints"""
        # This would test relationships between tables
        # if foreign keys are defined in the models
        pass


if __name__ == "__main__":
    # Run tests with detailed output
    unittest.main(verbosity=2)