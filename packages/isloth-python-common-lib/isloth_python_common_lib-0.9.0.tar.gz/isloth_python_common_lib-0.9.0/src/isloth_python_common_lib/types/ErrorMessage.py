"""
ErrorMessage.py
---------------
Defines the schema and builder for structured error messages used across services.
"""

from pydantic import BaseModel, Field
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.types.abstracts.BaseBuilder import BaseBuilder


class ErrorMessage(BaseModel):
    """
    Represents a structured error message.

    Attributes
    ----------
    code : ErrorCode
        Enum indicating the type of error.
    source : str
        The component or field where the error originated.
    message : str
        Human-readable explanation of the error.
    """
    code: ErrorCode
    source: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ErrorMessageBuilder(BaseBuilder[ErrorMessageModel]):
    """
    Builder class for constructing ErrorMessageModel instances.
    """

    def __init__(self) -> None:
        super().__init__(ErrorMessageModel)

    def set_code(self, code: ErrorCode) -> 'ErrorMessageBuilder':
        """
        Sets the error code.

        Parameters
        ----------
        code : ErrorCode
            The error code to set.

        Returns
        -------
        ErrorMessageBuilder
            The current builder instance.
        """
        self.data['code'] = code
        return self

    def set_source(self, source: str) -> 'ErrorMessageBuilder':
        """
        Sets the error source.

        Parameters
        ----------
        source : str
            The source string indicating the origin of the error.

        Returns
        -------
        ErrorMessageBuilder
            The current builder instance.
        """
        self.data['source'] = source
        return self

    def set_message(self, message: str) -> 'ErrorMessageBuilder':
        """
        Sets the error message.

        Parameters
        ----------
        message : str
            The message describing the error.

        Returns
        -------
        ErrorMessageBuilder
            The current builder instance.
        """
        self.data['message'] = message
        return self
