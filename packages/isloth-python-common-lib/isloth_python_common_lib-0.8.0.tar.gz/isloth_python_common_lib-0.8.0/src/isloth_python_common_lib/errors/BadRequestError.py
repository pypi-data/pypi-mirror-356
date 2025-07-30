"""
BadRequestError.py
------------------
Defines a 400 error for input validation failures. This exception is used
when the client sends malformed or invalid data, such as missing fields,
type mismatches, or failed schema validation.

This class extends AppError and adds helper methods for attaching
structured validation error metadata.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class BadRequestError(AppError):
    """
    Raised when input validation fails in a request.

    This exception is typically used when FastAPI or pydantic schema validation
    fails, or when additional application-level input validation fails.

    Attributes
    ----------
    message : str
        Always set to "Validation failed".
    status_code : StatusCode
        Always set to 400 (BAD_REQUEST).
    details : Any, optional
        Optional extra metadata to describe the error context.
    errors : list
        A list of structured field-level error messages.
    """

    def __init__(self, details: Optional[Any] = None):
        super().__init__('Validation failed', StatusCode.BAD_REQUEST, details)

    def add_error(self, error: Any) -> 'BadRequestError':
        """
        Add a custom error message object.

        Parameters
        ----------
        error : Any
            A structured error dictionary.

        Returns
        -------
        BadRequestError
            This instance (chained).
        """
        super().add_error(error)
        return self

    def add_errors(self, errors: list[dict]) -> 'BadRequestError':
        """
        Add multiple structured errors.

        Parameters
        ----------
        errors : list of dict
            Each error should follow the structure { code, field, message }.

        Returns
        -------
        BadRequestError
            This instance (chained).
        """
        for error in errors:
            self.add_error(error)
        return self

    def add_invalid_input_error(self, field: str, value: str) -> 'BadRequestError':
        """
        Add a single invalid input error.

        Parameters
        ----------
        field : str
            Name of the invalid field.
        value : str
            Value that caused the error.

        Returns
        -------
        BadRequestError
            This instance (chained).
        """
        return self.add_error({
            'code': ErrorCode.INVALID_INPUT.value,
            'field': field,
            'message': f'{value} is invalid'
        })

    def add_required_input_error(self, field: str) -> 'BadRequestError':
        """
        Add a missing/required field error.

        Parameters
        ----------
        field : str
            Name of the missing field.

        Returns
        -------
        BadRequestError
            This instance (chained).
        """
        return self.add_error({
            'code': ErrorCode.REQUIRED_INPUT.value,
            'field': field,
            'message': f'{field} is required'
        })

    def add_conflict_error(self, field: str, value: str) -> 'BadRequestError':
        """
        Add a conflict error (e.g., duplicate value).

        Parameters
        ----------
        field : str
            Name of the conflicting field.
        value : str
            Conflicting value.

        Returns
        -------
        BadRequestError
            This instance (chained).
        """
        return self.add_error({
            'code': ErrorCode.CONFLICT.value,
            'field': field,
            'message': f'{value} already exists'
        })

    def add_validation_errors(self, issues: list[dict]) -> 'BadRequestError':
        """
        Add a list of validation errors (from schema or custom validators).

        Parameters
        ----------
        issues : list of dict
            Each issue must have 'field' and 'message' keys.

        Returns
        -------
        BadRequestError
            This instance (chained).
        """
        for issue in issues:
            self.add_error({
                'code': ErrorCode.VALIDATION.value,
                'field': issue['field'],
                'message': issue['message']
            })
        return self
