#!/usr/bin/env python
"""
controller.py

Starts the Flask server. Interface between the front-end and back-end.

Author: David Gurevich
Date Started: December 9th, 2018

------------------------------------
YURI (Your Useless Recognizer of Images)
Copyright (C) 2018 David Gurevich
"""

import os
from uuid import uuid4

import image_recon.mask_rcnn
from flask import Flask, redirect, render_template, request, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploaded"
app.config["MAX_CONTENT_PATH"] = 5e6
app.config['SECRET_KEY'] = "yuri_ocr"

ALLOWED_IMAGE_EXTENSIONS = ['jpeg', 'jpg', 'tiff', 'bmp', 'png', 'gif']
ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'avi']

IMAGE = 'image'
VIDEO = 'video'
INVALID = 'invalid'


def determine_file_type(filename):
    if '.' in filename:
        extension = filename.rsplit('.', 1)[1].lower()
        if extension in ALLOWED_IMAGE_EXTENSIONS:
            return IMAGE
        elif extension in ALLOWED_VIDEO_EXTENSIONS:
            return VIDEO
        else:
            return INVALID


# Controllers
@app.route("/")
def main_page():
    session["user_identifier"] = str(uuid4())
    return render_template("upload.html")

@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        object_detector = image_recon.mask_rcnn.ObjectDetector()

        color_choice = request.form['color-choice']
        object_choice = request.form['object-choice']

        f = request.files['file']
        file_type = determine_file_type(secure_filename(f.filename))
        if file_type == INVALID:
            return "Invalid File"
        elif file_type == IMAGE:
            file_name = "src/image_recon/uploaded/" + session["user_identifier"] + ".jpg"
            f.save(file_name)
            session["file_extension"] = "jpg"
            session["file_type"] = IMAGE
            object_detector.run_prediction(session["user_identifier"] + ".jpg", IMAGE, color_choice, object_choice)
            del object_detector

            return redirect('/results')
        elif file_type == VIDEO:
            file_name = "src/image_recon/uploaded/" + session["user_identifier"] + ".avi"
            f.save(file_name)
            session["file_extension"] = "avi"
            session["file_type"] = VIDEO
            object_detector.run_prediction(session["user_identifier"] + ".avi", VIDEO)
            del object_detector

            return redirect('/results')


@app.route("/results")
def results():
    return render_template("result.html", img_name=(session["user_identifier"] + "_predicted." +
                                                    session["file_extension"]), is_video=session["file_type"] == VIDEO)


# Launch Flask Server
if __name__ == '__main__':
    app.run()
