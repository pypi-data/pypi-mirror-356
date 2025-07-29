"""file_extension.py

Contains a class that handles file IO for a specific file format.
Class is written as an abstract class.
"""

from abc import ABC, abstractmethod
from pathlib import Path


from typing import Any



class FileExtension(ABC):
    """
    A class that handles file IO for a specific file format.
    

    Attributes
    ----------
    path : pathlib.Path
        Absolute path of the file to be managed.

    extension_suffix : str
        The suffix of the file extension.
    """


    def __init__(
        self, 
        path : Path, 
        extension_suffix : str
    ) -> None:
        """
        Initializes FileExtension instance.

        
        Parameters
        ----------
        path : pathlib.Path
            Absolute path of the file to be managed.

        extension_suffix : str
            The suffix of the file extension.
        """
        
        self.path = path
        self.extension_suffix = extension_suffix
    
    
    @abstractmethod
    def read(self) -> Any:
        """
        Opens the file and returns the data held within.
        """
        pass

    
    @abstractmethod
    def write(self, data: Any) -> bool:
        """
        Writes to the file.
        """
        pass


    def print(self) -> None:
        """
        Opens the file and prints the data held within.
        """
        print(self.read())


    def get_extension_suffix(self) -> str:
        """
        Returns the suffix for this extention (ex. txt, yaml).
        """
        return self.extension_suffix
