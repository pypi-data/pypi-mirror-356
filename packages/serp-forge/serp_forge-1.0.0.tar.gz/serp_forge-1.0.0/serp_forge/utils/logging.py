"""
Logging utilities for Serp Forge.
"""

import logging
import sys
from typing import Optional

import structlog
from structlog.stdlib import LoggerFactory

from ..config import config

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Global logger instance
_logger: Optional[structlog.stdlib.BoundLogger] = None


def setup_logging(
    level: Optional[str] = None,
    format_type: Optional[str] = None
) -> None:
    """Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Log format type (json, console)
    """
    global _logger
    
    # Use config values if not provided
    level = level or config.monitoring.log_level
    format_type = format_type or config.monitoring.log_format
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper())
    )
    
    # Configure structlog based on format
    if format_type.lower() == "console":
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.dev.ConsoleRenderer()
            ],
            context_class=dict,
            logger_factory=LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    
    # Create global logger
    _logger = structlog.get_logger("serp_forge")
    
    _logger.info(
        "Logging configured",
        level=level,
        format=format_type
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)


def get_global_logger() -> structlog.stdlib.BoundLogger:
    """Get the global logger instance.
    
    Returns:
        Global logger instance
    """
    global _logger
    if _logger is None:
        setup_logging()
    return _logger 