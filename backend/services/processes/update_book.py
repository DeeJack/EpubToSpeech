import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests 
import tempfile
from ebooklib import epub
import ebooklib
import uuid

"""
    The public API endpoint to update info about the book in the database
    Steps required:
        1. The user sends the book ID with the new info (title, author, description)
        2. Update the book in the database
"""

info_namespace = Namespace("info", description="Update book's info API endpoint")

info_model = info_namespace.model(
    "Info",
    {
        "book_id": fields.String(
            required=True, description="The book ID"
        ),
        "title": fields.String(required=True, description="The new title"),
        "author": fields.String(required=True, description="The new author"),
        "description": fields.String(required=True, description="The new description"),
    },
)

@info_namespace.route("/")
@info_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Update book\'s info API endpoint', params={'book_id': 'The book ID', 'title': 'The new title', 'author': 'The new author', 'description': 'The new description'})
class Info(Resource):
    @info_namespace.expect(info_model)
    def put(self):
        """
            Update book's info API endpoint
        """
        book_id = request.json["book_id"]
        title = request.json["title"]
        author = request.json["author"]
        description = request.json["description"]
        
        if len(title) == 0 or len(author) == 0 or len(description) == 0:
            return abort(400, "Invalid Argument")
        
        if len(title) > 100 or len(author) > 100 or len(description) > 1000:
            return abort(400, "Invalid Argument")
        
        # Update the book in the database
        url = current_app.config["API_URL"]
        response = requests.post(f"{url}/database/update-book/{book_id}", json={'title': title, 'author': author, 'description': description})
        if response.status_code != 200:
            return abort(response.status_code, response.json()['message'])
        
        return {}, 200