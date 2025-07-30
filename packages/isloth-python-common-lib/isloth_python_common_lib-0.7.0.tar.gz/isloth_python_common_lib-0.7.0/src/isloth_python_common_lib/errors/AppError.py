"""
AppError.py
-----------
Abstract base class for application-specific exceptions.
Provides structured error metadata such as status code, details, and validation errors.
"""

from typing import Any, List, Optional
from isloth_python_common_lib.enums.StatusCode import StatusCode


class AppError(Exception):
    """
    Base class for structured application errors.

    Attributes
    ----------
    message : str
        Human-readable error message.
    status_code : StatusCode
        HTTP status code to associate with the error.
    details : Any, optional
        Additional metadata about the error context.
    errors : List[Any]
        Optional list of error messages for validation errors.
    """

    def __init__(self, message: str, status_code: StatusCode = StatusCode.INTERNAL_SERVER_ERROR, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details
        self.errors: List[Any] = []

    def add_error(self, error: Any) -> "AppError":
        """
        Add a single error message to the list.

        Parameters
        ----------
        error : Any
            Error message or object.

        Returns
        -------
        AppError
            This instance for chaining.
        """
        self.errors.append(error)
        return self

    def set_errors(self, errors: List[Any]) -> "AppError":
        """
        Set the full error list.

        Parameters
        ----------
        errors : List[Any]
            List of validation errors.

        Returns
        -------
        AppError
            This instance for chaining.
        """
        self.errors = errors
        return self

    def has_error(self) -> bool:
        """
        Check if validation errors exist.

        Returns
        -------
        bool
            True if any validation errors exist.
        """
        return bool(self.errors)

    def to_dict(self) -> dict:
        """
        Convert exception to dictionary format.

        Returns
        -------
        dict
            Dictionary representation of the error.
        """
        return {
            'name': self.__class__.__name__,
            'status_code': self.status_code.value,
            'message': self.message,
            'details': self.details,
            'errors': self.errors,
        }
