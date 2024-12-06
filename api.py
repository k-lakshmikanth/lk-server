from flask import Flask, request
import requests as req
import os

app = Flask(__name__)

@app.route("/api/chat", methods=["GET"])
def chat():
    """User prompt formating"""
    return {"chatInput":request.args["body"]} , 200

@app.route("/api/transcribe", methods=["GET"])
def transcribe():
    """Retrieve text from audio."""

    filename = f"/workspaces/lk-server/n8n/data/{request.args['file']}"
    audio_path = request.args["path"]

    with open(filename, "wb") as f:
        f.write(req.get(audio_path).content)

    transcription = req.post("https://api.groq.com/openai/v1/audio/transcriptions",
                    headers={"Authorization": "Bearer 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"},
                    data={"model": "whisper-large-v3-turbo",
                          "response_format": "verbose_json"},
                    files={"file": open(filename, "rb")})
    
    os.remove(filename)

    return {"chatInput":transcription.json()["text"]} , 200

if __name__ == "__main__":
    app.run(debug=True,port=3000)
