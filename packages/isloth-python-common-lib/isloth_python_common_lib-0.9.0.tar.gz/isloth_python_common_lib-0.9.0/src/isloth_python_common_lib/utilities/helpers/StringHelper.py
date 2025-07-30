"""
StringHelper.py
----------------
Provides utility methods for string transformations such as converting
between camelCase and snake_case.
"""


class StringHelper:
    """
    A utility class for string manipulations.

    Methods
    -------
    to_camel_case(s: str) -> str
        Converts a snake_case string to camelCase.
    to_snake_case(s: str) -> str
        Converts a camelCase or PascalCase string to snake_case.
    """

    @staticmethod
    def to_camel_case(s: str) -> str:
        """
        Convert a snake_case string to camelCase.

        Parameters
        ----------
        s : str
            The input string in snake_case.

        Returns
        -------
        str
            The converted string in camelCase.
        """
        parts = s.split('_')
        return parts[0] + ''.join(p.capitalize() for p in parts[1:])

    @staticmethod
    def to_snake_case(s: str) -> str:
        """
        Convert a camelCase or PascalCase string to snake_case.

        Parameters
        ----------
        s : str
            The input string in camelCase or PascalCase.

        Returns
        -------
        str
            The converted string in snake_case.
        """
        result = ''
        for i, c in enumerate(s):
            if c.isupper() and i != 0:
                result += '_'
            result += c.lower()
        return result
