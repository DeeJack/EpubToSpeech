from flask_restx import Api

from .data.log_service import log_namespace
from .data.storage_service import storage_namespace
from .adapters.sqlite_adapter import sqlite_namespace
from .adapters.epub_adapter import epub_namespace
from .adapters.gpt_adapter import openai_namespace

api = Api(
    title='Epub To Speech Services',
    version='1.0',
    description='APIs to convert epub files to speech and other AI services',
    doc='/docs',
)

api.add_namespace(log_namespace, path='/internal/log')
api.add_namespace(storage_namespace, path='/internal/storage')
api.add_namespace(sqlite_namespace, path='/internal/database')
api.add_namespace(epub_namespace, path='/internal/epub')
api.add_namespace(openai_namespace, path='/internal/openai')