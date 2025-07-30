"""
UnexpectedError.py
------------------
Defines a 500 error raised when an unknown or unhandled exception occurs.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class UnexpectedError(AppError):
    """
    Raised when an unanticipated exception is caught.

    Attributes
    ----------
    status_code : StatusCode
        Always 500 (INTERNAL_SERVER_ERROR).
    details : Any, optional
        Original error object, traceback, or contextual metadata.
    """

    def __init__(self, details: Optional[Any] = None):
        super().__init__('Unexpected error', StatusCode.INTERNAL_SERVER_ERROR, details)
