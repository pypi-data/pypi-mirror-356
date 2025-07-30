"""
ServiceUnavailableError.py
--------------------------
Defines a 503 error when a dependent service or component is unavailable.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class ServiceUnavailableError(AppError):
    """
    Raised when a required service is temporarily down or unreachable.

    Attributes
    ----------
    service : str
        The name of the unavailable service.
    status_code : StatusCode
        Always 503 (SERVICE_UNAVAILABLE).
    details : Any, optional
        Extra error metadata (stack trace, logs, etc.).
    """

    def __init__(self, service: str, details: Optional[Any] = None):
        super().__init__(f'{service} is unavailable', StatusCode.SERVICE_UNAVAILABLE, details)
        self.add_error({
            'code': ErrorCode.SERVICE_UNAVAILABLE.value,
            'field': service,
            'message': f'{service} is currently down'
        })
