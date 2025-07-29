"""file_minecraft_dat.py

Contains a class that handles Minecraft dat file IO.
"""

from pathlib import Path

import amulet_nbt
from lunapyutils import handle_error

from .file_dat import DatFile


from amulet_nbt import NamedTag



class MinecraftDatFile(DatFile):
    """
    Class that handles Minecraft dat file IO.

    
    Attributes
    ----------
    path : pathlib.Path
        Absolute path of the file to be managed.
    """


    def __init__(self, path: Path) -> None:
        """
        Initializes MinecraftDatFile instance.

        
        Attributes
        ----------
        path : pathlib.Path
            Absolute path of the file to be managed.
        """
        super().__init__(path = path)


    def read(self) -> NamedTag | None:
        """
        Opens Minecraft dat file and returns its data.

        
        Returns
        -------
        amulet_nbt.NamedTag
            The data contained in the file.
            None, if there was an error.
        """

        data = None
        try:
            data : NamedTag = amulet_nbt.load(str(self.path))

        except IOError as e:
            handle_error(e, 'MinecraftDatFile.open()',
                         'error opening file')

        except Exception as e:
            handle_error(e, 'MinecraftDatFile.open()', 
                         'erroneous error opening file')

        finally:
            return data
        

    def write(self, data: NamedTag) -> bool:
        """
        Writes data to Minecraft dat file. Overwrites all data held in file.

        
        Parameters
        ----------
        data : amulet_nbt.NamedTag
            The data to write to the file.

            
        Returns
        -------
        bool
            True,  if the data was written to the file.
            False, otherwise.
        """

        saved = False
        try: 
            data.save_to(str(self.path))
            saved = True
        
        except Exception as e:
            handle_error(e, 'MinecraftDatFile.write()', 'error writing to file')

        finally:
            return saved
