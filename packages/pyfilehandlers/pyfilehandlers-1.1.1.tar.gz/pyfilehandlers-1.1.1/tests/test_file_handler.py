from src.pyfilehandlers.file_handler import FileHandler
from src.pyfilehandlers.file_txt import TxtFile
from src.pyfilehandlers.file_json import JSONFile

from pathlib import Path
import pytest



class TestFileHandler:


    def test_from_directory_and_filename_default_directory(self):
        path_to_test = Path(Path.cwd(), 'data', 'testfile.txt')

        fh : FileHandler = FileHandler.from_directory_and_filename(
            filename = 'testfile.txt'
        )
        assert fh.path == path_to_test

        Path.unlink(path_to_test)



    def test__determine_file_extension_object_TxtFile(self):
        path_to_test = Path('test.txt')

        fh = FileHandler(path_to_test)
        assert fh._determine_file_extension_object() == TxtFile

        Path.unlink(path_to_test)

    def test__determine_file_extension_object_JSONFile(self):
        path_to_test = Path('test.json')

        fh = FileHandler(path_to_test)
        assert fh._determine_file_extension_object() == JSONFile

        Path.unlink(path_to_test)

    def test__determine_file_extension_object_no_ext_handler(self):
        with pytest.raises(ValueError):
            FileHandler(Path('test.sh'))
