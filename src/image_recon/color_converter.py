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
        """
        Initializes ColorConverter Class
        Using RGB and color values
        """
        self.rgb = ()
        self.color = ''

    def tuple_check(self, rgb):
        """
        Method takes an input, checks if the input is a tuple, and returns boolean value.

        (input) --> (bool)
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
            print('Tuple is not RGB compatible')
            return (0,0,0)
        
        r, g, b = rgb
        r = round(r)
        g = round(g)
        b = round(b)

        if r > 255 or r < 0 or g > 255 or g < 0 or b > 255 or b < 0:
            print('Tuple is not RGB compatible')
            return (0,0,0)

        else:
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
            self.tuple_correction(rgb)
            self.color = self.get_color(rgb)

            return self.color

#        import webcolors
#
#        def closest_colour(requested_colour):
#            min_colours = {}
#            for key, name in webcolors.css3_hex_to_names.items():
#                r_c, g_c, b_c = webcolors.hex_to_rgb(key)
#                rd = (r_c - requested_colour[0]) ** 2
#                gd = (g_c - requested_colour[1]) ** 2
#                bd = (b_c - requested_colour[2]) ** 2
#                min_colours[(rd + gd + bd)] = name
#            return min_colours[min(min_colours.keys())]
#
#        def get_colour_name(requested_colour):
#            try:
#                closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
#            except ValueError:
#                closest_name = closest_colour(requested_colour)
#                actual_name = None
#            return actual_name, closest_name
#
#        requested_colour = (119, 172, 152)
#        actual_name, closest_name = get_colour_name(requested_colour)
#
#        print("Actual colour name:", actual_name, ", closest colour name:", closest_name)