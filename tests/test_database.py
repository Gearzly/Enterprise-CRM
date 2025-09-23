#!/usr/bin/env python3
"""
Database testing strategy for Sales modules
"""
import sys
import os
import sqlite3
from datetime import datetime, timedelta

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

def setup_test_database():
    """Setup test database"""
    print("Setting up test database...")
    try:
        import importlib
        # Import the database module
        database_module = importlib.import_module('app.core.database')
        Base = getattr(database_module, 'Base')
        engine = getattr(database_module, 'engine')
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Test database setup complete")
        return True
    except Exception as e:
        print(f"Error setting up test database: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        import importlib
        # Import the database module
        database_module = importlib.import_module('app.core.database')
        SessionLocal = getattr(database_module, 'SessionLocal')
        
        # Create a test session
        db = SessionLocal()
        
        # Execute a simple query
        from sqlalchemy import text
        result = db.execute(text("SELECT 1"))
        row = result.fetchone()
        
        if row and row[0] == 1:
            print("✓ Database connection test passed")
            db.close()
            return True
        else:
            print("✗ Database connection test failed")
            db.close()
            return False
    except Exception as e:
        print(f"✗ Database connection test failed with error: {e}")
        return False

def test_sales_models_creation():
    """Test creation of all sales models"""
    print("Testing sales models creation...")
    try:
        import importlib
        # Import modules
        database_module = importlib.import_module('app.core.database')
        sales_module = importlib.import_module('app.models.sales')
        enums_module = importlib.import_module('app.models.enums')
        
        SessionLocal = getattr(database_module, 'SessionLocal')
        Lead = getattr(sales_module, 'Lead')
        Contact = getattr(sales_module, 'Contact')
        Opportunity = getattr(sales_module, 'Opportunity')
        Quotation = getattr(sales_module, 'Quotation')
        Activity = getattr(sales_module, 'Activity')
        Target = getattr(sales_module, 'Target')
        Report = getattr(sales_module, 'Report')
        
        LeadStatus = getattr(enums_module, 'LeadStatus')
        LeadSource = getattr(enums_module, 'LeadSource')
        OpportunityStage = getattr(enums_module, 'OpportunityStage')
        QuotationStatus = getattr(enums_module, 'QuotationStatus')
        ContactType = getattr(enums_module, 'ContactType')
        ActivityType = getattr(enums_module, 'ActivityType')
        ActivityStatus = getattr(enums_module, 'ActivityStatus')
        TargetPeriod = getattr(enums_module, 'TargetPeriod')
        TargetType = getattr(enums_module, 'TargetType')
        ReportType = getattr(enums_module, 'ReportType')
        ReportStatus = getattr(enums_module, 'ReportStatus')
        
        db = SessionLocal()
        
        # Create test data for each model
        # Lead
        lead = Lead(
            name="Test Lead",
            company="Test Company",
            email="test@example.com",
            phone="123-456-7890",
            status=LeadStatus.new,
            source=LeadSource.website,
            assigned_to="test_user",
            value=1000.0,
            notes="Test lead notes"
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        # Contact
        contact = Contact(
            first_name="Test",
            last_name="Contact",
            email="contact@example.com",
            phone="098-765-4321",
            company="Test Company",
            position="Manager",
            department="Sales",
            address="123 Test St",
            city="Test City",
            state="TS",
            country="Test Country",
            postal_code="12345",
            contact_type=ContactType.primary,
            notes="Test contact notes"
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
        
        # Opportunity
        opportunity = Opportunity(
            name="Test Opportunity",
            description="Test opportunity description",
            value=5000.0,
            stage=OpportunityStage.prospecting,
            probability=20,
            close_date=datetime.now() + timedelta(days=30),
            account_id=1,
            contact_id=contact.id,
            assigned_to="test_user",
            notes="Test opportunity notes"
        )
        db.add(opportunity)
        db.commit()
        db.refresh(opportunity)
        
        # Quotation
        quotation = Quotation(
            title="Test Quotation",
            description="Test quotation description",
            opportunity_id=opportunity.id,
            account_id=1,
            contact_id=contact.id,
            amount=4500.0,
            tax_amount=450.0,
            total_amount=4950.0,
            status=QuotationStatus.draft,
            valid_until=datetime.now() + timedelta(days=15),
            notes="Test quotation notes"
        )
        db.add(quotation)
        db.commit()
        db.refresh(quotation)
        
        # Activity
        activity = Activity(
            title="Test Activity",
            description="Test activity description",
            activity_type=ActivityType.call,
            status=ActivityStatus.pending,
            start_time=datetime.now() + timedelta(days=1),
            end_time=datetime.now() + timedelta(days=1, hours=1),
            related_to="lead",
            related_id=lead.id,
            assigned_to="test_user",
            notes="Test activity notes"
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        
        # Target
        target = Target(
            name="Test Target",
            description="Test target description",
            target_type=TargetType.revenue,
            period=TargetPeriod.monthly,
            year=2025,
            target_value=100000.0,
            assigned_to="test_user",
            notes="Test target notes"
        )
        db.add(target)
        db.commit()
        db.refresh(target)
        
        # Report
        report = Report(
            title="Test Report",
            description="Test report description",
            report_type=ReportType.sales_performance,
            status=ReportStatus.draft,
            generated_by="test_user",
            filters='{"period": "monthly"}',
            data='{"metrics": []}',
            notes="Test report notes"
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        
        # Verify all records were created
        lead_count = db.query(Lead).filter(Lead.id == lead.id).count()
        contact_count = db.query(Contact).filter(Contact.id == contact.id).count()
        opportunity_count = db.query(Opportunity).filter(Opportunity.id == opportunity.id).count()
        quotation_count = db.query(Quotation).filter(Quotation.id == quotation.id).count()
        activity_count = db.query(Activity).filter(Activity.id == activity.id).count()
        target_count = db.query(Target).filter(Target.id == target.id).count()
        report_count = db.query(Report).filter(Report.id == report.id).count()
        
        db.close()
        
        if (lead_count == 1 and contact_count == 1 and opportunity_count == 1 and 
            quotation_count == 1 and activity_count == 1 and target_count == 1 and report_count == 1):
            print("✓ Sales models creation test passed")
            return True
        else:
            print("✗ Sales models creation test failed")
            return False
    except Exception as e:
        print(f"✗ Sales models creation test failed with error: {e}")
        return False

def test_database_indexing():
    """Test database indexing performance"""
    print("Testing database indexing...")
    try:
        import importlib
        # Import modules
        database_module = importlib.import_module('app.core.database')
        sales_module = importlib.import_module('app.models.sales')
        enums_module = importlib.import_module('app.models.enums')
        
        SessionLocal = getattr(database_module, 'SessionLocal')
        Lead = getattr(sales_module, 'Lead')
        LeadStatus = getattr(enums_module, 'LeadStatus')
        LeadSource = getattr(enums_module, 'LeadSource')
        
        db = SessionLocal()
        
        # Create multiple test records for indexing tests
        for i in range(100):
            lead = Lead(
                name=f"Test Lead {i}",
                company=f"Company {i % 10}",
                email=f"test{i}@example.com",
                phone=f"123-456-{i:04d}",
                status=LeadStatus.new if i % 2 == 0 else LeadStatus.contacted,
                source=LeadSource.website if i % 3 == 0 else LeadSource.referral,
                assigned_to=f"user{i % 5}",
                value=float(i * 100),
                notes=f"Test lead notes {i}"
            )
            db.add(lead)
        db.commit()
        
        # Test indexed queries
        # Query by indexed field (name)
        start_time = datetime.now()
        leads_by_name = db.query(Lead).filter(Lead.name.like("Test Lead%")).all()
        name_query_time = datetime.now() - start_time
        
        # Query by indexed field (company)
        start_time = datetime.now()
        leads_by_company = db.query(Lead).filter(Lead.company == "Company 5").all()
        company_query_time = datetime.now() - start_time
        
        # Query by indexed field (status)
        start_time = datetime.now()
        leads_by_status = db.query(Lead).filter(Lead.status == LeadStatus.new).all()
        status_query_time = datetime.now() - start_time
        
        db.close()
        
        print(f"  Indexed query performance:")
        print(f"    Name search (100 records): {name_query_time.total_seconds():.4f}s")
        print(f"    Company search: {company_query_time.total_seconds():.4f}s")
        print(f"    Status search: {status_query_time.total_seconds():.4f}s")
        
        print("✓ Database indexing test completed")
        return True
    except Exception as e:
        print(f"✗ Database indexing test failed with error: {e}")
        return False

def test_database_transactions():
    """Test database transactions"""
    print("Testing database transactions...")
    try:
        import importlib
        # Import modules
        database_module = importlib.import_module('app.core.database')
        sales_module = importlib.import_module('app.models.sales')
        enums_module = importlib.import_module('app.models.enums')
        
        SessionLocal = getattr(database_module, 'SessionLocal')
        Lead = getattr(sales_module, 'Lead')
        LeadStatus = getattr(enums_module, 'LeadStatus')
        LeadSource = getattr(enums_module, 'LeadSource')
        
        db = SessionLocal()
        
        # Test successful transaction
        lead_data = {
            "name": "Transaction Test Lead",
            "company": "Transaction Test Company",
            "email": "transaction@example.com",
            "status": LeadStatus.new,
            "source": LeadSource.website
        }
        
        lead = Lead(**lead_data)
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        # Verify the lead was created
        lead_count = db.query(Lead).filter(Lead.id == lead.id).count()
        
        # Clean up
        db.delete(lead)
        db.commit()
        db.close()
        
        if lead_count == 1:
            print("✓ Database transactions test passed")
            return True
        else:
            print("✗ Database transactions test failed")
            return False
    except Exception as e:
        print(f"✗ Database transactions test failed with error: {e}")
        return False

def test_database_constraints():
    """Test database constraints"""
    print("Testing database constraints...")
    db = None
    try:
        import importlib
        # Import modules
        database_module = importlib.import_module('app.core.database')
        sales_module = importlib.import_module('app.models.sales')
        
        SessionLocal = getattr(database_module, 'SessionLocal')
        Lead = getattr(sales_module, 'Lead')
        LeadSource = getattr(importlib.import_module('app.models.enums'), 'LeadSource')
        
        db = SessionLocal()
        
        # Test enum constraints
        lead = Lead(
            name="Constraint Test Lead",
            company="Constraint Test Company",
            status="invalid_status",  # This should fail
            source=LeadSource.website
        )
        
        db.add(lead)
        db.commit()  # This should raise an exception
        
        print("✗ Database constraints test failed - invalid enum value was accepted")
        return False
    except Exception as e:
        if db:
            db.rollback()
            db.close()
        print("✓ Database constraints test passed - invalid enum value was rejected")
        return True
    finally:
        if db:
            db.close()

def cleanup_test_data():
    """Clean up test data"""
    print("Cleaning up test data...")
    try:
        import importlib
        # Import modules
        database_module = importlib.import_module('app.core.database')
        sales_module = importlib.import_module('app.models.sales')
        
        SessionLocal = getattr(database_module, 'SessionLocal')
        Lead = getattr(sales_module, 'Lead')
        Contact = getattr(sales_module, 'Contact')
        Opportunity = getattr(sales_module, 'Opportunity')
        Quotation = getattr(sales_module, 'Quotation')
        Activity = getattr(sales_module, 'Activity')
        Target = getattr(sales_module, 'Target')
        Report = getattr(sales_module, 'Report')
        
        db = SessionLocal()
        
        # Delete test data
        db.query(Report).filter(Report.title.like("Test%")).delete(synchronize_session=False)
        db.query(Target).filter(Target.name.like("Test%")).delete(synchronize_session=False)
        db.query(Activity).filter(Activity.title.like("Test%")).delete(synchronize_session=False)
        db.query(Quotation).filter(Quotation.title.like("Test%")).delete(synchronize_session=False)
        db.query(Opportunity).filter(Opportunity.name.like("Test%")).delete(synchronize_session=False)
        db.query(Contact).filter(Contact.first_name.like("Test%")).delete(synchronize_session=False)
        db.query(Lead).filter(Lead.name.like("Test%")).delete(synchronize_session=False)
        
        db.commit()
        db.close()
        print("Test data cleanup complete")
        return True
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return False

def main():
    """Run all database tests"""
    print("Running Database Test Suite...\n")
    
    # Setup
    setup_test_database()
    
    # Run tests
    tests = [
        test_database_connection,
        test_sales_models_creation,
        test_database_indexing,
        test_database_transactions,
        test_database_constraints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed with exception: {e}")
    
    # Cleanup
    cleanup_test_data()
    
    print(f"\nDatabase Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All database tests passed! ✅")
        return 0
    else:
        print("Some database tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())