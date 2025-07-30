"""
NotFoundError.py
----------------
Defines a 404 error for missing resources.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class NotFoundError(AppError):
    """
    Raised when a requested resource cannot be found.

    Parameters
    ----------
    resource : str
        The name or type of the missing resource.
    details : Any, optional
        Additional context or metadata.
    """

    def __init__(self, resource: str, details: Optional[Any] = None):
        super().__init__(f'{resource} not found', StatusCode.NOT_FOUND, details)
        self.add_error({
            'code': ErrorCode.NOT_FOUND.value,
            'field': resource,
            'message': f'{resource} not found'
        })
