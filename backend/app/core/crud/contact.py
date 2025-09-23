from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.crud.base import CRUDBase
from app.models.sales import Contact
from app.sales.contact.models import ContactCreate, ContactUpdate
from datetime import datetime, timedelta

class CRUDContact(CRUDBase[Contact, ContactCreate, ContactUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Contact]:
        return db.query(Contact).filter(Contact.email == email).first()

    def get_by_company(self, db: Session, *, company: str) -> List[Contact]:
        return db.query(Contact).filter(Contact.company == company).all()

    def get_by_contact_type(self, db: Session, *, contact_type: str) -> List[Contact]:
        return db.query(Contact).filter(Contact.contact_type == contact_type).all()

    def get_by_country(self, db: Session, *, country: str) -> List[Contact]:
        return db.query(Contact).filter(Contact.country == country).all()

    def get_by_state(self, db: Session, *, state: str) -> List[Contact]:
        return db.query(Contact).filter(Contact.state == state).all()

    def get_by_department(self, db: Session, *, department: str) -> List[Contact]:
        return db.query(Contact).filter(Contact.department == department).all()

    def get_recent(self, db: Session, *, days: int) -> List[Contact]:
        cutoff_date = datetime.now() - timedelta(days=days)
        return db.query(Contact).filter(Contact.created_at >= cutoff_date).all()

contact = CRUDContact(Contact)