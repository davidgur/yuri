from src.image_recon.color_converter import  ColorConverter

import unittest

ColorConverterTest = ColorConverter()

class TestingObscureColors(unittest.TestCase):
    def test(self):
        self.assertEqual(ColorConverterTest.get_color_name((0,0,255)), 'blue')

TestingObscureColors.test()