import whisper
import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
model = whisper.load_model("medium")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "GET":
        result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/transcribe", methods=(["POST"]))
def transcribe():
    if request.method == "POST":
        upload_folder = 'audio'

        audio = request.files["audio"]
        audio.save(os.path.join(upload_folder, audio.filename))

        file_path = os.path.join(upload_folder, audio.filename)
        audio_to_text = whisper.load_audio(file_path)
        transcript = model.transcribe(audio_to_text)
        resume = resume_text(transcript['text'])
        return redirect(url_for("index", result=resume))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def resume_text(text):
    openai.api_key = "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"
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,  # Controla la creatividad del modelo (0.2 a 1.0)
        # Controla la probabilidad de selección de palabras (0.7 a 1.0)
        top_p=1.0,
        messages=[{
            "role": "system",
            "content": "Eres una IA altamente capacitada y capacitada en comprensión y resumen de idiomas. Me gustaría que leyeras el siguiente texto y lo resumieras en un párrafo abstracto conciso. Trate de retener los puntos más importantes, proporcionando un resumen coherente y legible que pueda ayudar a una persona a comprender los puntos principales de la discusión sin necesidad de leer el texto completo. Evite detalles innecesarios o puntos tangenciales."
        },
            {"role": "user",                "content": text}]
    )
    return respuesta['choices'][0]['message']['content'].encode('utf-8').decode('utf-8')
