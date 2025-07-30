"""
ErrorCode.py
------------
Defines standardized error codes used across iSloth backend services.
"""

from enum import Enum


class ErrorCode(str, Enum):
    """
    Enum representing standardized semantic error codes shared across services.

    Attributes
    ----------
    INVALID_INPUT : str
        Generic client error due to invalid input.
    VALIDATION : str
        Input failed schema or business validation.
    REQUIRED_INPUT : str
        A required input field is missing.
    UNAUTHORIZED : str
        Request lacks valid authentication credentials.
    NOT_FOUND : str
        Requested resource is not found.
    FORBIDDEN : str
        Access is denied due to permission rules.
    CONFLICT : str
        Conflict occurred, such as a duplicate entry.
    INTERNAL_SERVER_ERROR : str
        Unhandled exception on server side.
    NOT_IMPLEMENTED : str
        Requested endpoint or feature not implemented.
    SERVICE_UNAVAILABLE : str
        Backend temporarily unavailable.
    GATEWAY_TIMEOUT : str
        Backend service did not respond in time.
    DATABASE_ERROR : str
        Internal database failure.
    EXTERNAL_SERVICE_ERROR : str
        Third-party API failure.
    LIBRARY_ERROR : str
        Internal library failure.
    UNKNOWN_ERROR : str
        Unclassified or fallback error.
    """

    INVALID_INPUT = 'INVALID_INPUT'
    VALIDATION = 'VALIDATION'
    REQUIRED_INPUT = 'REQUIRED_INPUT'
    UNAUTHORIZED = 'UNAUTHORIZED'
    NOT_FOUND = 'NOT_FOUND'
    FORBIDDEN = 'FORBIDDEN'
    CONFLICT = 'CONFLICT'
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    NOT_IMPLEMENTED = 'NOT_IMPLEMENTED'
    SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE'
    GATEWAY_TIMEOUT = 'GATEWAY_TIMEOUT'
    DATABASE_ERROR = 'DATABASE_ERROR'
    EXTERNAL_SERVICE_ERROR = 'EXTERNAL_SERVICE_ERROR'
    LIBRARY_ERROR = 'LIBRARY_ERROR'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
