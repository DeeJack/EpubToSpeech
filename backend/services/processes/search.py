import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests 
import tempfile
from ebooklib import epub
import ebooklib
import uuid

"""
    Public API endpoint to search for books.
    This process is done in 3 steps:
        1. The user sends the search query
        2. The search query is sent to the database service
        3. The database service returns the list of books matching the query
"""

search_namespace = Namespace("search", description="Search API endpoint")

keywords_parser = search_namespace.parser()
keywords_parser.add_argument(
    "keywords", type=str, required=True, help="The keywords to search for"
)


@search_namespace.route("/")
@search_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Search API endpoint', params={'keywords': 'The text to be searched'})
class Search(Resource):
    def get(self):
        """
            Search API endpoint
        """
        print('BEFORE ASD')
        args = keywords_parser.parse_args()
        if "keywords" not in args:
            return "No keywords provided", 400
        print('AFTER ASD')
        keywords = args["keywords"]
        
        if len(keywords) < 3:
            return "Keywords must be at least 3 characters long", 400
        
        if len(keywords) > 100:
            return "Keywords must be at most 100 characters long", 400
        
        print('AAAAAAAA')
        
        # Send the search query to the database service
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/search-book?keywords={keywords}")
        if response.status_code != 200:
            return abort(response.status_code)
        books = response.json()
        
        return books, 200