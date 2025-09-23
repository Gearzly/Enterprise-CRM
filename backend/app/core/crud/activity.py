from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.crud.base import CRUDBase
from app.models.sales import Activity
from app.sales.activity.models import ActivityCreate, ActivityUpdate
from datetime import datetime, timedelta

class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    def get_by_type(self, db: Session, *, activity_type: str) -> List[Activity]:
        return db.query(Activity).filter(Activity.activity_type == activity_type).all()

    def get_by_status(self, db: Session, *, status: str) -> List[Activity]:
        return db.query(Activity).filter(Activity.status == status).all()

    def get_by_assigned_to(self, db: Session, *, assigned_to: str) -> List[Activity]:
        return db.query(Activity).filter(Activity.assigned_to == assigned_to).all()

    def get_by_related(self, db: Session, *, related_to: str, related_id: int) -> List[Activity]:
        return db.query(Activity).filter(
            Activity.related_to == related_to, Activity.related_id == related_id
        ).all()

    def get_upcoming(self, db: Session, *, days: int) -> List[Activity]:
        now = datetime.now()
        cutoff_date = now + timedelta(days=days)
        return db.query(Activity).filter(
            Activity.start_time >= now, Activity.start_time <= cutoff_date
        ).all()

    def get_recent(self, db: Session, *, days: int) -> List[Activity]:
        cutoff_date = datetime.now() - timedelta(days=days)
        return db.query(Activity).filter(Activity.created_at >= cutoff_date).all()

activity = CRUDActivity(Activity)