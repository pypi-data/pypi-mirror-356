"""
ConflictError.py
----------------
Defines a 409 error raised when a resource conflict occurs, such as duplicate data.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class ConflictError(AppError):
    """
    Raised when a resource conflict occurs (e.g., duplicate key, already exists).

    Attributes
    ----------
    message : str
        Description of the conflict. Defaults to "Conflict occurred".
    status_code : StatusCode
        Always set to 409 (CONFLICT).
    details : Any, optional
        Additional context or metadata about the conflict.
    """

    def __init__(self, message: str = 'Conflict occurred', details: Optional[Any] = None):
        super().__init__(message, StatusCode.CONFLICT, details)
        self.add_error({
            'code': ErrorCode.CONFLICT.value,
            'field': 'resource',
            'message': message
        })
