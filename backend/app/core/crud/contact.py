from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status as fastapi_status
from app.core.crud.base import CRUDBase
from app.models.sales import Contact
from datetime import datetime, timedelta

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from app.sales.contact.models import ContactCreate, ContactUpdate

class CRUDContact(CRUDBase[Contact, 'ContactCreate', 'ContactUpdate']):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Contact]:
        try:
            stmt = select(Contact).where(Contact.email == email)
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching contact by email: {str(e)}"
            )

    def get_by_company(self, db: Session, *, company: str) -> List[Contact]:
        try:
            stmt = select(Contact).where(Contact.company == company)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching contacts by company: {str(e)}"
            )

    def get_by_contact_type(self, db: Session, *, contact_type: str) -> List[Contact]:
        try:
            stmt = select(Contact).where(Contact.contact_type == contact_type)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching contacts by type: {str(e)}"
            )

    def get_by_country(self, db: Session, *, country: str) -> List[Contact]:
        try:
            stmt = select(Contact).where(Contact.country == country)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching contacts by country: {str(e)}"
            )

    def get_by_state(self, db: Session, *, state: str) -> List[Contact]:
        try:
            stmt = select(Contact).where(Contact.state == state)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching contacts by state: {str(e)}"
            )

    def get_by_department(self, db: Session, *, department: str) -> List[Contact]:
        try:
            stmt = select(Contact).where(Contact.department == department)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching contacts by department: {str(e)}"
            )

    def get_recent(self, db: Session, *, days: int) -> List[Contact]:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            stmt = select(Contact).where(Contact.created_at >= cutoff_date)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching recent contacts: {str(e)}"
            )

contact = CRUDContact(Contact)