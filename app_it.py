from flask import Flask, render_template, Response, flash, request, redirect, jsonify

import sys
import os
import uuid

import wave
import pyaudio
from pyaudio import PyAudio
import speech_recognition as sr
from pydub import AudioSegment

import scipy
import numpy as np
import asyncio

import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import librosa
import glob

STATE = "OFF"
glob.glob(STATE)
UPLOAD_FOLDER = "files"
FILENAME = "audiofile"
flac_path = FILENAME + ".flac"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.route("/device", methods = ["POST", "GET"])
def device():
    if STATE == "OFF":
        return jsonify({"23" : "0", "0" : "0", "21": "0", "18": "0"})
    else:
        return jsonify({"23" : "1", "0" : "1", "21": "1", "18": "1"})
    
@app.route("/save-record", methods = ["POST"])
def save_record():
    # check if the post request has the file path
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    file_name = FILENAME + ".mp3"
    full_file_name = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    file.save(full_file_name)
    recognize()
    return "<h1>Success</h1>"

def recognize():
    r = sr.Recognizer()
    song = AudioSegment.from_mp3("audiofile" + ".mp3")
    song.export(flac_path, format = "flac")
    with sr.AudioFile("flac_path") as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
        if text == "on":
            STATE = "ON"
        else:
            STATE = "OFF"
    
if __name__ == "__main__":
    # app.run(host="0.0.0.0", debug=True, threaded= True, port= 5000)
    app.run(debug=True, threaded= True, port= 5000)