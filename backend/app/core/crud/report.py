from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.crud.base import CRUDBase
from app.models.sales import Report
from app.sales.report.models import ReportCreate, ReportUpdate

class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def get_by_type(self, db: Session, *, report_type: str) -> List[Report]:
        return db.query(Report).filter(Report.report_type == report_type).all()

    def get_by_status(self, db: Session, *, status: str) -> List[Report]:
        return db.query(Report).filter(Report.status == status).all()

    def get_by_generated_by(self, db: Session, *, generated_by: str) -> List[Report]:
        return db.query(Report).filter(Report.generated_by == generated_by).all()

report = CRUDReport(Report)