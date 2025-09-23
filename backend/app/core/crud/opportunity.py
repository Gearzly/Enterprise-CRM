from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.core.crud.base import CRUDBase
from app.models.sales import Opportunity
from app.sales.opportunity.models import OpportunityCreate, OpportunityUpdate
from datetime import datetime, timedelta

class CRUDOpportunity(CRUDBase[Opportunity, OpportunityCreate, OpportunityUpdate]):
    def get_by_account(self, db: Session, *, account_id: int) -> List[Opportunity]:
        try:
            stmt = select(Opportunity).where(Opportunity.account_id == account_id)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching opportunities by account: {str(e)}"
            )

    def get_by_contact(self, db: Session, *, contact_id: int) -> List[Opportunity]:
        try:
            stmt = select(Opportunity).where(Opportunity.contact_id == contact_id)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching opportunities by contact: {str(e)}"
            )

    def get_by_stage(self, db: Session, *, stage: str) -> List[Opportunity]:
        try:
            stmt = select(Opportunity).where(Opportunity.stage == stage)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching opportunities by stage: {str(e)}"
            )

    def get_by_assigned_to(self, db: Session, *, assigned_to: str) -> List[Opportunity]:
        try:
            stmt = select(Opportunity).where(Opportunity.assigned_to == assigned_to)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching opportunities by assignee: {str(e)}"
            )

    def get_multi_by_value_range(
        self, db: Session, *, min_value: float, max_value: float
    ) -> List[Opportunity]:
        try:
            stmt = select(Opportunity).where(
                and_(Opportunity.value >= min_value, Opportunity.value <= max_value)
            )
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching opportunities by value range: {str(e)}"
            )

    def get_multi_by_probability_range(
        self, db: Session, *, min_probability: int, max_probability: int
    ) -> List[Opportunity]:
        try:
            stmt = select(Opportunity).where(
                and_(Opportunity.probability >= min_probability, Opportunity.probability <= max_probability)
            )
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching opportunities by probability range: {str(e)}"
            )

    def get_recent(self, db: Session, *, days: int) -> List[Opportunity]:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            stmt = select(Opportunity).where(Opportunity.created_at >= cutoff_date)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching recent opportunities: {str(e)}"
            )

opportunity = CRUDOpportunity(Opportunity)