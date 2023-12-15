from flask_restx import Api

from .data.log_service import log_namespace
from .data.audio_storage_service import audio_namespace

api = Api(
    title='Audio Storage API',
    version='1.0',
    description='A simple audio storage API',
    doc='/docs',
)

api.add_namespace(log_namespace, path='/internal/log')
api.add_namespace(audio_namespace, path='/internal/audio_storage')