from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status as fastapi_status
from app.core.crud.base import CRUDBase
from app.models.sales import Target
from datetime import datetime, timedelta

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from app.sales.target.models import TargetCreate, TargetUpdate

class CRUDTarget(CRUDBase[Target, 'TargetCreate', 'TargetUpdate']):
    def get_by_type(self, db: Session, *, target_type: str) -> List[Target]:
        try:
            stmt = select(Target).where(Target.target_type == target_type)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching targets by type: {str(e)}"
            )

    def get_by_period(self, db: Session, *, period: str) -> List[Target]:
        try:
            stmt = select(Target).where(Target.period == period)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching targets by period: {str(e)}"
            )

    def get_by_year(self, db: Session, *, year: int) -> List[Target]:
        try:
            stmt = select(Target).where(Target.year == year)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching targets by year: {str(e)}"
            )

    def get_by_assigned_to(self, db: Session, *, assigned_to: str) -> List[Target]:
        try:
            stmt = select(Target).where(Target.assigned_to == assigned_to)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching targets by assignee: {str(e)}"
            )

    def get_multi_by_value_range(
        self, db: Session, *, min_value: float, max_value: float
    ) -> List[Target]:
        try:
            stmt = select(Target).where(
                and_(Target.target_value >= min_value, Target.target_value <= max_value)
            )
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching targets by value range: {str(e)}"
            )

    def get_recent(self, db: Session, *, days: int) -> List[Target]:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            stmt = select(Target).where(Target.created_at >= cutoff_date)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching recent targets: {str(e)}"
            )

target = CRUDTarget(Target)