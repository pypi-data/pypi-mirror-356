"""
NotImplementedError.py
----------------------
Defines a 501 error raised when a feature is declared but not yet supported.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class NotImplementedError(AppError):
    """
    Raised when a feature or operation is not yet implemented.

    Attributes
    ----------
    source : str
        Identifier for the unimplemented component (e.g., 'audio_translator').
    message : str
        Custom or default error message describing the missing implementation.
    status_code : StatusCode
        Always 501 (NOT_IMPLEMENTED).
    details : Any, optional
        Additional context or traceback data.
    """

    def __init__(self, source: str, message: str = 'This feature is not implemented.', details: Optional[Any] = None):
        super().__init__(message, StatusCode.NOT_IMPLEMENTED, details)
        self.add_error({
            'code': ErrorCode.NOT_IMPLEMENTED.value,
            'field': source,
            'message': message
        })
