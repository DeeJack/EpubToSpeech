import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests
import tempfile
from ebooklib import epub
import ebooklib
import uuid

"""
    The public API endpoint to request a TTS.
    This process is done in 2 steps:
        1. The user sends the book ID with the chapter to be processed
        1. Get the filepath of the book from the database
        2. Read the book with the epub adapter
        3. Send the chapters to the TTS service based on the service chosen
        4. Save the audio file in the storage service
        5. Send the file to the user
"""

tts_namespace = Namespace("tts", description="TTS API endpoint")

tts_model = tts_namespace.model(
    "TTS",
    {
        "book_id": fields.Integer(required=True, description="The book ID"),
        "chapters": fields.Integer(
            required=True, description="The chapter to be processed"
        ),
        "service": fields.String(
            required=True,
            description="The TTS service to be used",
            enum=["azure", "local", "elevenlabs", "openai"],
        ),
    },
)


@tts_namespace.route("/")
@tts_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="TTS API endpoint",
    params={
        "book_id": "The book ID",
        "chapter": "The chapter to be processed",
        "service": "The TTS service to be used",
    },
)
class TTS(Resource):
    @tts_namespace.expect(tts_model)
    def post(self):
        """
        TTS API endpoint
        """
        book_id = request.json["book_id"]
        chapter = request.json["chapter"]
        service = request.json["service"]

        try:
            book_id = int(book_id)
            chapter = int(chapter)
        except:
            return abort(400, message="Invalid parameters!")

        if (
            len(service) == 0
            or len(service) > 100
            or book_id < 0
            or chapter < 0
            or book_id > 1000000
            or chapter > 1000000
        ):
            return abort(400, message="Invalid parameters!")

        # Get the filepath of the book from the database
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/get-book/{book_id}")
        if response.status_code != 200:
            return abort(response.status_code)
        filepath = response.json()["filepath"]

        # Read the book with the epub adapter
        response = requests.get(f"{url}/epub/chapters/{filepath}/{chapter}")
        if response.status_code != 200:
            return abort(response.status_code)
        chapter_content = response.json()["text"]

        # Send the chapter to the TTS service based on the service chosen
        response = requests.post(
            f"{url}/tts/", json={"service": service, "text": chapter_content}
        )

        if response.status_code != 200:
            return abort(response.status_code)

        # Save the audio file in the storage service
        unique_filename = uuid.uuid4().hex
        audio_bytes = response.content
        response = requests.post(
            f"{url}/storage/store-file",
            files={"file": audio_bytes},
            data={"filename": f"{unique_filename}.wav"},
        )
        if response.status_code != 200:
            return abort(response.status_code, response)

        # Add chapter to database
        response = requests.post(
            f"{url}/database/add-chapter",
            json={
                "book_id": book_id,
                "number": chapter,
                "filepath": f"{unique_filename}.wav",
            },
        )

        # Send the file to the user
        return send_file(
            io.BytesIO(audio_bytes),
            mimetype="audio/wav",
            as_attachment=True,
            download_name=f"chapter_{chapter}.wav",
        )
