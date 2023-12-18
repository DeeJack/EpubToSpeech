import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests 

"""
    This is the logic for the TTS service.
    When it's called, it will generate a TTS audio based on the service choosen, and send it to the user.
"""

tts_namespace = Namespace("tts", description="TTS operations")

tts_model = tts_namespace.model(
    "TTS",
    {
        "text": fields.String(
            required=True, description="The text to be converted to speech"
        ),
        "service": fields.String(
            required=True, description="The service to be used", enum=['azure', 'openai', 'elevenlabs', 'local']
        )
    },
)

def generate_tts(url, output_name, text):
    response = requests.post(url, json={'text': text})
    
    if response.status_code != 200:
        abort(response.status_code, response.json()['message'])
    
    file = io.BytesIO(response.content)
    return send_file(
        file,
        mimetype="audio/wav",
        as_attachment=True,
        download_name=output_name,
    )

def generate_azure_tts(text):
    return generate_tts(f"{current_app.config['API_URL']}/azure/tts", "azure_tts_output.wav", text)

def generate_elevenlabs_tts(text):
    return generate_tts(f"{current_app.config['API_URL']}/elevenlabs/tts", "elevenlabs_tts_output.wav", text)

def generate_local_tts(text):
    return generate_tts(f"{current_app.config['API_URL']}/local/tts", "local_tts_output.wav", text)

def generate_openai_tts(text):
    return generate_tts(f"{current_app.config['API_URL']}/openai/tts", "openai_tts_output.wav", text)

@tts_namespace.route("/")
class TTS(Resource):
    @tts_namespace.expect(tts_model)
    def post(self):
        """
        Generate a TTS audio based on the service choosen, and send it to the user.
        """
        data = request.json
        text = data["text"]
        service = data["service"]
        if service == 'azure':
            return generate_azure_tts(text)
        elif service == 'openai':
            return generate_openai_tts(text)
        elif service == 'elevenlabs':
            return generate_elevenlabs_tts(text)
        elif service == 'local':
            return generate_local_tts(text)
        else:
            abort(400, "Invalid service")