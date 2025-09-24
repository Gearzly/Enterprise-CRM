"""
Comprehensive error handling middleware for consistent error responses,
logging, and monitoring across the CRM application.
"""
import json
import logging
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from enum import Enum

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from pydantic import BaseModel, ValidationError
import sqlalchemy.exc

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Types of errors for categorization"""
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    BUSINESS_LOGIC_ERROR = "business_logic_error"
    DATABASE_ERROR = "database_error"
    EXTERNAL_SERVICE_ERROR = "external_service_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    NOT_FOUND_ERROR = "not_found_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    SECURITY_ERROR = "security_error"


class ErrorResponse(BaseModel):
    """Standardized error response format"""
    error: bool = True
    error_type: str
    message: str
    details: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: str
    path: Optional[str] = None
    method: Optional[str] = None


class ErrorHandler:
    """Centralized error handling and formatting"""
    
    @staticmethod
    def create_error_response(
        error_type: ErrorType,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        request_id: Optional[str] = None,
        path: Optional[str] = None,
        method: Optional[str] = None
    ) -> JSONResponse:
        """Create a standardized error response"""
        
        error_response = ErrorResponse(
            error_type=error_type.value,
            message=message,
            details=details or {},
            error_code=error_code,
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat(),
            path=path,
            method=method
        )
        
        return JSONResponse(
            status_code=status_code,
            content=error_response.dict(exclude_none=True)
        )
    
    @staticmethod
    def log_error(
        error_type: ErrorType,
        message: str,
        request_id: str,
        exception: Optional[Exception] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        """Log error with consistent format"""
        log_data = {
            "request_id": request_id,
            "error_type": error_type.value,
            "message": message,
            "extra_data": extra_data or {}
        }
        
        if exception:
            log_data["exception_type"] = type(exception).__name__
            log_data["exception_message"] = str(exception)
            log_data["traceback"] = traceback.format_exc()
        
        # Log at appropriate level based on error type
        if error_type in [ErrorType.INTERNAL_SERVER_ERROR, ErrorType.DATABASE_ERROR]:
            logger.error(f"Error: {message}", extra=log_data)
        elif error_type in [ErrorType.AUTHENTICATION_ERROR, ErrorType.AUTHORIZATION_ERROR]:
            logger.warning(f"Security issue: {message}", extra=log_data)
        else:
            logger.info(f"Client error: {message}", extra=log_data)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for centralized error handling"""
    
    def __init__(self, app, include_traceback: bool = False):
        super().__init__(app)
        self.include_traceback = include_traceback
        self.error_handler = ErrorHandler()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and handle any errors"""
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        try:
            response = await call_next(request)
            return response
            
        except HTTPException as e:
            return await self._handle_http_exception(e, request, request_id)
        
        except ValidationError as e:
            return await self._handle_validation_error(e, request, request_id)
        
        except sqlalchemy.exc.SQLAlchemyError as e:
            return await self._handle_database_error(e, request, request_id)
        
        except ConnectionError as e:
            return await self._handle_connection_error(e, request, request_id)
        
        except PermissionError as e:
            return await self._handle_permission_error(e, request, request_id)
        
        except ValueError as e:
            return await self._handle_value_error(e, request, request_id)
        
        except Exception as e:
            return await self._handle_generic_error(e, request, request_id)
    
    async def _handle_http_exception(
        self, 
        exception: HTTPException, 
        request: Request, 
        request_id: str
    ) -> JSONResponse:
        """Handle FastAPI HTTP exceptions"""
        
        # Determine error type based on status code
        error_type = self._get_error_type_from_status(exception.status_code)
        
        # Log the error
        self.error_handler.log_error(
            error_type=error_type,
            message=exception.detail,
            request_id=request_id,
            exception=exception,
            extra_data={
                "status_code": exception.status_code,
                "headers": exception.headers
            }
        )
        
        return self.error_handler.create_error_response(
            error_type=error_type,
            message=exception.detail,
            status_code=exception.status_code,
            request_id=request_id,
            path=str(request.url.path),
            method=request.method
        )
    
    async def _handle_validation_error(
        self, 
        exception: ValidationError, 
        request: Request, 
        request_id: str
    ) -> JSONResponse:
        """Handle Pydantic validation errors"""
        
        error_details = []
        for error in exception.errors():
            error_details.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        self.error_handler.log_error(
            error_type=ErrorType.VALIDATION_ERROR,
            message="Request validation failed",
            request_id=request_id,
            exception=exception,
            extra_data={"validation_errors": error_details}
        )
        
        return self.error_handler.create_error_response(
            error_type=ErrorType.VALIDATION_ERROR,
            message="Invalid request data",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"validation_errors": error_details},
            request_id=request_id,
            path=str(request.url.path),
            method=request.method
        )
    
    async def _handle_database_error(
        self, 
        exception: sqlalchemy.exc.SQLAlchemyError, 
        request: Request, 
        request_id: str
    ) -> JSONResponse:
        """Handle database-related errors"""
        
        error_message = "Database operation failed"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        # Customize message based on specific database error types
        if isinstance(exception, sqlalchemy.exc.IntegrityError):
            error_message = "Data integrity constraint violation"
            status_code = status.HTTP_409_CONFLICT
        elif isinstance(exception, sqlalchemy.exc.DataError):
            error_message = "Invalid data format"
            status_code = status.HTTP_400_BAD_REQUEST
        elif isinstance(exception, sqlalchemy.exc.OperationalError):
            error_message = "Database connection error"
        elif isinstance(exception, sqlalchemy.exc.NoResultFound):
            error_message = "Requested resource not found"
            status_code = status.HTTP_404_NOT_FOUND
        
        self.error_handler.log_error(
            error_type=ErrorType.DATABASE_ERROR,
            message=error_message,
            request_id=request_id,
            exception=exception,
            extra_data={
                "exception_type": type(exception).__name__,
                "original_exception": str(exception.orig) if hasattr(exception, 'orig') else None
            }
        )
        
        return self.error_handler.create_error_response(
            error_type=ErrorType.DATABASE_ERROR,
            message=error_message,
            status_code=status_code,
            error_code=f"DB_{type(exception).__name__.upper()}",
            request_id=request_id,
            path=str(request.url.path),
            method=request.method
        )
    
    async def _handle_connection_error(
        self, 
        exception: ConnectionError, 
        request: Request, 
        request_id: str
    ) -> JSONResponse:
        """Handle connection errors (external services)"""
        
        self.error_handler.log_error(
            error_type=ErrorType.EXTERNAL_SERVICE_ERROR,
            message="External service connection failed",
            request_id=request_id,
            exception=exception
        )
        
        return self.error_handler.create_error_response(
            error_type=ErrorType.EXTERNAL_SERVICE_ERROR,
            message="External service temporarily unavailable",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="SERVICE_UNAVAILABLE",
            request_id=request_id,
            path=str(request.url.path),
            method=request.method
        )
    
    async def _handle_permission_error(
        self, 
        exception: PermissionError, 
        request: Request, 
        request_id: str
    ) -> JSONResponse:
        """Handle permission errors"""
        
        self.error_handler.log_error(
            error_type=ErrorType.AUTHORIZATION_ERROR,
            message="Permission denied",
            request_id=request_id,
            exception=exception
        )
        
        return self.error_handler.create_error_response(
            error_type=ErrorType.AUTHORIZATION_ERROR,
            message="Insufficient permissions",
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="PERMISSION_DENIED",
            request_id=request_id,
            path=str(request.url.path),
            method=request.method
        )
    
    async def _handle_value_error(
        self, 
        exception: ValueError, 
        request: Request, 
        request_id: str
    ) -> JSONResponse:
        """Handle value errors (usually business logic)"""
        
        self.error_handler.log_error(
            error_type=ErrorType.BUSINESS_LOGIC_ERROR,
            message=str(exception),
            request_id=request_id,
            exception=exception
        )
        
        return self.error_handler.create_error_response(
            error_type=ErrorType.BUSINESS_LOGIC_ERROR,
            message=str(exception),
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="BUSINESS_RULE_VIOLATION",
            request_id=request_id,
            path=str(request.url.path),
            method=request.method
        )
    
    async def _handle_generic_error(
        self, 
        exception: Exception, 
        request: Request, 
        request_id: str
    ) -> JSONResponse:
        """Handle unexpected errors"""
        
        self.error_handler.log_error(
            error_type=ErrorType.INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred",
            request_id=request_id,
            exception=exception,
            extra_data={
                "exception_type": type(exception).__name__,
                "exception_args": exception.args
            }
        )
        
        # Include traceback in development mode
        details = {}
        if self.include_traceback:
            details["traceback"] = traceback.format_exc()
        
        return self.error_handler.create_error_response(
            error_type=ErrorType.INTERNAL_SERVER_ERROR,
            message="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details,
            error_code="INTERNAL_ERROR",
            request_id=request_id,
            path=str(request.url.path),
            method=request.method
        )
    
    def _get_error_type_from_status(self, status_code: int) -> ErrorType:
        """Map HTTP status codes to error types"""
        if status_code == 400:
            return ErrorType.VALIDATION_ERROR
        elif status_code == 401:
            return ErrorType.AUTHENTICATION_ERROR
        elif status_code == 403:
            return ErrorType.AUTHORIZATION_ERROR
        elif status_code == 404:
            return ErrorType.NOT_FOUND_ERROR
        elif status_code == 429:
            return ErrorType.RATE_LIMIT_ERROR
        elif 400 <= status_code < 500:
            return ErrorType.BUSINESS_LOGIC_ERROR
        else:
            return ErrorType.INTERNAL_SERVER_ERROR


class SecurityErrorMiddleware(BaseHTTPMiddleware):
    """Specialized middleware for security-related errors"""
    
    def __init__(self, app):
        super().__init__(app)
        self.error_handler = ErrorHandler()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Monitor for security violations"""
        
        try:
            response = await call_next(request)
            return response
            
        except HTTPException as e:
            # Log security-related HTTP exceptions
            if e.status_code in [401, 403]:
                self._log_security_event(request, e)
            raise
        
        except Exception as e:
            # Check for potential security issues
            if self._is_security_related(e):
                self._log_security_event(request, e)
            raise
    
    def _is_security_related(self, exception: Exception) -> bool:
        """Check if exception might be security-related"""
        security_keywords = [
            "injection", "xss", "csrf", "sql", "script", 
            "authentication", "authorization", "token"
        ]
        
        exception_str = str(exception).lower()
        return any(keyword in exception_str for keyword in security_keywords)
    
    def _log_security_event(self, request: Request, exception: Exception):
        """Log security events for monitoring"""
        security_data = {
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown"),
            "path": str(request.url.path),
            "method": request.method,
            "query_params": dict(request.query_params),
            "exception_type": type(exception).__name__,
            "exception_message": str(exception)
        }
        
        logger.warning(
            f"Security event detected: {type(exception).__name__}",
            extra={"security_event": security_data}
        )


