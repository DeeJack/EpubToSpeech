from httpx import request
import utils.ip_limiter
from flask import Blueprint, Flask, current_app
from flask_restx import Api, Resource, abort, fields, Namespace
import os
import sqlite3
import config

"""
    This is the adapter for the SQLite database.
    It accepts the following endpoints:
        - /add-book: Add a book to the database
        - /get-book: Get a book from the database
        - /get-books: Get all books from the database
        - /delete-book: Delete a book's filepath from the database
        - /search-book: Search for a book in the database
        - /add-chapter: Add a chapter (and the audio file path!) to the database
        - /get-chapters: Get all chapters from the database
"""

sqlite_namespace = Namespace("database", description="Database operations")


def create_connection():
    return sqlite3.connect(
        os.path.join(
            config.ROOT_FOLDER,
            config.DATABASE_FOLDER,
            config.DATABASE_FILE,
        )
    )


SCHEMA_FILE_NAME = "db_schema.sqlite"
with open(os.path.join(config.ROOT_FOLDER, "db_schema.sqlite")) as f:
    connection = create_connection()
    connection.executescript(f.read())


def write(query, *values):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    conn.close()
    return cur.lastrowid


def read(query, *values):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
    except Exception as e:
        print(e)
        abort(400)
    rows = cursor.fetchall()
    connection.close()
    return rows


book = sqlite_namespace.model(
    "Book",
    {
        "title": fields.String(required=True, description="The book title"),
        "author": fields.String(required=True, description="The author of the book"),
        "description": fields.String(
            required=True, description="The description of the book"
        ),
        "filepath": fields.String(
            required=True, description="The path for the .epub file"
        ),
    },
)

book_id = sqlite_namespace.model(
    "Book", {"id": fields.String(required=True, description="The book ID")}
)

keywords_parser = sqlite_namespace.parser()
keywords_parser.add_argument(
    "keywords", type=str, required=True, help="The keywords to search for"
)


@sqlite_namespace.route("/add-book")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Add a book to the database",
    params={
        "title": "The book title",
        "author": "The author of the book",
        "description": "The description of the book",
        "filepath": "The path for the .epub file",
    },
)
class AddBook(Resource):
    @sqlite_namespace.expect(book)
    @sqlite_namespace.marshal_with(book_id)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        id = write(
            f"INSERT INTO books (title, author, description, filepath) VALUES (?, ?, ?, ?);",
            sqlite_namespace.payload["title"],
            sqlite_namespace.payload["author"],
            sqlite_namespace.payload["description"],
            sqlite_namespace.payload["filepath"],
        )
        return {"id": id}, 201


@sqlite_namespace.route("/get-book/<string:id>")
@sqlite_namespace.doc(
    responses={
        200: "OK",
        400: "Invalid Argument",
        404: "Book not found",
        500: "Mapping Key Error",
    },
    description="Get a book from the database",
    params={"id": "The book ID"},
)
class GetBook(Resource):
    @sqlite_namespace.expect(book_id)
    @sqlite_namespace.marshal_with(book, as_list=False, skip_none=True)
    @utils.ip_limiter.limit_ip_access
    def get(self, id):
        rows = read("SELECT * FROM books WHERE ID = ?;", id)
        if len(rows) == 0:
            return {"error": "Not found"}, 404
        if len(rows) > 1:
            print("SQL INJECTION???")
            # request('POST', '/internal/log/error', json={
            # 'message': f'SQL Injection!!'}, headers={})
            return {"error": "Internal Error"}, 500
        result = rows[0]
        book = {
            "id": result[0],
            "title": result[1],
            "author": result[2],
            "description": result[3],
            "filepath": result[4],
        }
        return book, 200


# For the project it's fine for it to be one user, so I can get the last book uploaded
@sqlite_namespace.route("/get-last-book")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Get the last book from the database",
)
class LastBook(Resource):
    @utils.ip_limiter.limit_ip_access
    def get(self):
        rows = read(f"SELECT * FROM books ORDER BY ID DESC LIMIT 1;")
        if len(rows) == 0:
            return "No book found", 404
        if len(rows) > 1:
            return "Internal error", 500
        return rows[0], 200


@sqlite_namespace.route("/get-books")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Get all books from the database",
)
class GetBooks(Resource):
    @utils.ip_limiter.limit_ip_access
    def get(self):
        rows = read(f"SELECT * FROM books;")
        if len(rows) == 0:
            return "No books found", 404
        return rows, 200


