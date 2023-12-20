import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests 
import tempfile
from ebooklib import epub
import ebooklib
import uuid


"""
    Public API to upload a book.
    This process is done in 4 steps:
        1. Store the book using the data layer servie
        2. Save the book in the database with the sqlite adapter
        3. Get metadata about the book using the epub adapter
        4. Return those info to the user
"""

upload_namespace = Namespace("upload", description="Upload operations")

@upload_namespace.route("/")
@upload_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Upload a book', params={'file': 'The file to be uploaded'})
class Upload(Resource):
    def post(self):
        """
            Upload a book
        """
        print('Uploading')
        file = request.files["file"]

        # Check the size of the file
        if len(file.read()) > current_app.config["FILE_SIZE_MAX"]:
            abort(400, "File too large")
        file.seek(0)
        
        url = current_app.config["API_URL"]
        files = {'file': file}
        
        unique_filename = uuid.uuid4().hex

        response = requests.post(
            f"{url}/epub/store-book",
            files=files,
            data={
                'filename': unique_filename
            }
        )
        if response.status_code != 200:
            return abort(response.status_code, response.json()['message'])
        
        metadata = response.json()
        print('STORED')
        print(metadata)
        
        # Store the book in the database
        response = requests.post(
            f"{url}/database/add-book",
            json={
                'title': metadata['title'],
                'author': metadata['author'],
                'filepath': f'{unique_filename}.epub'
            }
        )
        if response.status_code != 201:
            return abort(response.status_code, response.json()['message'])
        
        id = response.json()['id']
        
        print('STORED IN DB WITH ID', id)
        
        return {
            'id': id,
            'title': metadata['title'],
            'author': metadata['author'],
        }, 200