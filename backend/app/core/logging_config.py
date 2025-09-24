"""
Comprehensive Logging Configuration for CRM Application
Provides structured logging with proper formatters, handlers, and security considerations.
"""
import logging
import logging.config
import os
import sys
from datetime import datetime
from typing import Dict, Any
import json


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        
        if hasattr(record, 'error_type'):
            log_entry['error_type'] = record.error_type
        
        if hasattr(record, 'security_event'):
            log_entry['security_event'] = record.security_event
        
        if hasattr(record, 'performance_metrics'):
            log_entry['performance_metrics'] = record.performance_metrics
        
        # Add exception information if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else None,
                'message': str(record.exc_info[1]) if record.exc_info[1] else None,
                'traceback': self.formatException(record.exc_info) if record.exc_info else None
            }
        
        return json.dumps(log_entry, ensure_ascii=False)


class SecurityFilter(logging.Filter):
    """Filter to prevent logging of sensitive information"""
    
    SENSITIVE_PATTERNS = [
        'password', 'token', 'secret', 'key', 'authorization',
        'cookie', 'session', 'credential', 'private'
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out log records containing sensitive information"""
        message = record.getMessage().lower()
        
        # Check if message contains sensitive patterns
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in message:
                # Replace sensitive content with placeholder
                record.msg = "[SENSITIVE DATA REDACTED]"
                record.args = ()
                break
        
        return True


def get_log_level() -> int:
    """Get log level from environment variable"""
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level_name, logging.INFO)


def get_logging_config() -> Dict[str, Any]:
    """Get comprehensive logging configuration"""
    
    # Determine if we're in development or production
    is_development = os.getenv("ENVIRONMENT", "development").lower() == "development"
    log_level = get_log_level()
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "format": "%(levelname)s - %(name)s - %(message)s"
            },
            "structured": {
                "()": StructuredFormatter
            }
        },
        "filters": {
            "security_filter": {
                "()": SecurityFilter
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "detailed" if is_development else "structured",
                "stream": sys.stdout,
                "filters": ["security_filter"]
            },
            "file_general": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "structured",
                "filename": os.path.join(log_dir, "crm_general.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "filters": ["security_filter"]
            },
            "file_error": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "structured",
                "filename": os.path.join(log_dir, "crm_errors.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 10,
                "filters": ["security_filter"]
            },
            "file_security": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "WARNING",
                "formatter": "structured",
                "filename": os.path.join(log_dir, "crm_security.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 20
            },
            "file_audit": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "structured",
                "filename": os.path.join(log_dir, "crm_audit.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 30
            }
        },
        "loggers": {
            # Root logger
            "": {
                "level": log_level,
                "handlers": ["console", "file_general", "file_error"]
            },
            # Application loggers
            "app": {
                "level": log_level,
                "handlers": ["console", "file_general", "file_error"],
                "propagate": False
            },
            # Security-specific logger
            "app.core.security": {
                "level": "WARNING",
                "handlers": ["console", "file_security"],
                "propagate": False
            },
            # Audit logger
            "app.core.audit": {
                "level": "INFO",
                "handlers": ["file_audit"],
                "propagate": False
            },
            # OAuth2 authentication logger
            "app.core.auth": {
                "level": "INFO",
                "handlers": ["console", "file_general", "file_security"],
                "propagate": False
            },
            # Database logger
            "app.core.database": {
                "level": "WARNING",
                "handlers": ["console", "file_general"],
                "propagate": False
            },
            # Reduce noise from external libraries
            "uvicorn": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False
            },
            "sqlalchemy.engine": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False
            },
            "sqlalchemy.pool": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False
            }
        }
    }
    
    return config


def configure_logging():
    """Configure comprehensive logging for the application"""
    config = get_logging_config()
    logging.config.dictConfig(config)
    
    # Log configuration success
    logger = logging.getLogger(__name__)
    logger.info("Logging configuration initialized successfully")
    logger.info(f"Log level: {logging.getLevelName(get_log_level())}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)


def log_performance_metric(
    logger: logging.Logger,
    operation: str,
    duration_ms: float,
    additional_data: Dict[str, Any] = None
):
    """Log performance metrics in a structured way"""
    performance_data = {
        "operation": operation,
        "duration_ms": duration_ms,
        "additional_data": additional_data or {}
    }
    
    logger.info(
        f"Performance metric: {operation} took {duration_ms:.2f}ms",
        extra={"performance_metrics": performance_data}
    )


def log_security_event(
    logger: logging.Logger,
    event_type: str,
    description: str,
    severity: str = "medium",
    additional_data: Dict[str, Any] = None
):
    """Log security events in a structured way"""
    security_data = {
        "event_type": event_type,
        "description": description,
        "severity": severity,
        "additional_data": additional_data or {}
    }
    
    logger.warning(
        f"Security event: {event_type} - {description}",
        extra={"security_event": security_data}
    )


# Initialize logging when module is imported
if __name__ != "__main__":
    configure_logging()