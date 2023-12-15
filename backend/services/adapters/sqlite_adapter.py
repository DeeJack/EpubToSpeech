from httpx import request
import utils.ip_limiter
from flask import Blueprint, Flask, current_app
from flask_restx import Api, Resource, fields, Namespace
import os
import sqlite3

"""
    This is the adapter for the SQLite database.
    It accepts the following endpoints:
        - /add-book: Add a book to the database
        - /get-book: Get a book from the database
        - /get-books: Get all books from the database
        - /delete-book: Delete a book's filepath from the database
        - /add-chapter: Add a chapter (and the audio file path!) to the database
        - /get-chapters: Get all chapters from the database
"""

sqlite_namespace = Namespace("database", description="Database operations")


def create_connection():
    return sqlite3.connect(
        os.path.join(
            current_app.config["ROOT_FOLDER"],
            current_app.config["DATABASE_FOLDER"],
            current_app.config["DATABASE_FILE"],
        )
    )


def write(query, values=()):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    conn.close()


def read(query, values):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, values)
    rows = cur.fetchall()
    conn.close()
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
    "Book", {"id": fields.Integer(required=True, description="The book ID")}
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
    @sqlite_namespace.marshal_with(book)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write(
            f"INSERT INTO books (title, author, description, filepath) VALUES ('{sqlite_namespace.payload['title']}', '{sqlite_namespace.payload['author']}', '{sqlite_namespace.payload['description']}', '{sqlite_namespace.payload['filepath']}');"
        )
        return "OK", 200


@sqlite_namespace.route("/get-book")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Get a book from the database",
    params={"title": "The book title"},
)
class GetBook(Resource):
    @sqlite_namespace.expect(book_id)
    @sqlite_namespace.marshal_with(book_id)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        rows = read(
            f"SELECT * FROM books WHERE ID = ?;", sqlite_namespace.payload['id']
        )
        if len(rows) == 0:
            return "Book not found", 404
        if len(rows) > 1:
            print('SQL INJECTION???')
            # request('POST', '/internal/log/error', json={
                # 'message': f'SQL Injection!!'}, headers={})
            return "Internal error", 500
        return rows[0], 200
    
# For the project it's fine for it to be one user, so I can get the last book uploaded
@sqlite_namespace.route("/get-last-book")
@sqlite_namespace.doc(responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"}, description="Get the last book from the database")
class LastBook(Resource):
    @utils.ip_limiter.limit_ip_access
    def get(self):
        rows = read(f"SELECT * FROM books ORDER BY ID DESC LIMIT 1;", ())
        if len(rows) == 0:
            return "No book found", 404
        if len(rows) > 1:
            return "Internal error", 500
        return rows[0], 200
    
@sqlite_namespace.route("/get-books")
@sqlite_namespace.doc(responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"}, description="Get all books from the database")
class GetBooks(Resource):
    @utils.ip_limiter.limit_ip_access
    def get(self):
        rows = read(f"SELECT * FROM books;", ())
        if len(rows) == 0:
            return "No books found", 404
        return rows, 200
    
@sqlite_namespace.route("/delete-book")
@sqlite_namespace.doc(responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"}, description="Delete a book's filepath from the database")
class DeleteBook(Resource):
    @sqlite_namespace.expect(book_id)
    @sqlite_namespace.marshal_with(book_id)
    @utils.ip_limiter.limit_ip_access
    def delete(self):
        write(f"UPDATE books SET filepath = NULL WHERE ID = ?;", sqlite_namespace.payload['id'])
        return "OK", 200

    
chapter = sqlite_namespace.model(
    "Chapter",
    {
        "book_id": fields.Integer(required=True, description="The book ID"),
        "title": fields.String(required=True, description="The chapter title"),
        "filepath": fields.String(
            required=True, description="The path for the .mp3 file"
        ),
    },
)

@sqlite_namespace.route("/add-chapter")
@sqlite_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Add a chapter to the database",
    params={
        "book_id": "The book ID",
        "title": "The chapter title",
        "filepath": "The path for the .mp3 file",
    },
)
class AddChapter(Resource):
    @sqlite_namespace.expect(chapter)
    @sqlite_namespace.marshal_with(chapter)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write(
            f"INSERT INTO chapters (book_id, title, filepath) VALUES ('{sqlite_namespace.payload['book_id']}', '{sqlite_namespace.payload['title']}', '{sqlite_namespace.payload['filepath']}');"
        )
        return "OK", 200
    
@sqlite_namespace.route("/get-chapters")
@sqlite_namespace.doc(responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"}, description="Get all chapters from the database", params={"book_id": "The book ID"})
class GetChapters(Resource):
    @sqlite_namespace.expect(book_id)
    @sqlite_namespace.marshal_with(book_id)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        rows = read(
            f"SELECT * FROM chapters WHERE book_id = ?;", sqlite_namespace.payload['id']
        )
        if len(rows) == 0:
            return "Book not found", 404
        return rows, 200