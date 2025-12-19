"""
Helper utility functions
"""

from uuid import uuid4
from datetime import datetime
from typing import Optional


def generate_request_id() -> str:
    """Generate unique request ID"""
    return str(uuid4())


def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat()


def parse_datetime(dt_string: str) -> Optional[datetime]:
    """Parse ISO datetime string"""
    try:
        return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return None
