import whisper
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
model = whisper.load_model("medium")



@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "GET":
       result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/transcribe", methods=( ["POST"]))
def transcribe():
    if request.method == "POST":
        upload_folder = 'audio'
        
        
        audio = request.files["audio"]
        audio.save(os.path.join(upload_folder, audio.filename))

        file_path = os.path.join(upload_folder, audio.filename)
        audio_to_text=whisper.load_audio(file_path)
        transcript = model.transcribe(audio_to_text)
        return redirect(url_for("index", result=transcript['text']))

    result = request.args.get("result")
    return render_template("index.html", result=result)

