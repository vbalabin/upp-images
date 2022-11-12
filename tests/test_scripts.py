import pytest
from PIL import Image
from src.mscripts import MergerScripts


class TestScripts():
    @classmethod
    def setup_class(cls):
        """
        """
        cls.images = list()
        cls.images.append(Image.open('img/puzzle.ico'))
        cls.images.append(Image.open('img/include.png'))


    @classmethod
    def teardown_class(cls):
        """
        """        

    def test_findfolderpath(self):
        expected = 'E:\\folder1\workdir\\'
        actual = MergerScripts.find_folderpath(r'E:\folder1\workdir\merger.py')
        assert expected == actual

    def test_findfilename(self):
        expected = 'merger.py'
        actual = MergerScripts._find_filename(r'E:\folder1\workdir\merger.py')
        assert expected == actual

    def test_formfilepath(self):
        expected = 'merger.py.png'
        actual = MergerScripts.make_default_concatenation_path(r'merger.py')
        assert expected == actual

    def test_concatenate_h(self):
        expected = 288
        actual = MergerScripts.concatenate_h(self.images, 'white', Image).width
        assert expected == actual
    
    def test_concatenate_v(self):
        expected = 270
        actual = MergerScripts.concatenate_v(self.images, 'white', Image).height
        assert expected == actual

    def test_find_max_width(self):
        expected = 256
        actual = MergerScripts.find_max_width(self.images)
        assert expected == actual

    def test_find_max_height(self):
        expected = 256
        actual = MergerScripts.find_max_height(self.images)
        assert expected == actual

    def test_resize_all_tomax(self):
        expected = 256
        actual = MergerScripts.resize_all_tomax(self.images, 256, Image, True)[1].width
        assert expected == actual

    def test_change_folder_strip_ext(self):
        tested_list = ['D:/images/resized1.png', 'D:/images/resized2.jpg']
        expected = ['G:/my_images/resized1', 'G:/my_images/resized2']
        actual = MergerScripts.change_folder_strip_ext(tested_list, 'G:/my_images/')
        assert expected == actual