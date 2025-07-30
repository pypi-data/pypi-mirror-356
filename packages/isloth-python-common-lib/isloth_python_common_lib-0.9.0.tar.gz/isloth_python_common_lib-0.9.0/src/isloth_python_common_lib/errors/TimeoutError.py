"""
TimeoutError.py
---------------
Defines a 504-style error raised when an operation times out.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class TimeoutError(AppError):
    """
    Raised when a request or internal operation exceeds the time limit.

    Attributes
    ----------
    source : str
        The source or component that timed out.
    message : str
        The message to include in the error.
    status_code : StatusCode
        Uses 500 (INTERNAL_SERVER_ERROR) to remain consistent with internal errors.
    details : Any, optional
        Additional metadata or debugging info.
    """

    def __init__(self, source: str, message: str = 'Request timed out.', details: Optional[Any] = None):
        super().__init__(message, StatusCode.INTERNAL_SERVER_ERROR, details)
        self.add_error({
            'code': ErrorCode.GATEWAY_TIMEOUT.value,
            'field': source,
            'message': message
        })