# Custom exception classes for business logic
class BusinessLogicError(Exception):
    """Base class for business logic errors"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ResourceNotFoundError(BusinessLogicError):
    """Raised when a requested resource is not found"""
    pass


class DuplicateResourceError(BusinessLogicError):
    """Raised when attempting to create a duplicate resource"""
    pass


class InvalidOperationError(BusinessLogicError):
    """Raised when an operation is not valid in the current state"""
    pass


class ExternalServiceError(Exception):
    """Raised when external service calls fail"""
    
    def __init__(self, service_name: str, message: str, status_code: Optional[int] = None):
        self.service_name = service_name
        self.message = message
        self.status_code = status_code
        super().__init__(f"{service_name}: {message}")


# Utility functions for error handling
def create_business_error(message: str, error_code: Optional[str] = None) -> HTTPException:
    """Create a business logic error response"""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


def create_not_found_error(resource: str, identifier: Any) -> HTTPException:
    """Create a not found error response"""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with identifier '{identifier}' not found"
    )


def create_duplicate_error(resource: str, field: str, value: Any) -> HTTPException:
    """Create a duplicate resource error response"""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource} with {field} '{value}' already exists"
    )


def create_validation_error(field: str, message: str) -> HTTPException:
    """Create a validation error response"""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Validation error for field '{field}': {message}"
    )


# Error monitoring and metrics (placeholder for integration with monitoring systems)
class ErrorMetrics:
    """Error metrics collection"""
    
    @staticmethod
    def increment_error_count(error_type: ErrorType, endpoint: str):
        """Increment error count for monitoring"""
        # In production, integrate with Prometheus, DataDog, etc.
        logger.info(f"Error metric: {error_type.value} at {endpoint}")
    
    @staticmethod
    def record_error_response_time(endpoint: str, response_time: float):
        """Record response time for error scenarios"""
        # In production, integrate with monitoring systems
        logger.info(f"Error response time: {endpoint} took {response_time}ms")