"""
IObjectProcessor.py
--------------------
Defines the interface for object processors used by image-processing-service
to interact with the text-processing-service in a standardized way.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict


class IObjectProcessor(ABC):
    """
    Interface for object processors used in cross-service calls between image and text processing services.
    """

    @abstractmethod
    def process_objects(self, object_data: Dict[str, Any]) -> List[dict[str, Any]]:
        """
        Process objects extracted from an image to detect products using BLIP captioning and helper logic.

        Parameters
        ----------
        object_data : dict
            Dictionary containing metadata and the cropped object from the original image (e.g., PIL.Image.Image).

        Returns
        -------
        List[dict[str, Any]]
            List of detected product combinations with attributes.
        """
        pass
