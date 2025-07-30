"""
InternalServerError.py
----------------------
Defines a 500 error raised when an unexpected server failure occurs.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class InternalServerError(AppError):
    """
    Raised when an unhandled exception or unknown failure occurs.

    Attributes
    ----------
    message : str
        Always "Internal server error".
    status_code : StatusCode
        Always 500 (INTERNAL_SERVER_ERROR).
    details : Any, optional
        Additional error context or debugging metadata.
    """

    def __init__(self, details: Optional[Any] = None):
        super().__init__('Internal server error', StatusCode.INTERNAL_SERVER_ERROR, details)
        self.add_error({
            'code': ErrorCode.INTERNAL_SERVER_ERROR.value,
            'field': 'server',
            'message': 'Something went wrong'
        })
