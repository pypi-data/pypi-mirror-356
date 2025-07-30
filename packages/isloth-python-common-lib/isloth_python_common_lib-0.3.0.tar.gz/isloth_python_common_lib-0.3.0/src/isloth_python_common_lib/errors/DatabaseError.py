"""
DatabaseError.py
----------------
Defines a 500 error raised when a database operation fails.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class DatabaseError(AppError):
    """
    Raised when a database-related operation encounters an error.

    Attributes
    ----------
    database : str
        The database name (e.g., 'mongo', 'redis').
    table : str
        The affected table, collection, or keyspace.
    operation : str
        The type of operation (e.g., 'insert', 'find', 'delete').
    status_code : StatusCode
        Always 500 (INTERNAL_SERVER_ERROR).
    details : Any, optional
        Contextual error metadata or exception stack trace.
    """

    def __init__(self, database: str, table: str, operation: str, details: Optional[Any] = None):
        message = f'Database error for {operation} on {database}.{table}'
        super().__init__(message, StatusCode.INTERNAL_SERVER_ERROR, details)
        self.add_error({
            'code': ErrorCode.DATABASE_ERROR.value,
            'field': 'database',
            'message': 'A database error occurred'
        })
