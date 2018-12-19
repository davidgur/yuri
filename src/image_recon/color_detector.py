"""
color_detector.py

Starts the Flask server. Interface between the front-end and back-end.

Author: David Gurevich, Kenan Liu
Date Started: December 9th, 2018

------------------------------------
YURI (Your Useless Recognizer of Images)
Copyright (C) 2018 David Gurevich, Kenan Liu
"""

import cv2
import numpy as np

from sklearn.cluster import KMeans

class ColorDetector:
    def __init__(self):
        self.roi = None
        self.clt = KMeans(n_clusters=1)

    def set_roi(self, roi):
        self.roi = roi

    def increase_contrast(self, input_img):
        self.img = input_img

        brightness = 0
        contrast = 48

        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255
            gamma_b = shadow

            buf = cv2.addWeighted(self.img, alpha_b, self.img, 0, gamma_b)
        else:
            buf = self.img.copy()

        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

        return buf

    def find_histogram(self):
        numLabels = np.arange(0, len(np.unique(self.clt.labels_)) + 1)
        (hist, _) = np.histogram(self.clt.labels_, bins=numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()
        return hist

    def determine_color(self):
        self.clt.fit(self.roi)

        hist = self.find_histogram()
        colors = [color.astype("uint8")[::-1] for (percent, color) in zip(hist, self.clt.cluster_centers_)]
        colors = tuple(np.asscalar(val) for val in colors[0][::-1])

        return colors