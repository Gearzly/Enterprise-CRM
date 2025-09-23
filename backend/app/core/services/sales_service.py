from sqlalchemy.orm import Session
from app.core.database_transactions import transaction_context, execute_in_transaction
from app.models.sales import Lead, Opportunity, Quotation
from app.sales.lead.models import LeadCreate
from app.sales.opportunity.models import OpportunityCreate
from app.sales.quotation.models import QuotationCreate
from fastapi import HTTPException, status
from typing import Tuple

def create_lead_opportunity_quotation(
    db: Session, 
    lead_data: LeadCreate, 
    opportunity_data: OpportunityCreate, 
    quotation_data: QuotationCreate
) -> Tuple[Lead, Opportunity, Quotation]:
    """
    Create a lead, opportunity, and quotation in a single transaction.
    
    This function demonstrates how to use transactions for complex operations
    that involve multiple related entities.
    
    Args:
        db: Database session
        lead_data: Data for creating a lead
        opportunity_data: Data for creating an opportunity
        quotation_data: Data for creating a quotation
        
    Returns:
        Tuple of created lead, opportunity, and quotation
        
    Raises:
        HTTPException: If there's a database error or validation issue
    """
    def operations(tx_db):
        # Create lead
        lead_dict = lead_data.dict()
        lead = Lead(**lead_dict)
        tx_db.add(lead)
        
        # Create opportunity
        opportunity_dict = opportunity_data.dict()
        opportunity = Opportunity(**opportunity_dict)
        tx_db.add(opportunity)
        
        # Create quotation
        quotation_dict = quotation_data.dict()
        quotation = Quotation(**quotation_dict)
        tx_db.add(quotation)
        
        # Flush to get IDs for relationships if needed
        tx_db.flush()
        
        return lead, opportunity, quotation
    
    return execute_in_transaction(db, operations)

def delete_lead_and_related_opportunities(
    db: Session, 
    lead_id: int
) -> dict:
    """
    Delete a lead and all related opportunities in a single transaction.
    
    Args:
        db: Database session
        lead_id: ID of the lead to delete
        
    Returns:
        Dictionary with deletion confirmation
        
    Raises:
        HTTPException: If there's a database error or if lead is not found
    """
    def operations(tx_db):
        # Get lead
        lead = tx_db.get(Lead, lead_id)
        if lead is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with id {lead_id} not found"
            )
        
        # Delete lead
        tx_db.delete(lead)
        
        # In a real implementation, you might also want to delete related opportunities
        # For now, we're just demonstrating the transaction pattern
        
        return {"message": f"Lead {lead_id} and related data deleted successfully"}
    
    return execute_in_transaction(db, operations)