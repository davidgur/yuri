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
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


def find_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist


def determine_color(frame, box):
    left = box[0]
    top = box[1]
    width = box[2]
    height = box[3]

    frame_copy = frame.copy()

    img = frame_copy[top:top+height, left:left+width]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))

    clt = KMeans(n_clusters=3)
    clt.fit(img)

    hist = find_histogram(clt)
    colors = [tuple(color.astype("uint8")) for (percent, color) in zip(hist, clt.cluster_centers_)]

    return colors

