from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status as fastapi_status
from app.core.crud.base import CRUDBase
from app.models.sales import Activity
from datetime import datetime, timedelta

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from app.sales.activity.models import ActivityCreate, ActivityUpdate

class CRUDActivity(CRUDBase[Activity, 'ActivityCreate', 'ActivityUpdate']):
    def get_by_activity_type(self, db: Session, *, activity_type: str) -> List[Activity]:
        try:
            stmt = select(Activity).where(Activity.activity_type == activity_type)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching activities by type: {str(e)}"
            )

    def get_by_status(self, db: Session, *, status: str) -> List[Activity]:
        try:
            stmt = select(Activity).where(Activity.status == status)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching activities by status: {str(e)}"
            )

    def get_by_assigned_to(self, db: Session, *, assigned_to: str) -> List[Activity]:
        try:
            stmt = select(Activity).where(Activity.assigned_to == assigned_to)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching activities by assignee: {str(e)}"
            )

    def get_by_related(self, db: Session, *, related_to: str, related_id: int) -> List[Activity]:
        try:
            stmt = select(Activity).where(
                and_(Activity.related_to == related_to, Activity.related_id == related_id)
            )
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching activities by related entity: {str(e)}"
            )

    def get_upcoming(self, db: Session, *, days: int) -> List[Activity]:
        try:
            cutoff_date = datetime.now() + timedelta(days=days)
            stmt = select(Activity).where(
                and_(
                    Activity.start_time >= datetime.now(),
                    Activity.start_time <= cutoff_date
                )
            )
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching upcoming activities: {str(e)}"
            )

    def get_recent(self, db: Session, *, days: int) -> List[Activity]:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            stmt = select(Activity).where(Activity.created_at >= cutoff_date)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching recent activities: {str(e)}"
            )

activity = CRUDActivity(Activity)