"""
EphemeralDB - A lightweight volatile context management store for Python
"""

from .core import EphemeralDB
from .exceptions import (
    EphemeralDBError, 
    ScopeError, 
    KeyError, 
    ValidationError, 
    CapacityError, 
    ThreadSafetyError
)

__version__ = "0.1.0"
__author__ = "EphemeralDB Team"
__email__ = "info@ephemeraldb.dev"

__all__ = [
    "EphemeralDB",
    "EphemeralDBError", 
    "ScopeError",
    "KeyError",
    "ValidationError",
    "CapacityError",
    "ThreadSafetyError",
]