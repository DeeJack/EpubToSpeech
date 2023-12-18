import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import os
import tempfile
from elevenlabs import generate, play, save, stream
import utils.ip_limiter
import requests

elevenlabs_namespace = Namespace("elevenlabs", description="Elevenlabs TTS operations")

tts_model = elevenlabs_namespace.model(
    "TTS",
    {
        "text": fields.String(
            required=True, description="The text to be converted to speech"
        ),
    },
)

def generate_tts(text):
    
    response = requests.post(f"{current_app.config['API_URL']}/log/external_api", json={
        'message': f'[ELEVENLABS] Prompt: {text}'
    })
    
    audio = generate(
        text=text,
        voice="Charlie",
        model="eleven_multilingual_v2",
        api_key=current_app.config["ELEVENLABS_API_KEY"],
    )

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file_path = temp_file.name
    temp_file.close()
    
    # Save the audio to the temporary file
    save(audio, temp_file_path)
    
    # Read the bytes from the file
    with open(temp_file_path, 'rb') as f:
        audio_buffer = f.read()
    
    # Delete the temporary file
    os.remove(temp_file_path)
    
    return audio_buffer
    
    # return stream(audio)

@elevenlabs_namespace.route("/tts")
class TTS(Resource):
    @elevenlabs_namespace.expect(tts_model)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        data = request.get_json()
        text = data["text"]
        return send_file(io.BytesIO(generate_tts(text)), mimetype="audio/wav", as_attachment=True, download_name="elevenlabs_tts_output.wav") 