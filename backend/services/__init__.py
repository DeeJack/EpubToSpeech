from flask_restx import Api

from .data.log_service import log_namespace
from .data.storage_service import storage_namespace
from .adapters.sqlite_adapter import sqlite_namespace
from .adapters.epub_adapter import epub_namespace
from .adapters.gpt_adapter import openai_namespace
from .adapters.azure_adapter import azure_namespace
from .adapters.local_tts_adapter import localtts_namespace
from .adapters.elevenlabs_adapter import elevenlabs_namespace
from .logic.tts_logic import tts_namespace as tts_logic_namespace
from .logic.gpt_logic import gptlogic_namespace
from .processes.upload import upload_namespace
from .processes.tts import tts_namespace as tts_process_namespace

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
api.add_namespace(azure_namespace, path='/internal/azure')
api.add_namespace(localtts_namespace, path='/internal/local')
api.add_namespace(elevenlabs_namespace, path='/internal/elevenlabs')
api.add_namespace(tts_logic_namespace, path='/internal/tts')
api.add_namespace(gptlogic_namespace, path='/internal/gpt')

# Public API
api.add_namespace(upload_namespace, path='/api/upload')
api.add_namespace(tts_process_namespace, path='/api/tts')