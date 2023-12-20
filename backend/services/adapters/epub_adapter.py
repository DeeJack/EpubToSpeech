from bs4 import BeautifulSoup
import utils.ip_limiter
from flask import Blueprint, Flask, current_app, request
from flask_restx import Api, Resource, abort, fields, Namespace
import tempfile
from ebooklib import epub
import ebooklib
import requests

"""
    This is the adapter to read and parse the epub files
    Endpoints:
        - /epub/chapters/<book_id> - GET
        - /epub/chapter/<book_id>/<chapter_id> - GET
        - /epub/book/<book_id> POST
"""
epub_namespace = Namespace("epub", description="Epub related operations")

"""
    
"""

def get_chapter_list(content):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(content)
        book = epub.read_epub(f.name)
        chapters_raw = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        chapters = []
        for item in chapters_raw:
            chapters.append(item.get_name())
        return chapters


def read_chapter(content, number):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(content)
        book = epub.read_epub(f.name)
        chapters_raw = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        if number < 0 or number >= len(chapters_raw):
            return abort(400, message="Invalid chapter number")
        
        text = chapters_raw[number].get_content().decode("utf-8")
        
        parser = BeautifulSoup(text, 'html.parser')
        text = parser.get_text()

        return text


def read_chapters(content, chapters):
    with tempfile.NamedTemporaryFile(delete=True) as f:
        f.write(content)
        book = ebooklib.epub.read_epub(f.name)
        chapters_raw = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        result = []
        for chapter in chapters:
            if chapter < 0 or chapter >= len(chapters_raw):
                continue
            else:
                result.append(chapters_raw[chapter].get_content())
        return result


@epub_namespace.route("/chapters/<string:filepath>")
@epub_namespace.doc(params={"filepath": "The path to the epub file"})
class EpubChapters(Resource):
    @epub_namespace.doc("get_chapter_list")
    @utils.ip_limiter.limit_ip_access
    def get(self, filepath):
        """
        Get the list of chapters of a book
        """
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/storage/get-file/{filepath}")


        if response.status_code != 200:
            abort(response.status_code)

        return get_chapter_list(response.content), 200


@epub_namespace.route("/chapters/<string:filepath>/<int:chapter_number>")
class EpubChapter(Resource):
    @epub_namespace.doc("read_chapter")
    @utils.ip_limiter.limit_ip_access
    def get(self, filepath, chapter_number):
        """
        Get a chapter of a book
        """
        url = current_app.config["API_URL"]
        response = requests.get(f"{url}/storage/get-file/{filepath}")

        if response.status_code != 200:
            abort(response.status_code)
        chapter = {
            'text': read_chapter(response.content, chapter_number)
        }
        return chapter, 200


@epub_namespace.route("/store-book")
@epub_namespace.doc(params={"filename": "The filename of the book", "file": "The epub file"})
class EpubBook(Resource):
    @epub_namespace.doc("read_chapters")
    @utils.ip_limiter.limit_ip_access
    def post(self):
        """
        Get a chapter of a book
        """
        file = request.files["file"]
        filename = request.form["filename"]
        metadata = {}
        
        print('RECEIVED FILE', file.filename)
        
        # Tries to parse the file to make sure it's an epub, also tries to parse the book_id to make sure it's an int
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as f:
                f.write(file.read())
                book = epub.read_epub(f.name)
                print('OK')
                metadata['title'] = book.get_metadata('DC', 'title')[0][0]
                metadata['author'] = book.get_metadata('DC', 'creator')[0][0]
        except Exception as e:
            print(e)
            print('ERROR WHILE PARSING')
            abort(400)
        file.seek(0)
        print('PARSED')
        
        url = current_app.config["API_URL"]
        print('URL:', f'{url}/storage/store-file')
        print(file.filename)
        files = {'file': file}
        values = {'filename': f'{filename}.epub'}
        response = requests.post(
            f"{url}/storage/store-file",
            files=files,
            data=values
            # headers= {
            #     "Content-Type": "multipart/form-data",
            # }
        )
        
        print('RECEIVED RESPONSE', response.status_code)

        if response.status_code != 200:
            abort(response.status_code)

        return metadata, 200
