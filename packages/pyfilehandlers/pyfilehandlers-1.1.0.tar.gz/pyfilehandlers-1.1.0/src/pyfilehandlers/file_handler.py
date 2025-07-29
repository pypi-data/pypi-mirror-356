"""file_handler.py

Contains class that handles a single file.
"""

from pathlib import Path

from lunapyutils import handle_error, print_internal

from .file_extension import FileExtension
from .file_dat import DatFile
from .file_minecraft_dat import MinecraftDatFile
from .file_txt import TxtFile
from .file_json import JSONFile
from .file_yaml import YAMLFile


from typing import Any


SCRIPT_ROOT = Path.cwd()



class FileHandler:
    """
    A class that handles a single file's input and output.

    
    Attributes
    ----------
    path : pathlib.Path
        Absolute path of the file to be managed.

    extension : FileExtension
        Handles file IO based on extension type.
    """


    def __init__(
        self, 
        file_path : Path
    ) -> None:
        """
        Initializes a FileHandler instance.

        Either provide a relative or absolute `pathlib.Path` path for the file. 
        Relative paths with be rooted at the current working directory where
        the script was run. If the file does not exist, it will be created.

        
        Parameters
        ----------
        file_path : pathlib.Path
            The relative or absolute path of the file to be managed, 
            including extension.

            
        Raises
        ------
        ValueError
            If the file does not have a FileExtension subclass to handle it.
        """

        self.path : Path = self._resolve_path(file_path)
        self.extension : FileExtension = self._determine_file_extension_object()(self.path)
            
        if not self.file_exists():
            if self.create_file():
                print_internal(f'{self.path} created successfully')
            else:
                print_internal(f'error creating file {self.path}')


    @classmethod
    def from_directory_and_filename(
        cls,
        filename : str, 
        directory : str = 'data'
    ) -> None:
        """
        Initializes a FileHandler instance.

        The file's path will start with the root of the script, and will
        have an optional directory (defaults to `data/`), as well as a
        filename.

        
        Parameters
        ----------
        filename : str
            The name of the file, including extension.

        directory : str, default = 'data'
            The name of the directory to put the file in.
        """
        return cls(
            file_path = Path(SCRIPT_ROOT, directory, filename)
        )


    def _determine_file_extension_object(self) -> FileExtension:
        """
        Determines the appropriate FileExtension subclass to use for this file.

        
        Returns
        -------
        FileHandler
            The appropriate FileExtension subclass for this FileHandler's file.
        
            
        Raises
        ------
        ValueError
            If the file does not have a FileExtension subclass to handle it.
        """

        match self.path.suffix:
            case '.txt'  : return TxtFile
            case '.yaml' : return YAMLFile
            case '.json' : return JSONFile
            case '.dat'  : return self._determine_dat_file_subclass()
            case _: raise ValueError('No FileExtension for given extension')


    def _determine_dat_file_subclass(self) -> DatFile:
        """
        Determines the appropriate DatFile subclass to use for this file.
        

        Returns
        -------
        DatFile
            Subclass that handles the specific format held in the dat file.
        
            
        Raises
        -------
        ValueError
            If the subclass of `DatFile` can not be determined, or if there
            is no existing subclass of `DatFile` to handle the format.
        """

        # only supports Minecraft dat files, if this is to be expanded,
        # there will be some logic to figure out automatically if the
        # given file is a Minecraft dat file or otherwise
        return MinecraftDatFile

    
    def _resolve_path(self, given_path : Path) -> Path:
        """
        Returns an absolute path to a file.
        

        Parameters
        ----------
        given_path : pathlib.Path
            The absolute or relative path of the file.
        
            
        Returns
        -------
        pathlib.Path
            The absolute path of the file.
        """

        if given_path.is_absolute():
            return given_path
        
        return given_path.resolve()


    @staticmethod
    def create_dir(dir_path : str) -> bool: 
        """
        Creates directory based at the root of the script.

        
        Parameters
        ----------
        dir_path : str
            Path of the directory to be created.
            

        Returns
        -------
        bool
            True,  if the directory was created successfully or already exists.
            False, otherwise.
        """

        created = False
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            created = True

        except FileExistsError:
            created = True

        except Exception as e:
            handle_error(e, 'FileHandler.create_dir()', 
                        'erroneous error creating data directory')

        finally:
            return created


    def create_file(self) -> bool:
        """
        Creates file at path specified in the `path` attribute.

        
        Returns
        -------
        bool
            True,  if file was created successfully.
            False, otherwise.
        """

        file_created_successfully = False
        try:
            with open(self.path, 'a+'):
                file_created_successfully = True

        except FileNotFoundError:
            if not FileHandler.create_dir(self.path.parent):
                return False

            return self.create_file()

        except IOError as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'error creating file')

        except Exception as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'erroneous error creating file')

        return file_created_successfully
        

    def file_exists(self) -> bool:
        """
        Determines if file exists.

        
        Returns
        -------
        bool
            True,  if file exists.
            False, otherwise.
        """
        return self.path.exists()
    

    def is_empty(self) -> bool:
        """
        Determins if file is empty.

        
        Returns
        -------
        bool
            True,  if file is empty.
            False, otherwise.
        """

        return self.path.stat().st_size == 0
    

    def read(self) -> Any | None:
        """
        Opens file and returns its data.

        
        Returns
        -------
        Any
            The data held in the file.
            None, if file is empty.

        Raises
        ------
        PermissionError
            If process does not have the permission to read from the file.
        """

        try:
            open(self.path, mode='r')
        
        except PermissionError:
            raise PermissionError(f'Lacking permissions to read from file {self.path}')

        else:
            if self.is_empty():
                return None
            return self.extension.read()
    

    def write(self, data: Any) -> bool:
        """
        Writes data to file.

        
        Parameters
        ----------
        data : Any
            Data to write to the file.

        
        Returns
        -------
        bool
            True,  if the data was written to the file successfully.
            False, otherwise.


        Raises
        ------
        PermissionError
            If process does not have the permission to write to the file.
        """

        try:
            open(self.path, mode='w')

        except PermissionError:
            raise PermissionError(f'Lacking permissions to write to file {self.path}')
        
        else:
            return self.extension.write(data)
    
    
    def print(self) -> None:
        """
        Prints the data held in the file to standard out.

        
        Raises
        ------
        PermissionError
            If process does not have the permission to read from the file.
        """

        try:
            self.extension.print()
            
        except PermissionError:
            raise PermissionError(f'Lacking permissions to read from file {self.path}')