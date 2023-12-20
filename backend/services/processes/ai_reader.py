import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests
import tempfile
from ebooklib import epub
import ebooklib
import uuid

"""
    Public API endpoint for the functions present in the AI reader.
    The functions are:
        1. Show the text for a chapter
        2. Show the list of chapters to choose from
        3. Use the GPT API to do stuff (Translate, Summarize, Custom Prompt)
"""

reader_namespace = Namespace("reader", description="Reader Public API endpoint")

@reader_namespace.route("/chapter/<string:book_id>/<string:chapter>")
@reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Show the text for a chapter', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number'})
class Reader(Resource):
    @reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Show the text for a chapter', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number'})
    def get(self, book_id, chapter):
        """
            Show the text for a chapter
        """
        
        try:
            int(chapter)
            int(book_id)
        except:
            return abort(400, message="Invalid parameters!")
        
        # Read the filepath of the file from the db
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/get-book/{book_id}")
        if response.status_code != 200:
            return abort(response.status_code)
        book = response.json()
        
        # Process the epub and read the chapter from the epub adapter
        response = requests.get(f"{url}/epub/chapters/{book['filepath']}/{chapter}")
        if response.status_code != 200:
            return abort(response.status_code)
        
        chapter = response.json()
        
        return {'text': chapter['text']}, 200

@reader_namespace.route("/chapters/<string:book_id>")
@reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Show the list of chapters to choose from', params={'book_id': 'The ID of the book'})
class ReaderChapters(Resource):
    @reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Show the list of chapters to choose from', params={'book_id': 'The ID of the book'})
    def get(self, book_id):
        """
            Show the list of chapters to choose from
        """
        
        try:
            int(book_id)
        except:
            return abort(400, message="Invalid parameters!")
        
        # Read the filepath of the file from the db
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/get-book/{book_id}")
        if response.status_code != 200:
            return abort(response.status_code)
        book = response.json()
        
        # Process the epub and read the chapter from the epub adapter
        response = requests.get(f"{url}/epub/chapters/{book['filepath']}")
        if response.status_code != 200:
            return abort(response.status_code)
        
        chapters = response.json()
        
        return chapters, 200

@reader_namespace.route("/translate/<string:book_id>/<string:chapter>")
@reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Translate the chapter', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number'})
class ReaderGPT(Resource):
    @reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Translate the chapter', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number'})
    def post(self, book_id, chapter):
        """
            Translate the chapter
        """
        
        try:
            int(chapter)
            int(book_id)
        except:
            return abort(400, message="Invalid parameters!")
        
        # Read the filepath of the file from the db
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/get-book/{book_id}")
        if response.status_code != 200:
            return abort(response.status_code)
        book = response.json()
        
        # Process the epub and read the chapter from the epub adapter
        response = requests.get(f"{url}/epub/chapters/{book['filepath']}/{chapter}")
        if response.status_code != 200:
            return abort(response.status_code)
        
        chapter = response.json()
        
        # Send the chapter to the GPT API
        response = requests.post(f"{url}/gpt/translate", json={
            'text': chapter['text'],
        })
        if response.status_code != 200:
            return abort(response.status_code)
        
        return response.json(), 200
    
@reader_namespace.route("/summarize/<string:book_id>/<string:chapter>")
@reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Summarize the chapter', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number'})
class ReaderSummarize(Resource):
    @reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Summarize the chapter', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number'})
    def post(self, book_id, chapter):
        """
            Summarize the chapter
        """
        
        try:
            int(chapter)
            int(book_id)
        except:
            return abort(400, message="Invalid parameters!")
        
        # Read the filepath of the file from the db
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/get-book/{book_id}")
        if response.status_code != 200:
            return abort(response.status_code)
        book = response.json()
        
        # Process the epub and read the chapter from the epub adapter
        response = requests.get(f"{url}/epub/chapters/{book['filepath']}/{chapter}")
        if response.status_code != 200:
            return abort(response.status_code)
        
        chapter = response.json()
        
        # Send the chapter to the GPT API
        response = requests.post(f"{url}/gpt/summarize", json={
            'text': chapter['text'],
        })
        if response.status_code != 200:
            return abort(response.status_code)
        
        return response.json(), 200
    
@reader_namespace.route("/generate/<string:book_id>/<string:chapter>")
@reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Generate text from prompt', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number', 'prompt': 'The prompt to be processed'})
class ReaderGenerate(Resource):
    @reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Generate text from prompt', params={'book_id': 'The ID of the book', 'chapter': 'The chapter\'s number', 'prompt': 'The prompt to be processed'})
    def post(self, book_id, chapter):
        """
            Generate text from prompt
        """
        
        try:
            int(chapter)
            int(book_id)
        except:
            return abort(400, message="Invalid parameters!")
        
        prompt = request.json["prompt"]
        
        if len(prompt) > 1000:
            return abort(400, "Prompt too long")
        
        if len(prompt) == 0:
            return abort(400, "Prompt too short")
        
        # Read the filepath of the file from the db
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/get-book/{book_id}")
        if response.status_code != 200:
            return abort(response.status_code)
        book = response.json()
        
        # Process the epub and read the chapter from the epub adapter
        response = requests.get(f"{url}/epub/chapters/{book['filepath']}/{chapter}")
        if response.status_code != 200:
            return abort(response.status_code)
        
        chapter = response.json()
        
        # Send the chapter to the GPT API
        response = requests.post(f"{url}/gpt/generate", json={
            'prompt': prompt,
            'text': chapter['text'],
        })
        if response.status_code != 200:
            return abort(response.status_code)
        
        return response.json(), 200
    
# Generate image
@reader_namespace.route("/image/")
@reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Generate image from prompt', params={'prompt': 'The prompt for the image'})
class ReaderImage(Resource):
    @reader_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Generate image from prompt', params={'prompt': 'The prompt for the image'})
    def post(self):
        """
            Generate image from prompt
        """
        
        prompt = request.json["prompt"]
        
        if len(prompt) > 1000:
            return abort(400, "Prompt too long")
        
        if len(prompt) < 5:
            return abort(400, "Prompt too short")
        
        API_URL = current_app.config["API_URL"]
        # Send the chapter to the GPT API
        response = requests.post(f"{API_URL}/gpt/image", json={
            'text': prompt,
        })
        if response.status_code != 200:
            return abort(response.status_code)
        
        return response.json(), 200