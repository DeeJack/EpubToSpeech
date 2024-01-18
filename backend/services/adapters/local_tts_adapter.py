import io
from time import sleep
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import pyttsx3
import tempfile
import os
import utils.ip_limiter

localtts_namespace = Namespace("local", description="Local TTS operations")
INITIALIZED = False
engine = None


def initialize_tts():
    global engine
    global INITIALIZED
    print('Initializing')
    engine = pyttsx3.init()
    # INITIALIZED = True


def local_tts(text):
    global engine
    global INITIALIZED
    if not INITIALIZED:
        initialize_tts()
    # engine = pyttsx3.init()
    buffer = get_audio_buffer(text)
    print('sending')
    return send_file(
        io.BytesIO(buffer),
        mimetype="audio/wav",
        as_attachment=True,
        download_name="local_tts_output.wav",
    )


def get_audio_buffer(text):
    global engine
    global INITIALIZED
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file_path = temp_file.name
    temp_file.close()

    # Save the audio to the temporary file
    os.remove(temp_file_path)
    print('Generating', text, temp_file_path )
    engine.save_to_file(text, temp_file_path)
    print('Waiting')
    engine.runAndWait()
    print('Waiting not working shit')

    times = 0
    MAX_TRIES = 10
    while times < MAX_TRIES and not os.path.exists(temp_file_path):
        engine.save_to_file(text, temp_file_path)
        engine.runAndWait()
        times += 1
        sleep(0.5)
    print('Done in ', times)

    if times == MAX_TRIES:
        return abort(500, message="Error creating the audio file!")

    # Read the bytes from the file
    with open(temp_file_path, "rb") as f:
        audio_buffer = f.read()

    # Delete the temporary file
    os.remove(temp_file_path)
    engine.stop()
    engine = None
    INITIALIZED = False

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
@localtts_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Convert text to speech",
    params={"text": "The text to be converted to speech"},
)
class TTSService(Resource):
    @localtts_namespace.expect(tts_model)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        """Convert text to speech"""
        data = request.json
        text = data["text"]
        
        print('Starting local')

        # Checks result.
        return local_tts(text)
