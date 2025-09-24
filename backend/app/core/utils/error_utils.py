"""
Error Handling Utilities
Provides decorators and utilities for consistent error handling across all modules.
"""
import logging
import functools
import time
from typing import Callable, Any, Optional, Dict
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, OperationalError
from app.core.middleware.error_handling import (
    ErrorType, 
    BusinessLogicError, 
    ResourceNotFoundError, 
    DuplicateResourceError,
    create_business_error,
    create_not_found_error,
    create_duplicate_error
)
from app.core.logging_config import get_logger, log_performance_metric, log_security_event


def handle_database_errors(func: Callable) -> Callable:
    """
    Decorator to handle database errors consistently across all modules.
    Converts SQLAlchemy exceptions to appropriate HTTP exceptions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            # Log performance metric
            duration_ms = (time.time() - start_time) * 1000
            log_performance_metric(
                logger, 
                f"{func.__module__}.{func.__name__}", 
                duration_ms
            )
            
            return result
            
        except IntegrityError as e:
            logger.error(f"Database integrity error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Data integrity constraint violation"
            )
        except DataError as e:
            logger.error(f"Database data error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data format"
            )
        except OperationalError as e:
            logger.error(f"Database operational error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service temporarily unavailable"
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
    
    return wrapper


def handle_business_logic_errors(func: Callable) -> Callable:
    """
    Decorator to handle business logic errors consistently.
    Converts business logic exceptions to appropriate HTTP exceptions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        try:
            return func(*args, **kwargs)
            
        except ResourceNotFoundError as e:
            logger.warning(f"Resource not found in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except DuplicateResourceError as e:
            logger.warning(f"Duplicate resource in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except BusinessLogicError as e:
            logger.warning(f"Business logic error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except ValueError as e:
            logger.warning(f"Value error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid value: {str(e)}"
            )
    
    return wrapper


def handle_security_errors(func: Callable) -> Callable:
    """
    Decorator to handle security-related errors and log security events.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(f"security.{func.__module__}")
        
        try:
            return func(*args, **kwargs)
            
        except PermissionError as e:
            log_security_event(
                logger,
                "permission_denied",
                f"Permission denied in {func.__name__}: {str(e)}",
                "high"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        except Exception as e:
            # Check if error might be security-related
            error_str = str(e).lower()
            security_keywords = ['injection', 'xss', 'csrf', 'unauthorized', 'forbidden']
            
            if any(keyword in error_str for keyword in security_keywords):
                log_security_event(
                    logger,
                    "potential_security_issue",
                    f"Potential security issue in {func.__name__}: {str(e)}",
                    "high"
                )
            
            raise
    
    return wrapper


def comprehensive_error_handler(
    include_database: bool = True,
    include_business_logic: bool = True,
    include_security: bool = False
):
    """
    Comprehensive error handler decorator that combines multiple error handling strategies.
    
    Args:
        include_database: Whether to handle database errors
        include_business_logic: Whether to handle business logic errors
        include_security: Whether to handle security errors
    """
    def decorator(func: Callable) -> Callable:
        # Apply decorators in reverse order (innermost first)
        decorated_func = func
        
        if include_business_logic:
            decorated_func = handle_business_logic_errors(decorated_func)
        
        if include_database:
            decorated_func = handle_database_errors(decorated_func)
        
        if include_security:
            decorated_func = handle_security_errors(decorated_func)
        
        return decorated_func
    
    return decorator


def log_api_call(func: Callable) -> Callable:
    """
    Decorator to log API calls with performance metrics and error tracking.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(f"api.{func.__module__}")
        start_time = time.time()
        
        # Log API call start
        logger.info(f"API call started: {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            
            # Log successful completion with performance metric
            duration_ms = (time.time() - start_time) * 1000
            log_performance_metric(
                logger,
                f"api.{func.__name__}",
                duration_ms,
                {"status": "success"}
            )
            
            logger.info(f"API call completed successfully: {func.__name__} ({duration_ms:.2f}ms)")
            return result
            
        except HTTPException as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.warning(
                f"API call failed: {func.__name__} - {e.status_code}: {e.detail} ({duration_ms:.2f}ms)"
            )
            raise
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"API call error: {func.__name__} - {str(e)} ({duration_ms:.2f}ms)",
                exc_info=True
            )
            raise
    
    return wrapper


def validate_input(validation_func: Callable[[Any], bool], error_message: str):
    """
    Decorator to validate input parameters.
    
    Args:
        validation_func: Function that takes the first argument and returns True if valid
        error_message: Error message to raise if validation fails
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if args and not validation_func(args[0]):
                logger = get_logger(func.__module__)
                logger.warning(f"Input validation failed in {func.__name__}: {error_message}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


class ErrorContext:
    """
    Context manager for error handling with automatic logging and cleanup.
    """
    
    def __init__(self, operation_name: str, logger: Optional[logging.Logger] = None):
        self.operation_name = operation_name
        self.logger = logger or get_logger(__name__)
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        
        if exc_type is None:
            # Success
            log_performance_metric(
                self.logger,
                self.operation_name,
                duration_ms,
                {"status": "success"}
            )
            self.logger.info(f"Operation completed successfully: {self.operation_name} ({duration_ms:.2f}ms)")
        else:
            # Error occurred
            self.logger.error(
                f"Operation failed: {self.operation_name} - {exc_type.__name__}: {str(exc_val)} ({duration_ms:.2f}ms)",
                exc_info=True
            )
        
        # Don't suppress exceptions
        return False


# Utility functions for common error scenarios
def ensure_resource_exists(resource, resource_name: str, identifier: Any):
    """Ensure a resource exists, raise ResourceNotFoundError if not"""
    if resource is None:
        raise ResourceNotFoundError(f"{resource_name} with identifier '{identifier}' not found")
    return resource


def ensure_unique_resource(existing_resource, resource_name: str, field: str, value: Any):
    """Ensure a resource is unique, raise DuplicateResourceError if not"""
    if existing_resource is not None:
        raise DuplicateResourceError(f"{resource_name} with {field} '{value}' already exists")


def validate_business_rule(condition: bool, message: str):
    """Validate a business rule, raise BusinessLogicError if violated"""
    if not condition:
        raise BusinessLogicError(message)