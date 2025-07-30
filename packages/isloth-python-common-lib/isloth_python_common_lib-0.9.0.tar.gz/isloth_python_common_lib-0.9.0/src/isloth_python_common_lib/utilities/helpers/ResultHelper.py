"""
Result.py
---------
Defines a standardized result object for API responses or internal method returns.
"""

from typing import Any, Optional
from isloth_python_common_lib.types.ErrorMessage import ErrorMessage


class Result:
    """
    A standardized response wrapper indicating success or failure.

    Attributes
    ----------
    success : bool
        Indicates whether the operation was successful.
    message : str
        A message describing the result.
    data : Optional[Any]
        Optional data payload associated with the result.
    errors : list[ErrorMessage]
        List of error messages if the operation failed.
    """

    def __init__(self) -> None:
        self.success: bool = False
        self.message: str = ''
        self.data: Optional[Any] = None
        self.errors: list[ErrorMessage] = []

    def add_errors(self, errors: list[ErrorMessage]) -> None:
        """
        Appends a list of error messages to the result.

        Parameters
        ----------
        errors : list[ErrorMessage]
            A list of error message dictionaries to attach to the result.
        """
        self.errors.extend(errors)

