"""
SortOrder.py
------------
Defines sort direction options used for ordering queries and results.
"""

from enum import Enum


class SortOrder(str, Enum):
    """
    Enum representing sort direction for ordered data queries.

    Attributes
    ----------
    ASC : str
        Sort results in ascending order (A → Z, 0 → 9).
    DESC : str
        Sort results in descending order (Z → A, 9 → 0).
    """

    ASC = 'ASC'
    DESC = 'DESC'
