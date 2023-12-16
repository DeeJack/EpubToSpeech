from flask_restx import Api

from .data.log_service import log_namespace
from .data.storage_service import storage_namespace
from .adapters.sqlite_adapter import sqlite_namespace
from .adapters.epub_adapter import epub_namespace

api = Api(
    title='Audio Storage API',
    version='1.0',
    description='A simple audio storage API',
    doc='/docs',
)

api.add_namespace(log_namespace, path='/internal/log')
api.add_namespace(storage_namespace, path='/internal/audio_storage')
api.add_namespace(sqlite_namespace, path='/internal/database')
api.add_namespace(epub_namespace, path='/internal/epub')