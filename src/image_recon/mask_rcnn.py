"""
mask_rcnn.py

Contains ObjectDetector class.

Utilizing Mask R-CNN framework for object instance segmentation.

Author: David Gurevich
Date Started: December 12th, 2018

------------------------------------
YURI (Your Useless Recognizer of Images)
Copyright (C) 2018 David Gurevich
"""

import os.path
import time

import cv2 as cv
import numpy as np
from image_recon.color_converter import ColorConverter
from image_recon.color_detector import ColorDetector


class ObjectDetector:
    """
    This is a class for simple object detection
    with Mask-RCNN
    """

    def __init__(self):
        """
        The constructor of the ObjectDetector class.

        Initializes critical variables and options for the object detector.
        """
        self.confidence_threshold = 0.5
        self.mask_threshold = 0.3

        self.color_detector = ColorDetector()
        self.color_converter = ColorConverter()
        self.colors = "src/image_recon/colors.json"

        self.text_graph = "src/image_recon/models/inception_v2/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"
        self.model_weights = "src/image_recon/models/inception_v2/frozen_inference_graph.pb"

        self.net = cv.dnn.readNetFromTensorflow(self.model_weights, self.text_graph)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        self.frame = None

        self.classes_file = "src/image_recon/models/inception_v2/mscoco_labels.names"
        self.classes = None
        with open(self.classes_file, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

    def get_color_of_prediction(self, frame, left, top, right, bottom, class_mask):
        """
        Given a frame and a mask, return the color of the object inside.
        """

        new_frame = self.color_detector.increase_contrast(frame)

        class_mask = cv.resize(class_mask, (right - left + 1, bottom - top + 1))
        mask = (class_mask > self.mask_threshold)
        roi = new_frame[top:bottom + 1, left:right + 1][mask]

        self.color_detector.set_roi(roi.astype(np.uint8))
        return self.color_detector.determine_color()

    def draw_box(self, frame, class_id, conf, left, top, right, bottom, class_mask, color):
        """
        Draws a box around a detected object with the name of the object and the confidence
        """
        cv.rectangle(frame, (left, top), (right, bottom), color, 3)
        label = "%.2f" % conf
        if self.classes:
            assert (class_id < len(self.classes))
            # label = '%s' % (self.classes[class_id])
            if self.classes[class_id] == "person":
                label = '%s' % (self.classes[class_id])
            else:
                label = '%s %s' % (
                self.color_converter.get_closest_color(color[::-1], self.colors), self.classes[class_id])

        label_size, base_line = cv.getTextSize(label, cv.FONT_HERSHEY_DUPLEX, 0.5, 1)
        top = max(top, label_size[1])
        cv.rectangle(frame, (left, top - round(1.5 * label_size[1])), (left + round(1.5 * label_size[0]),
                                                                       top + base_line), color, cv.FILLED)
        cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
        class_mask = cv.resize(class_mask, (right - left + 1, bottom - top + 1))
        mask = (class_mask > self.mask_threshold)
        roi = frame[top:bottom + 1, left:right + 1][mask]

    def post_process(self, boxes, masks):
        """
        Catch-all function to draw boxes and determine color of objects.
        """
        num_detections = boxes.shape[2]

        colors = []

        frameH = self.frame.shape[0]
        frameW = self.frame.shape[1]

        for i in range(num_detections):
            box = boxes[0, 0, i]
            mask = masks[i]
            score = box[2]
            if score > self.confidence_threshold:
                class_id = int(box[1])

                left = int(frameW * box[3])
                top = int(frameH * box[4])
                right = int(frameW * box[5])
                bottom = int(frameH * box[6])

                left = max(0, min(left, frameW - 1))
                top = max(0, min(top, frameH - 1))
                right = max(0, min(right, frameW - 1))
                bottom = max(0, min(bottom, frameH - 1))

                class_mask = mask[class_id]

                # Get color of object
                colors.append(self.get_color_of_prediction(self.frame, left, top, right, bottom,
                                                           class_mask))

        for i in range(num_detections):
            box = boxes[0, 0, i]
            mask = masks[i]
            score = box[2]
            if score > self.confidence_threshold:
                class_id = int(box[1])

                left = int(frameW * box[3])
                top = int(frameH * box[4])
                right = int(frameW * box[5])
                bottom = int(frameH * box[6])

                left = max(0, min(left, frameW - 1))
                top = max(0, min(top, frameH - 1))
                right = max(0, min(right, frameW - 1))
                bottom = max(0, min(bottom, frameH - 1))

                class_mask = mask[class_id]

                # Draw bounding box, colorize and show the mask on the image
                self.draw_box(self.frame, class_id, score, left, top, right, bottom, class_mask, colors[i])

    def mask_rcnn(self, file, file_type):
        """
        Run the object detection neural network for all images in
        an input stream.
        """
        output_file = "src/static/" + file[:-4]
        file = "src/image_recon/uploaded/" + file

        if file_type == "image":
            if not os.path.isfile(file):
                print("[OBJECT DETECTOR] Image not found!")
                return False
            cap = cv.VideoCapture(file)
            output_file += "_predicted.jpg"

        elif file_type == "video":
            if not os.path.isfile(file):
                print("[OBJECT DETECTOR] Video not found!")
                return False
            cap = cv.VideoCapture(file)
            output_file += "_predicted.avi"
            vid_writer = cv.VideoWriter(output_file, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 28, (
                round(cap.get(cv.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

        while cv.waitKey(1) < 0:
            start_time = time.time()
            has_frame, self.frame = cap.read()
            if not has_frame:
                print("[OBJECT DETECTOR] Done Processing!")
                break

            blob = cv.dnn.blobFromImage(self.frame, swapRB=True, crop=False)
            self.net.setInput(blob)
            boxes, masks = self.net.forward(['detection_out_final', 'detection_masks'])
            self.post_process(boxes, masks)

            # label = 'yuri (your useless recognizer (of) images)'
            # cv.putText(self.frame, label, (0, 15), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0))

            if file_type == "image":
                cv.imwrite(output_file, self.frame.astype(np.uint8))
                print("[OBJECT DETECTOR] Wrote the file to", output_file)
            else:
                vid_writer.write(self.frame.astype(np.uint8))

            end_time = time.time()
            print("[OBJECT DETECTOR] Time Elapsed:", round(end_time - start_time, 2))

        return True

    def run_prediction(self, file_name, file_type):
        """
        Create an async thread to run the object detector on a file.
        """
        from multiprocessing.pool import ThreadPool

        print("[OBJECT DETECTOR] Starting new object detector thread")
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self.mask_rcnn, (file_name, file_type))
        return async_result.get()
