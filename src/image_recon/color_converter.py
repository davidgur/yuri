"""
color_converter.py

Takes RGB tuple input and converts into color. (str)

Author: Kenan Liu
Date Started: December 11th, 2018

------------------------------------
YURI (Your Useless Recognizer of Images)
Copyright (C) 2018 David Gurevich, Kenan Liu
"""
import json

import webcolors


class ColorConverter:

    def __init__(self):
        """
        Initializes ColorConverter Class
        Using RGB and color values
        """
        self.rgb = ()
        self.webcolors = {}
        self.closest_color = 'None'
        self.color_name = 'None'


    def get_webcolors(self, file):
        """
        Method takes JSON file and converts it into a python dictionary.
        Sets the self.webcolors variable, however returns None.

        (str) --> (dict)
        """
        with open(file) as json_file:
            self.webcolors = json.load(json_file)


    def tuple_check(self, rgb):
        """
        Method takes an input, checks if the input is a tuple, and returns boolean value.

        (tuple) --> (bool)
        """
        if isinstance(rgb, tuple):
            return True

        else:
            return False


    def tuple_correction(self, rgb):
        """
        Method takes an RGB tuple, extracts each RGB value, rounds them individually, and returns a rounded RGB tuple.
        Method returns (0,0,0) if the tuple is not RGB compatible and prints in the shell.

        (tuple) --> (tuple)
        """

        if len(rgb) != 3:
            ############ADD CLASS DAVID SAID ABOUT EXCEPTIONS
            print('Tuple is not RGB compatible')
            self.rgb = (255, 255, 255)
            return self.rgb

        r, g, b = rgb
        r = round(r)
        g = round(g)
        b = round(b)

        if r > 255 or r < 0 or g > 255 or g < 0 or b > 255 or b < 0:
            ############ADD CLASS DAVID SAID ABOUT EXCEPTIONS
            print('Tuple is not RGB compatible')
            self.rgb = (255, 255, 255)
            return self.rgb

        else:
            self.rgb = (r, g, b)
            return self.rgb


    def get_closest_color(self, rgb, color_file):
        """
        Method takes an RGB tuple and JSON file as inputs.
        Method calls other methods to ensure everything is compatible.
        Method converts RGB into HEX and searches the 'webcolors' database and sets the closest common color name.
        Method then searches JSON file dictionary for the common general name for the closest name.

        (tuple) (json_file) --> (str)
        """
        self.rgb = rgb
        self.get_webcolors(color_file)

        if self.tuple_check(self.rgb):
            self.tuple_correction(self.rgb)
            min_colours = {}
            for key, name in webcolors.css3_hex_to_names.items():
                r_c, g_c, b_c = webcolors.hex_to_rgb(key)
                rd = (r_c - self.rgb[0]) ** 2
                gd = (g_c - self.rgb[1]) ** 2
                bd = (b_c - self.rgb[2]) ** 2
                min_colours[(rd + gd + bd)] = name

            self.closest_color = min_colours[min(min_colours.keys())]
            self.color_name = self.webcolors[self.closest_color]

            return self.color_name

        else:
            return 'Error Converting Color!'
