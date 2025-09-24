from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status as fastapi_status
from app.core.crud.base import CRUDBase
from app.models.support import SLA, SLABreach, SLANotification
from datetime import datetime

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from app.support.sla.models import SLACreate, SLAUpdate, SLABreachCreate, SLABreachUpdate, SLANotificationCreate, SLANotificationUpdate


class CRUDSLA(CRUDBase[SLA, "SLACreate", "SLAUpdate"]):
    def get_active_slas(self, db: Session) -> List[SLA]:
        """Get all active SLAs"""
        try:
            stmt = select(SLA).where(SLA.is_active == True)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error retrieving active SLAs: {str(e)}"
            )

    def get_by_type(self, db: Session, *, sla_type: str) -> List[SLA]:
        """Get SLAs by type"""
        try:
            stmt = select(SLA).where(SLA.type == sla_type)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error retrieving SLAs by type: {str(e)}"
            )

    def activate_sla(self, db: Session, *, sla_id: int) -> SLA:
        """Activate an SLA"""
        try:
            sla = self.get(db=db, id=sla_id)
            if not sla:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_404_NOT_FOUND,
                    detail="SLA not found"
                )
            sla.is_active = True
            sla.updated_at = datetime.now()
            db.commit()
            db.refresh(sla)
            return sla
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error activating SLA: {str(e)}"
            )

    def deactivate_sla(self, db: Session, *, sla_id: int) -> SLA:
        """Deactivate an SLA"""
        try:
            sla = self.get(db=db, id=sla_id)
            if not sla:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_404_NOT_FOUND,
                    detail="SLA not found"
                )
            sla.is_active = False
            sla.updated_at = datetime.now()
            db.commit()
            db.refresh(sla)
            return sla
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error deactivating SLA: {str(e)}"
            )


class CRUDSLABreach(CRUDBase[SLABreach, "SLABreachCreate", "SLABreachUpdate"]):
    def get_unresolved_breaches(self, db: Session) -> List[SLABreach]:
        """Get all unresolved SLA breaches"""
        try:
            stmt = select(SLABreach).where(SLABreach.resolved == False)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error retrieving unresolved breaches: {str(e)}"
            )

    def get_breaches_for_ticket(self, db: Session, *, ticket_id: int) -> List[SLABreach]:
        """Get all breaches for a specific ticket"""
        try:
            stmt = select(SLABreach).where(SLABreach.ticket_id == ticket_id)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error retrieving breaches for ticket: {str(e)}"
            )

    def resolve_breach(self, db: Session, *, breach_id: int) -> SLABreach:
        """Resolve an SLA breach"""
        try:
            breach = self.get(db=db, id=breach_id)
            if not breach:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_404_NOT_FOUND,
                    detail="SLA breach not found"
                )
            breach.resolved = True
            breach.resolved_at = datetime.now()
            breach.updated_at = datetime.now()
            db.commit()
            db.refresh(breach)
            return breach
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error resolving breach: {str(e)}"
            )


class CRUDSLANotification(CRUDBase[SLANotification, "SLANotificationCreate", "SLANotificationUpdate"]):
    def get_notifications_for_sla(self, db: Session, *, sla_id: int) -> List[SLANotification]:
        """Get all notifications for a specific SLA"""
        try:
            stmt = select(SLANotification).where(SLANotification.sla_id == sla_id)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error retrieving notifications for SLA: {str(e)}"
            )


# Create instances
sla = CRUDSLA(SLA)
sla_breach = CRUDSLABreach(SLABreach)
sla_notification = CRUDSLANotification(SLANotification)