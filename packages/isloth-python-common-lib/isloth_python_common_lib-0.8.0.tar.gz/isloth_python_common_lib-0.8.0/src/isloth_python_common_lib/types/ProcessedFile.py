"""
ProcessedFile.py
----------------
Defines a standardized structure for passing file metadata and content between AI backend services.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, validator
from isloth_python_common_lib.types.abstracts.BaseBuilder import BaseBuilder


class ProcessedFileModel(BaseModel):
    """
    Represents a processed file exchanged between services (image, audio, text).

    Attributes
    ----------
    filename : str
        The original or generated file name.
    mimetype : str
        The MIME type (e.g., 'audio/wav', 'image/jpeg').
    size : int
        File size in bytes.
    content : Any, optional
        Raw content or reference (e.g., bytes, path, S3 URI).
    """
    filename: str = Field(..., min_length=1)
    mimetype: str
    size: int = Field(..., gt=0)
    content: Optional[Any] = None

    @validator('mimetype')
    def validate_mimetype(cls, v: str) -> str:
        if not v.startswith(('audio/', 'video/', 'image/', 'application/')):
            raise ValueError('Invalid mimetype')
        return v


class ProcessedFileBuilder(BaseBuilder[ProcessedFileModel]):
    """
    Builder class for creating ProcessedFileModel instances.
    """

    def __init__(self) -> None:
        """
        Initializes the builder with the ProcessedFileModel schema.
        """
        super().__init__(ProcessedFileModel)

    def set_filename(self, filename: str) -> 'ProcessedFileBuilder':
        """
        Sets the file name.

        Parameters
        ----------
        filename : str
            The file name to assign.

        Returns
        -------
        ProcessedFileBuilder
            The current builder instance.
        """
        self.data['filename'] = filename
        return self

    def set_mimetype(self, mimetype: str) -> 'ProcessedFileBuilder':
        """
        Sets the file mimetype.

        Parameters
        ----------
        mimetype : str
            The MIME type of the file.

        Returns
        -------
        ProcessedFileBuilder
            The current builder instance.
        """
        self.data['mimetype'] = mimetype
        return self

    def set_size(self, size: int) -> 'ProcessedFileBuilder':
        """
        Sets the file size.

        Parameters
        ----------
        size : int
            The size of the file in bytes.

        Returns
        -------
        ProcessedFileBuilder
            The current builder instance.
        """
        self.data['size'] = size
        return self

    def set_content(self, content: Any) -> 'ProcessedFileBuilder':
        """
        Sets the file content or reference.

        Parameters
        ----------
        content : Any
            Raw bytes, file path, or S3 URI.

        Returns
        -------
        ProcessedFileBuilder
            The current builder instance.
        """
        self.data['content'] = content
        return self
