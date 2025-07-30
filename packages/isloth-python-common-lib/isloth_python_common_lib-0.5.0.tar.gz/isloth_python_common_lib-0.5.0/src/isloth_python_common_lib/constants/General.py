"""
General.py
----------
Defines general-purpose constants used across services.
"""


class General:
    """
    General-purpose constants shared across microservices.

    Attributes
    ----------
    DATE_FORMAT : str
        Format for representing dates, e.g., '2024-06-19'.
    TIME_FORMAT : str
        Format for representing time, e.g., '23:59:59Z'. 'Z' indicates UTC timezone.
    """

    DATE_FORMAT: str = '%Y-%m-%d'
    TIME_FORMAT: str = '%H:%M:%SZ'
