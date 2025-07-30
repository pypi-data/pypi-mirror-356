"""
Convertor.py
------------
Utility functions for type and structure conversion.
"""


class Convertor:
    """
    Provides utility methods for converting values and transforming structures.

    Methods
    -------
    to_json(obj: any) -> any
        Parses a string to a JSON object if necessary.
    to_number(val: str) -> float | None
        Converts a string to a float, or None if input is falsy.
    to_records(obj: dict, parent_field: str) -> dict[str, any]
        Converts a dictionary to a flattened record for MongoDB-style updates.
    """

    @staticmethod
    def to_json(obj: any) -> any:
        """
        Converts a JSON string to a dictionary if needed.

        Parameters
        ----------
        obj : any
            A JSON string or already-parsed object.

        Returns
        -------
        any
            Parsed JSON object if string, else original input.
        """
        import json
        return json.loads(obj) if isinstance(obj, str) else obj

    @staticmethod
    def to_number(val: str) -> float | None:
        """
        Converts a string to a float.

        Parameters
        ----------
        val : str
            The value to convert.

        Returns
        -------
        float or None
            The parsed number, or None if input is falsy.
        """
        return float(val) if val else None

    @staticmethod
    def to_records(obj: dict, parent_field: str) -> dict[str, any]:
        """
        Converts nested fields into dot notation for MongoDB-style updates.

        Parameters
        ----------
        obj : dict
            The dictionary with fields to convert.
        parent_field : str
            The parent path under which to nest each field.

        Returns
        -------
        dict[str, any]
            Flattened update dictionary suitable for MongoDB's $set.
        """
        return {
            f"{parent_field}.$.{key}": value
            for key, value in obj.items()
            if key != 'id'
        }
