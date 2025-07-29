from src.pyfilehandlers.file_dat import DatFile
import pytest

class TestAbstractClasses:

    def test_DatFile(self) -> None:
        with pytest.raises(Exception):
            DatFile()