from flask import Flask, request
import requests as req
import os

app = Flask(__name__)

@app.route("/")
def index():
  return "<h1>This is an api</h1>"

@app.route("/api/chat", methods=["GET"])
def chat():
    """User prompt formating"""
    if request.args["body"] != "/start":
        return {"chatInput":request.args["body"]} , 200
    else:
        return {"Error":"This is a start command of the conversation with the chat bot."}, 200

@app.route("/api/transcribe", methods=["GET"])
def transcribe():
    """Retrieve text from audio."""
    try:
        api_token = request.args["token"]
        file_id = request.args["file_id"]
        file_path = req.get(f'https://api.telegram.org/bot{api_token}/getFile',
                        data={"file_id":file_id}).json()["result"]["file_path"]

        file_name = f"/workspaces/lk-server/n8n/data/{file_path[:-3]}mp3"
        audio_path = f'https://api.telegram.org/file/bot{api_token}/{file_path}'

        with open(file_name, 'wb') as file:
            file.write(req.get(audio_path).content)

        transcription = req.post("https://api.groq.com/openai/v1/audio/transcriptions",
                        headers={"Authorization": "Bearer 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"},
                        data={"model": "whisper-large-v3-turbo",
                                "response_format": "verbose_json"},
                        files={"file": open(file_name, "rb")})
        
        os.remove(file_name)

        return {"chatInput":transcription.json()["text"]} , 200
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True,port=8000)