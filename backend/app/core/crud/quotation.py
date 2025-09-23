from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status as fastapi_status
from app.core.crud.base import CRUDBase
from app.models.sales import Quotation
from app.sales.quotation.models import QuotationCreate, QuotationUpdate
from datetime import datetime, timedelta

class CRUDQuotation(CRUDBase[Quotation, QuotationCreate, QuotationUpdate]):
    def get_by_account(self, db: Session, *, account_id: int) -> List[Quotation]:
        try:
            stmt = select(Quotation).where(Quotation.account_id == account_id)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching quotations by account: {str(e)}"
            )

    def get_by_contact(self, db: Session, *, contact_id: int) -> List[Quotation]:
        try:
            stmt = select(Quotation).where(Quotation.contact_id == contact_id)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching quotations by contact: {str(e)}"
            )

    def get_by_opportunity(self, db: Session, *, opportunity_id: int) -> List[Quotation]:
        try:
            stmt = select(Quotation).where(Quotation.opportunity_id == opportunity_id)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching quotations by opportunity: {str(e)}"
            )

    def get_by_status(self, db: Session, *, status: str) -> List[Quotation]:
        try:
            stmt = select(Quotation).where(Quotation.status == status)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching quotations by status: {str(e)}"
            )

    def get_multi_by_amount_range(
        self, db: Session, *, min_amount: float, max_amount: float
    ) -> List[Quotation]:
        try:
            stmt = select(Quotation).where(
                and_(Quotation.total_amount >= min_amount, Quotation.total_amount <= max_amount)
            )
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching quotations by amount range: {str(e)}"
            )

    def get_valid_within_days(self, db: Session, *, days: int) -> List[Quotation]:
        try:
            cutoff_date = datetime.now() + timedelta(days=days)
            stmt = select(Quotation).where(Quotation.valid_until <= cutoff_date)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching quotations valid within days: {str(e)}"
            )

    def get_recent(self, db: Session, *, days: int) -> List[Quotation]:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            stmt = select(Quotation).where(Quotation.created_at >= cutoff_date)
            result = db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching recent quotations: {str(e)}"
            )

quotation = CRUDQuotation(Quotation)