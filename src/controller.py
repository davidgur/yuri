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

from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from uuid import uuid4

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploaded"
app.config["MAX_CONTENT_PATH"] = 5e6
app.config['SECRET_KEY'] = "yuri_ocr"

ALLOWED_EXTENSIONS = ['jpeg', 'jpg', 'tiff', 'bmp', 'png', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Controllers
@app.route("/")
def main_page():
    session["user_identifier"] = str(uuid4())
    print(session["user_identifier"])
    return render_template("upload.html")


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(secure_filename(f.filename)):
            file_name = "src/uploaded/" + session["user_identifier"]
            f.save(file_name)
            print(f"File ({f.filename} successfully")
            return redirect("/results")
        else:
            return "Invalid file"


@app.route("/results")
def results():
    print("Results:", session["user_identifier"])
    return "Not yet implemented"

# Launch Flask Server
if __name__ == '__main__':
    app.run()
