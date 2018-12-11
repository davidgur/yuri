"""
color_converter.py

Takes RGB tuple input and converts into color. (str)

Author: Kenan Liu
Date Started: December 11th, 2018

------------------------------------
YURI (Your Useless Recognizer of Images)
Copyright (C) 2018 David Gurevich, Kenan Liu
"""

class ColorConverter:

    def __init__(self):
        '''
        Initiallizes ColorConverter Class
        Using RGB and color values
        '''
        self.rgb = ()
        self.color = ''

    def tuple_check(self, rgb):
        '''
        Method takes an input, checks if the input is a tuple, and returns boolean value.

        (input) --> (bool)
        '''
        if isinstance(rgb, tuple):
            return True

        else:
            return False

    def round_tuple(self, rgb):
        '''
        Method takes an RGB tuple, extracts each RGB value, rounds them individually, and returns a rounded RGB tuple.

        (tuple) --> (tuple)
        '''
        r, g, b = rgb
        round(r)
        round(g)
        round(b)
        self.rgb = (r, g, b)

        return self.rgb

    def get_color(self, rgb):
        #
        #
        #LOOTTAAAAA WORKKK HEREEEEEEEEEE GOOGLE IT LATER
        #
        #
        return "color_here"
        pass

    def convert_RGB(self, rgb):

        if self.tuple_check(rgb):
            self.round_tuple(rgb)
            self.color = self.get_color(rgb)

            return self.color
