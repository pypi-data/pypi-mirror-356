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

__version__ = "1.0.0"
__author__ = "tikisan"
__email__ = "s2501082@sendai-nct.jp"

__all__ = [
    "EphemeralDB",
    "EphemeralDBError", 
    "ScopeError",
    "KeyError",
    "ValidationError",
    "CapacityError",
    "ThreadSafetyError",
]