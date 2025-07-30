"""
ProcessorFactory.py
-------------------
Defines an abstract factory interface for processors used across services.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from isloth_python_common_lib.interfaces.IObjectProcessor import IObjectProcessor
    from isloth_python_common_lib.dtos.ImageProcessorResult import ImageProcessorResult
    from isloth_python_common_lib.dtos.ObjectProcessorResult import ObjectProcessorResult


class ProcessorFactory(ABC):
    """
    Abstract factory interface for processor registration and access across services.
    """

    @abstractmethod
    def get_object_processor(self) -> 'IObjectProcessor':
        """
        Returns an implementation of the IObjectProcessor interface.

        Returns
        -------
        IObjectProcessor
            Instance implementing the object processing logic.
        """
        pass
