"""
DetailLevel.py
--------------
Defines levels of detail for API responses or internal queries.
"""

from enum import Enum


class DetailLevel(str, Enum):
    """
    Enum representing the granularity of a response payload.

    Attributes
    ----------
    OVERVIEW : str
        Minimal summary information only.
    DETAIL : str
        Full detailed response with all fields.
    """

    OVERVIEW = 'OVERVIEW'
    DETAIL = 'DETAIL'
