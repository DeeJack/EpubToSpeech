import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests
import tempfile
from ebooklib import epub
import ebooklib
import uuid
from itertools import groupby

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
@search_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Search API endpoint",
    params={"keywords": "The text to be searched"},
)
class Search(Resource):
    def get(self):
        """
        Search API endpoint
        """
        args = keywords_parser.parse_args()
        if "keywords" not in args:
            return "No keywords provided", 400
        keywords = args["keywords"]

        if len(keywords) < 3:
            return "Keywords must be at least 3 characters long", 400

        if len(keywords) > 100:
            return "Keywords must be at most 100 characters long", 400

        # Send the search query to the database service
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/search-book?keywords={keywords}")
        if response.status_code != 200:
            return abort(response.status_code)
        books = response.json()

        chap_per_books = []

        if len(books) == 0:
            return [], 200

        chap_per_books = []

        for book_id, group in groupby(books, key=lambda x: x["id"]):
            group_list = list(group)
            current_book = {
                "id": group_list[0]["id"],
                "title": group_list[0]["title"],
                "author": group_list[0]["author"],
                "description": group_list[0]["description"],
                "chapters": [book["chapter_number"] for book in group_list],
            }
            chap_per_books.append(current_book)

        return chap_per_books, 200


@search_namespace.route("/download/<int:book_id>/<int:chapter>")
@search_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Download API endpoint",
    params={"book_id": "The book id", "chapter": "The chapter number"},
)
class Download(Resource):
    def get(self, book_id, chapter):
        """
        Download API endpoint
        """
        # Send the search query to the database service
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/database/get-chapter/{book_id}/{chapter}")
        if response.status_code != 200:
            return abort(response.status_code)
        chapter_path = response.json()["filepath"]

        response = requests.get(f"{url}/storage/get-file/{chapter_path}")
        if response.status_code != 200:
            return abort(response.status_code)

        # Create a response
        return send_file(
            io.BytesIO(response.content),
            mimetype="audio/wav",
            as_attachment=True,
            download_name=f"chapter_{chapter}.wav",
        )
