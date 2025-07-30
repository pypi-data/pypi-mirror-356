"""
Assertion.py
------------
Provides assertion utilities for common validations.
"""

from isloth_python_common_lib.errors.NotFoundError import NotFoundError


class Assertion:
    """
    A utility class for performing common assertions.
    """

    @staticmethod
    def exists(value: object, resource: str = 'resource') -> object:
        """
        Asserts that the given value exists (i.e., is not None).

        Parameters
        ----------
        value : object
            The value to check for existence.
        resource : str, optional
            The name of the resource being asserted. Used in the error message.

        Returns
        -------
        object
            The original value if it is not None.

        Raises
        ------
        NotFoundError
            If the value is None or undefined.
        """
        if value is None:
            raise NotFoundError(resource)
        return value