@sqlite_namespace.route("/delete-book")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Delete a book's filepath from the database",
)
class DeleteBook(Resource):
    @sqlite_namespace.expect(book_id)
    @sqlite_namespace.marshal_with(book_id)
    @utils.ip_limiter.limit_ip_access
    def delete(self):
        write(
            f"UPDATE books SET filepath = NULL WHERE ID = ?;",
            sqlite_namespace.payload["id"],
        )
        return "OK", 200


@sqlite_namespace.route("/search-book")
@sqlite_namespace.doc(
    responses={
        200: "OK",
        400: "Invalid Argument",
        404: "No book found",
        500: "Mapping Key Error",
    },
    description="Search for a book in the database",
    params={"keywords": "The keywords to search for"},
)
class SearchBook(Resource):
    @sqlite_namespace.expect(keywords_parser)
    @sqlite_namespace.marshal_with(book, as_list=True, skip_none=True)
    @utils.ip_limiter.limit_ip_access
    def get(self):
        args = keywords_parser.parse_args()
        if "keywords" not in args:
            return "No keywords provided", 400
        keywords = args["keywords"]
        title_search = "%" + keywords + "%"
        description_search = "%" + keywords + "%"
        rows = read(
            "SELECT * FROM books WHERE title LIKE ? OR description LIKE ?;",
            title_search,
            description_search,
        )
        if len(rows) == 0:
            return [], 404
        rows = [
            {
                "id": result[0],
                "title": result[1],
                "author": result[2],
                "description": result[3],
                "filepath": result[4],
            }
            for result in rows
        ]
        return rows, 200


chapter = sqlite_namespace.model(
    "Chapter",
    {
        "book_id": fields.Integer(required=True, description="The book ID"),
        "number": fields.Integer(required=True, description="The chapter number"),
        "filepath": fields.String(
            required=True, description="The path for the .mp3 file"
        ),
    },
)

chapter_parser = sqlite_namespace.parser()
chapter_parser.add_argument(
    "book_id",
    type=int,
    required=True,
    help="The book ID",
)
chapter_parser.add_argument(
    "number",
    type=int,
    required=True,
    help="The chapter number",
)


@sqlite_namespace.route("/add-chapter")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Add a chapter to the database",
    params={
        "book_id": "The book ID",
        "number": "The chapter number",
        "filepath": "The path for the .mp3 file",
    },
)
class AddChapter(Resource):
    @sqlite_namespace.expect(chapter)
    @sqlite_namespace.marshal_with(chapter)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        book_id = sqlite_namespace.payload["book_id"]
        chapter_number = sqlite_namespace.payload["number"]
        filepath = sqlite_namespace.payload["filepath"]
        write(
            f"INSERT INTO chapters (book_id, number, filepath) VALUES (?, ?, ?);",
            book_id,
            chapter_number,
            filepath,
        )
        return "OK", 201


@sqlite_namespace.route("/get-chapters/<string:book_id>")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Get all chapters from the database",
    params={"book_id": "The book ID"},
)
class GetChapters(Resource):
    @sqlite_namespace.expect(book_id)
    @sqlite_namespace.marshal_with(book_id, as_list=True, skip_none=True)
    @utils.ip_limiter.limit_ip_access
    def get(self, book_id):
        rows = read(
            f"SELECT * FROM chapters WHERE book_id = ?;",
            book_id
        )
        if len(rows) == 0:
            return [], 404
        rows = [
            {
                "book_id": result[1],
                "number": result[2],
                "filepath": result[3],
            }
            for result in rows
        ]
        return rows, 200


@sqlite_namespace.route("/get-chapter/<string:book_id>/<string:chapter_number>")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Get a chapter from the database",
    params={"book_id": "The book ID", "chapter_number": "The chapter number"},
)
class GetChapter(Resource):
    @sqlite_namespace.marshal_with(chapter, as_list=False, skip_none=True)
    @utils.ip_limiter.limit_ip_access
    def get(self, book_id, chapter_number):
        # args = chapter_parser.parse_args()
        # book_id = args['book_id']
        # chapter_number = args['number']
        rows = read(
            f"SELECT * FROM chapters WHERE book_id = ? AND number = ?;",
            book_id,
            chapter_number,
        )
        if len(rows) == 0:
            return {}, 404
        if len(rows) > 1:
            print("SQL INJ????")
            return {}, 500
        chapter = {
            "book_id": rows[0][0],
            "number": rows[0][1],
            "filepath": rows[0][2],
        }
        return chapter, 200
