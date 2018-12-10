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

class DominantColors:

    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None

    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def dominantColors(self):
        #convert to rgb from bgr
        self.IMAGE = cv2.cvtColor(self.IMAGE, cv2.COLOR_BGR2RGB)

        #reshaping to a list of pixels
        self.IMAGE = img.reshape((self.IMAGE.shape[0] * self.IMAGE.shape[1], 3))


        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit(self.IMAGE)

        #the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        #save labels
        self.LABELS = kmeans.labels_

        #returning after converting to integer from float
        return self.COLORS.astype(int)


def determine_color(frame, box):
    left = box[0]
    top = box[1]
    width = box[2]
    height = box[3]

    frame_copy = frame.copy()

    img = frame_copy[top:top+height, left:left+width]
    dc = DominantColors(img, 5)
    colors = dc.dominantColors()
    dc.plotHistogram()
    return (255, 255, 255)
