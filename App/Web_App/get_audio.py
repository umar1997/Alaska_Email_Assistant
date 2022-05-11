import os 
import uuid
import sys

from flask import Flask, flash, request, url_for, render_template, redirect, session, jsonify
from werkzeug.utils import secure_filename
import moviepy.editor as moviepy

# from App.Utils.speechToText import SpeechToText
# dir_path = os.path.dirname(os.path.realpath("./Utils/"))
dir_path_models = os.path.dirname(os.path.realpath("./../../Models/"))
# sys.path.append(dir_path)
sys.path.append(dir_path_models)

from Utils.speechToText import SpeechToText
from Models.models import Model
# from Data_Processing.functions impor

UPLOAD_FOLDER = "audio"
ALLOWED_EXTENSIONS = {"wav", "webm", "mp3"}
 

app = Flask(__name__)
# set a random secret key 
app.secret_key = b'^\x95\x9c\xf5p\x06\x05|b\xcb\xac\x8fO\xf2\x84\x91'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# helper function 
def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
@app.route("/home/", methods=["GET"])
def home():
    return render_template("base.html")

@app.route("/send_email", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        print("request method running")
        # check if the post request has the file part 
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if the user does not select a file, the browser submit on 
        # empty file without a filename 
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = "Audio" + ".webm"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            clip = moviepy.AudioFileClip(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            filename = filename.replace("webm", "wav") 
            # change filename variable 
            session["filename"] = filename
            clip.write_audiofile(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("File Uploaded")
            return redirect(request.url)
            # instead of rendering the page, return a jsonified out 

    return render_template("send_email.html")

@app.route("/_email_text")
def email_text():
    # send audio file to speech_to_text 
    print('#'*20)
    # file_path = "audio/Audio.wav"
    # voice = SpeechToText(file_path)
    # text = voice.convertToText()
    # print('#'*20)
    # print(text)
    # model = Model()
    # res = model.run(text)
    # print(res)

    # email = "mahaagro48@gmail.com"
    # subject = "leave for two days"
    # body = "bla bla"
    res = {
            "function": "EMAIL",
            "EMAILS": {"What are the email addresses?": "mahaagro",
            "What is the email subject?": "bla bla", 
            "What is the email content?": "bla bla" }
        }
    return jsonify(res)