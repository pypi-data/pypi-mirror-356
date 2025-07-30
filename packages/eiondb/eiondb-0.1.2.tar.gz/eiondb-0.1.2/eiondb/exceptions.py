"""
Eion SDK Exceptions

Custom exception classes for the Eion Python SDK.
"""

from typing import Optional, Dict, Any


class EionError(Exception):
    """Base exception for all Eion SDK errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class EionAuthenticationError(EionError):
    """Raised when authentication fails."""
    pass


class EionValidationError(EionError):
    """Raised when request validation fails."""
    pass


class EionNotFoundError(EionError):
    """Raised when a resource is not found."""
    pass


class EionServerError(EionError):
    """Raised when the server returns a 5xx error."""
    pass


class EionConnectionError(EionError):
    """Raised when connection to the server fails."""
    pass


class EionTimeoutError(EionError):
    """Raised when a request times out."""
    pass 