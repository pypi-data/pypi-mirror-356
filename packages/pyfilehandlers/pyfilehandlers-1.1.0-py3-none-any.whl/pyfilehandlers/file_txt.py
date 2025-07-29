"""file_txt.py

Contains a class that handles txt file IO.
"""

from pathlib import Path

from lunapyutils import handle_error

from .file_extension import FileExtension



class TxtFile(FileExtension):
    """
    Class that handles txt file IO.


    Attributes
    ----------
    path : pathlib.Path
        Absolute path of the file to be managed.
    """


    def __init__(self, path: Path) -> None:
        """
        Creates TxtFile instance.

        
        Attributes
        ----------
        path : pathlib.Path
            Absolute path of the file to be managed.
        """
        super().__init__(path = path, extension_suffix = '.txt')


    def read(self) -> list[str] | None:
        """
        Opens txt file and returns its data.

        
        Returns
        -------
        list[str]
            The data contained in the file.
            None, if there was an error.
        """

        data = None
        try:
            with open(self.path, 'r') as f:
                data = f.readlines()

        except IOError as e:
            handle_error(e, 'TxtFile.open()',
                         'error opening file')

        except Exception as e:
            handle_error(e, 'TxtFile.open()', 
                         'erroneous error opening file')

        finally:
            return data
        

    def write(self, data: list[str] | str) -> bool:
        """
        Writes data to txt file. Overwrites all data held in file.

        
        Parameters
        ----------
        data : list[str] | str
            The data to write to the file.

            
        Returns
        -------
        bool
            True,  if the data was written to the file.
            False, otherwise.
        """

        saved = False
        try: 
            with open(self.path, 'w') as f:
                if isinstance(data, list):
                    f.writelines(line + '\n' for line in data)
                else:
                    f.write(data)
                saved = True
        
        except Exception as e:
            handle_error(e, 'TxtFile.write()', 'error writing to file')

        finally:
            return saved
        
    
    def print(self) -> None:
        """
        Opens the text file and prints the data.
        """
        
        data = self.read()
        print(data)
