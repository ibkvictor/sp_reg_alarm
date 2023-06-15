from flask import Flask, render_template, Response, flash, request, redirect, jsonify
    
import os
import uuid
from flask import Flask, flash, request, redirect
from pyaudio import PyAudio
import speech_recognition as sr
from pydub import AudioSegment
import numpy as np
# import asyncio

import soundfile as sf
# import sounddevice as sd
from scipy.io.wavfile import write
import ffmpeg

UPLOAD_FOLDER = 'files'
STATE = "OFF"
FILENAME = "audiofile"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/save-record', methods=['POST'])
def save_record():
    global STATE
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = "audiofile" + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)
    stream = ffmpeg.input(full_file_name)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "audiofile.wav"))
    stream = ffmpeg.output(stream, os.path.join(app.config['UPLOAD_FOLDER'], "audiofile.wav"))
    r = sr.Recognizer()
    ffmpeg.run(stream)
    text = None
    with sr.AudioFile(os.path.join(app.config['UPLOAD_FOLDER'], "audiofile.wav")) as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
    if text == "on":
        STATE = "ON"
    else:
        STATE = "OFF"
    print(STATE)
    
    # song = AudioSegment.from_mp3(os.path.join(app.config['UPLOAD_FOLDER'], "audiofile.wav"))
    # recognize()
    return '<h1>Success</h1>'

def recognize():
    global STATE
    r = sr.Recognizer()
    song = AudioSegment.from_mp3(os.path.join(app.config['UPLOAD_FOLDER'], "audiofile" + ".mp3"))
    flac_path = os.path.join(app.config['UPLOAD_FOLDER'], "audiofile" + ".flac")
    song.export(flac_path, format = "wav")
    with sr.AudioFile(flac_path) as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
        if text == "on":
            STATE = "ON"
        else:
            STATE = "OFF"
            

@app.route("/device", methods = ["POST", "GET"])
def device():
    global STATE
    if STATE == "OFF":
        return jsonify({"23" : "0", "1" : "0", "21": "0", "18": "0"})
    else:
        return jsonify({"23" : "1", "1" : "1", "21": "1", "18": "1"})

if __name__ == "__main__":
    # app.run(host="0.0.0.0", debug=True, threaded= True, port= 5000)
    app.run(debug=True, threaded= True, port= 5000)