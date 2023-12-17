import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import torch
from TTS.api import TTS
import tempfile
import os

localtts_namespace = Namespace("local", description="Local TTS operations")
INITIALIZED = False
tts = None

def initialize_tts():
    # Get device
    global tts
    global INITIALIZED
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    INITIALIZED = True

def local_tts(text):
    if not INITIALIZED:
        initialize_tts()
    buffer = get_audio_buffer(tts, text)
    return send_file(
        io.BytesIO(buffer),
        mimetype="audio/wav",
        as_attachment=True,
        download_name="local_tts_output.wav",
    )
    
def get_audio_buffer(tts, text):
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file_path = temp_file.name
    temp_file.close()
    
    # Save the audio to the temporary file
    clone_folder = os.path.join(current_app.config["ROOT_FOLDER"], 'static', "clone.mp3")
    tts.tts_to_file(text=text, speaker_wav=clone_folder, language="en", file_path=temp_file_path)
    
    # Read the bytes from the file
    with open(temp_file_path, 'rb') as f:
        audio_buffer = f.read()
    
    # Delete the temporary file
    os.remove(temp_file_path)
    
    return audio_buffer

tts_model = localtts_namespace.model(
    "TTS",
    {
        "text": fields.String(
            required=True, description="Text to be converted to speech"
        ),
    },
)

@localtts_namespace.route("/tts")
class TTSService(Resource):
    @localtts_namespace.expect(tts_model)
    def post(self):
        """Convert text to speech"""
        data = request.json
        text = data["text"]

        # Checks result.
        return local_tts(text)