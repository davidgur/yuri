"""
object_detector.py

Starts the Flask server. Interface between the front-end and back-end.

Author: David Gurevich
Date Started: December 9th, 2018

------------------------------------
YURI (Your Useless Recognizer of Images)
Copyright (C) 2018 David Gurevich, Kenan Liu
"""

import cv2 as cv
import numpy as np
import os.path
import threading

# noinspection PyUnresolvedReferences
from image_recon.color_detector import determine_color


class ObjectDetector:
    def __init__(self):
        self.file_name = None
        self.file_type = None
        self.frame = None

        self.confidence_threshold = 0.5
        self.nms_threshold = 0.4
        self.input_width = 416
        self.input_height = 416

        self.model_configuration = "src/image_recon/models/yolov3.cfg"
        self.model_weights = "src/image_recon/models/yolov3.weights"

        self.classes_file = "src/image_recon/models/coco.names"
        self.classes = None

        self.net = cv.dnn.readNetFromDarknet(self.model_configuration, self.model_weights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        with open(self.classes_file, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

    def get_output_names(self):
        layers_names = self.net.getLayerNames()
        return [layers_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def draw_predictions(self, class_id, conf, left, top, right, bottom, color):
        cv.rectangle(self.frame, (left, top), (right, bottom), color, 3)
        label = f"{round(conf, 3)}"
        if self.classes:
            assert(class_id < len(self.classes))
            label = f"{self.classes[class_id]}: {label}"

        label_size, base_line = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, label_size[1])
        cv.rectangle(self.frame, (left, top - round(1.5 * label_size[1])), (left + round(1.5 * label_size[0]),
                                                                       top + base_line),
                     (255, 255, 255), cv.FILLED)
        cv.putText(self.frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

    def post_process(self, frame, outs):
        colours = []
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.confidence_threshold:
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    width = int(detection[2] * frame_width)
                    height = int(detection[3] * frame_height)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            colors = determine_color(self.frame, box)


            self.draw_predictions(class_ids[i], confidences[i], left, top, left + width, top + height, (255, 255, 255))

        print(colours)

    def prediction_engine(self, file_name, file_type, success_indicator):
        self.file_name = "src/image_recon/uploaded/" + file_name
        self.file_type = file_type

        print(f"[OBJECT DETECTOR] File Name: {self.file_name}")
        output_file = None
        cap = None
        vid_writer = None

        if self.file_type == "image":
            if not os.path.isfile(self.file_name):
                print("[OBJECT DETECTOR] Image could not be found")
                success_indicator.append(False)
                return
            cap = cv.VideoCapture(self.file_name)
            output_file = "src/static/" + file_name[:-4] + "_predicted.jpg"

        elif self.file_type == "video":
            if not os.path.isfile(self.file_name):
                print("[OBJECT DETECTOR] Video could not be found")
                success_indicator.append(False)
                return
            cap = cv.VideoCapture(self.file_name)
            output_file = "src/static/" + file_name[:-4] + "_predicted.avi"
            vid_writer = cv.VideoWriter("src/static/"+output_file, cv.VideoWriter_fourcc('M', 'J', 'P',
                                                                                                    'G'), 30, (
                            round(cap.get(cv.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

        while cv.waitKey(1) < 0:
            has_frame, self.frame = cap.read()
            if not has_frame:
                print(f"[OBJECT DETECTOR] Done processing {self.file_name}")
                print(f"[OBJECT DETECTOR] Output file is stored at {output_file}")
                cap.release()

            try:
                blob = cv.dnn.blobFromImage(self.frame, 1 / 255, (self.input_width, self.input_height),
                                            [0, 0, 0], 1, crop=False)
            except cv.error:
                success_indicator.append(True)
                break
            self.net.setInput(blob)
            outs = self.net.forward(self.get_output_names())
            self.post_process(self.frame, outs)

            if self.file_type == "image":
                cv.imwrite(output_file, self.frame.astype(np.uint8))
            else:
                vid_writer.write(self.frame.astype(np.uint8))

        success_indicator.append(True)
        return

    def run_prediction(self, file_name, file_type):
        print("[OBJECT DETECTOR] Starting new object detector thread")
        success_indicator = [False]
        processing_thread = threading.Thread(target=self.prediction_engine,
                                             args=(file_name, file_type, success_indicator))
        processing_thread.start()
        processing_thread.join()
        return success_indicator[-1]
