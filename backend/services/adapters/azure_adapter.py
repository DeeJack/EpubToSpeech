import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import azure.cognitiveservices.speech as speechsdk
import os
import tempfile
import utils.ip_limiter
import requests

azure_namespace = Namespace("azure", description="Azure's TTS operations")

tts_model = azure_namespace.model(
    "TTS",
    {
        "text": fields.String(
            required=True, description="The text to be converted to speech"
        ),
    },
)


def generate_tts(text):
    
    response = requests.post(f"{current_app.config['API_URL']}/log/external_api", json={
        'message': f'[AZURE GPT] Prompt: {text}'
    })
    
    print(current_app.config)
    print(current_app.config["AZURE_TTS_KEY"])
    print(current_app.config["AZURE_TTS_REGION"])
    print(current_app.config["AZURE_TTS_VOICE"])
    # https://learn.microsoft.com/it-it/azure/ai-services/speech-service/how-to-speech-synthesis?tabs=browserjs%2Cterminal&pivots=programming-language-python
    speech_config = speechsdk.SpeechConfig(
        subscription=current_app.config["AZURE_TTS_KEY"],
        region=current_app.config["AZURE_TTS_REGION"],
        
    )
    # audio_config = speechsdk.audio.AudioOutputConfig(filename="azure_tts_output.wav")
    # "en-US-JennyNeural"
    # Voices: https://learn.microsoft.com/it-it/azure/ai-services/speech-service/language-support?tabs=tts#prebuilt-neural-voices
    speech_config.speech_synthesis_voice_name = current_app.config["AZURE_TTS_VOICE"]
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    # speech_config=speech_config, audio_config=stream_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    if (
        speech_synthesis_result.reason
        == speechsdk.ResultReason.SynthesizingAudioCompleted
    ):
        data = get_audio_buffer(speech_synthesis_result)
        return send_file(
            io.BytesIO(data),
            mimetype="audio/wav",
            as_attachment=True,
            download_name="azure_tts_output.wav",
        )
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        abort(500, message=cancellation_details.reason)
        # return {'status': 'Speech synthesis canceled: {}'.format(cancellation_details.reason)}, 500
    else:
        abort(500, message="Speech synthesis failed.")
        # return {'status': 'Speech synthesis failed.'}, 500
    abort(500, message="Speech synthesis failed.")


def get_audio_buffer(speech_synthesis_result):
    stream = speechsdk.AudioDataStream(speech_synthesis_result)
    
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file_path = temp_file.name
    temp_file.close()
    
    # Save the audio to the temporary file
    stream.save_to_wav_file(temp_file_path)
    
    # Read the bytes from the file
    with open(temp_file_path, 'rb') as f:
        audio_buffer = f.read()
    
    # Delete the temporary file
    os.remove(temp_file_path)
    
    return audio_buffer


@azure_namespace.route("/tts")
class TTSService(Resource):
    @azure_namespace.expect(tts_model)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        """Convert text to speech"""
        data = request.json
        text = data["text"]

        # Checks result.
        return generate_tts(text)
