"""file_dat.py

Contains a class that handles dat file IO.
Class is written as an abstract class.
"""

from pathlib import Path

from .file_extension import FileExtension



class DatFile(FileExtension):
    """
    Class that handles dat file IO.


    Attributes
    ----------
    path : pathlib.Path
        Absolute path of the file to be managed.
    """


    def __init__(self, path: Path) -> None:
        """
        Initializes DatFile instance.


        Attributes
        ----------
        path : pathlib.Path
            Absolute path of the file to be managed.
        """
        super().__init__(path = path, extension_suffix = '.dat')
