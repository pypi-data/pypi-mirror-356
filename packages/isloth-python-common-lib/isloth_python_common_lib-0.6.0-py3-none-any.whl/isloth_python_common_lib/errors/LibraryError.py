"""
LibraryError.py
---------------
Defines a 500 error raised when a third-party library fails internally.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class LibraryError(AppError):
    """
    Raised when a third-party Python library causes an exception.

    Attributes
    ----------
    libName : str
        The name of the failing library (e.g., 'whisper', 'torch').
    message : str
        Descriptive message for the library error.
    status_code : StatusCode
        Always 500 (INTERNAL_SERVER_ERROR).
    details : Any, optional
        Tracebacks, logs, or any debugging context.
    """

    def __init__(self, libName: str, message: str = 'Library error', details: Optional[Any] = None):
        super().__init__(message, StatusCode.INTERNAL_SERVER_ERROR, details)
        self.add_error({
            'code': ErrorCode.LIBRARY_ERROR.value,
            'field': libName,
            'message': message
        })
