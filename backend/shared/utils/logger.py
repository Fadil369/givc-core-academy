"""
Structured logging setup for BrainSAIT LINC agents
"""

import logging
import sys
from typing import Any, Dict
import structlog

from shared.config.settings import settings


def setup_logger(name: str) -> structlog.BoundLogger:
    """Setup structured logger with HIPAA compliance"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger(name)


def get_logger(name: str) -> structlog.BoundLogger:
    """Get logger instance"""
    return structlog.get_logger(name)
