import tkinter as tk
from unittest.mock import patch
from merger import ImageMerger
from src.mscripts import MergerScripts

class TestMerger():
    @classmethod
    def setup_class(cls):
        cls.root = tk.Tk()
        cls.app = ImageMerger(cls.root)

    @classmethod
    def teardown_class(cls):
        cls.root.destroy()   

    def test_biscale_property(self):
        self.app.bs_concat.variable = False
        expected = False
        actual = self.app.bs_concat.variable
        assert expected == actual
        
    def test_dir_entry_property(self):
        self.app.direntry.variable = 'property'
        expected = 'property'
        actual = self.app.direntry.variable
        assert expected == actual

    def test_call_askdir(self):
        with patch('merger.askdirectory', return_value='D:/root_folder/Folder'):
            self.app._call_askdir()
            expected = r'D:\root_folder\Folder\result.png'
            actual = self.app.direntry.variable
            assert expected == actual