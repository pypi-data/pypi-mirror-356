"""
ILogger.py
----------
Defines the interface for logging messages across the application.
"""

from abc import ABC, abstractmethod


class ILogger(ABC):
    """
    Abstract base class for a logger implementation.

    Methods
    -------
    info(message: str) -> None
        Logs an informational message.
    warn(message: str) -> None
        Logs a warning message.
    error(message: str | Exception) -> None
        Logs an error message.
    """

    @abstractmethod
    def info(self, message: str) -> None:
        """Logs an informational message."""
        pass

    @abstractmethod
    def warn(self, message: str) -> None:
        """Logs a warning message."""
        pass

    @abstractmethod
    def error(self, message: str | Exception) -> None:
        """Logs an error message."""
        pass
