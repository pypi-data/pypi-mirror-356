"""
Custom exceptions for EphemeralDB
"""


class EphemeralDBError(Exception):
    """Base exception for EphemeralDB"""
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self):
        result = self.message
        if self.error_code:
            result = f"[{self.error_code}] {result}"
        if self.details:
            result += f" (詳細: {self.details})"
        return result


class ScopeError(EphemeralDBError):
    """Exception raised for scope-related errors"""
    pass


class KeyError(EphemeralDBError):
    """Exception raised for key-related errors"""
    pass


class ValidationError(EphemeralDBError):
    """Exception raised for data validation errors"""
    pass


class CapacityError(EphemeralDBError):
    """Exception raised when capacity limits are exceeded"""
    pass


class ThreadSafetyError(EphemeralDBError):
    """Exception raised for thread safety violations"""
    pass