from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import Generator

@contextmanager
def transaction_context(db: Session) -> Generator[Session, None, None]:
    """
    Context manager for database transactions.
    
    Usage:
        with transaction_context(db) as tx_db:
            # Perform multiple database operations
            tx_db.add(obj1)
            tx_db.add(obj2)
            # Transaction will be committed automatically
            # If an exception occurs, it will be rolled back
    
    Args:
        db: Database session
        
    Yields:
        Database session for use within the transaction
        
    Raises:
        HTTPException: If there's a database error
    """
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database transaction error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during transaction: {str(e)}"
        )

def execute_in_transaction(db: Session, operations_func):
    """
    Execute a function within a database transaction.
    
    Usage:
        def my_operations(tx_db):
            obj1 = MyModel(name="test1")
            tx_db.add(obj1)
            obj2 = MyModel(name="test2")
            tx_db.add(obj2)
            return [obj1, obj2]
            
        results = execute_in_transaction(db, my_operations)
    
    Args:
        db: Database session
        operations_func: Function that takes a database session and performs operations
        
    Returns:
        Result of the operations_func
        
    Raises:
        HTTPException: If there's a database error
    """
    try:
        result = operations_func(db)
        db.commit()
        return result
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database transaction error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during transaction: {str(e)}"
        )