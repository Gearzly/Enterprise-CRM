from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status as fastapi_status
from datetime import datetime, timedelta
from app.core.crud.base import CRUDBase
from app.models.sales import Lead

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from app.sales.lead.models import LeadCreate, LeadUpdate

class CRUDLead(CRUDBase[Lead, 'LeadCreate', 'LeadUpdate']):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Lead]:
        try:
            stmt = select(Lead).where(Lead.name == name)
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching lead by name: {str(e)}"
            )

    def get_by_company(self, db: Session, *, company: str) -> List[Lead]:
        try:
            stmt = select(Lead).where(Lead.company == company)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching leads by company: {str(e)}"
            )

    def get_by_status(self, db: Session, *, status: str) -> List[Lead]:
        try:
            stmt = select(Lead).where(Lead.status == status)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching leads by status: {str(e)}"
            )

    def get_by_source(self, db: Session, *, source: str) -> List[Lead]:
        try:
            stmt = select(Lead).where(Lead.source == source)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching leads by source: {str(e)}"
            )

    def get_by_assigned_to(self, db: Session, *, assigned_to: str) -> List[Lead]:
        try:
            stmt = select(Lead).where(Lead.assigned_to == assigned_to)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching leads by assignee: {str(e)}"
            )

    def get_multi_by_value_range(
        self, db: Session, *, min_value: float, max_value: float
    ) -> List[Lead]:
        try:
            stmt = select(Lead).where(
                and_(Lead.value >= min_value, Lead.value <= max_value)
            )
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching leads by value range: {str(e)}"
            )

    def get_recent(self, db: Session, *, days: int) -> List[Lead]:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            stmt = select(Lead).where(Lead.created_at >= cutoff_date)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching recent leads: {str(e)}"
            )

# Create instance without importing the models to avoid circular import
lead = CRUDLead(Lead)