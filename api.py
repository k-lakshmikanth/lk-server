
from flask import Flask, request
import requests as req
import os

app = Flask(__name__)

@app.route("/api/transcribe", methods=["GET"])
def transcribe():
    """Retrieve text from audio."""

    filename = request.args["path"]
    
    transcription = req.post("https://api.groq.com/openai/v1/audio/transcriptions",
                    headers={"Authorization": "Bearer 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"},
                    data={"model": "whisper-large-v3-turbo",
                          "response_format": "verbose_json"},
                    files={"file": open(filename, "rb")})
    
    os.remove(filename)

    return transcription.json() , 200

if __name__ == "__main__":
    app.run(debug=True,port=3000)
