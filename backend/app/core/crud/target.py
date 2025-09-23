from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.crud.base import CRUDBase
from app.models.sales import Target
from app.sales.target.models import TargetCreate, TargetUpdate

class CRUDTarget(CRUDBase[Target, TargetCreate, TargetUpdate]):
    def get_by_type(self, db: Session, *, target_type: str) -> List[Target]:
        return db.query(Target).filter(Target.target_type == target_type).all()

    def get_by_period(self, db: Session, *, period: str) -> List[Target]:
        return db.query(Target).filter(Target.period == period).all()

    def get_by_year(self, db: Session, *, year: int) -> List[Target]:
        return db.query(Target).filter(Target.year == year).all()

    def get_by_assigned_to(self, db: Session, *, assigned_to: str) -> List[Target]:
        return db.query(Target).filter(Target.assigned_to == assigned_to).all()

    def get_multi_by_value_range(
        self, db: Session, *, min_value: float, max_value: float
    ) -> List[Target]:
        return db.query(Target).filter(
            Target.target_value >= min_value, Target.target_value <= max_value
        ).all()

target = CRUDTarget(Target)