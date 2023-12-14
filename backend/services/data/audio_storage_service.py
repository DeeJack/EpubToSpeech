from flask import Blueprint, Flask, current_app
from flask_restx import Api, Resource, fields, abort
import utils.ip_limiter
import os

def save_file(file, filename):
    if os.path.basename(filename) != filename:
        abort(400)
    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
        f.write(file)
        
def get_file(filename):
    if os.path.basename(filename) != filename:
        abort(400)
    try:
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
            return f.read()
    except FileNotFoundError:
        abort(404)
    except:
        abort(500)
        
file_blueprint = Blueprint('audio_storage_blueprint', __name__, url_prefix='/api')
api = Api(
    file_blueprint,
    title='Audio Storage Service',
    version='1.0',
    description='A service for storing audio files',
)

namespace = api.namespace('audio_storage', description='Audio storage operations')

file = api.model(
    'File',
    {
        'file': fields.String(required=True, description='The file to store'),
        'filename': fields.String(required=True, description='The name of the file to store'),
    },
)

@namespace.route('/store-file')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Store a file', params={'file': 'The file to store'})
class StoreFile(Resource):
    @namespace.expect(file)
    @api.marshal_with(file)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        save_file(api.payload['file'], api.payload['filename'])
        return 'OK', 200
    
@namespace.route('/get-file/<string:filename>')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Get a file', params={'filename': 'The file to get'})
class GetFile(Resource):
    @namespace.expect(file)
    @api.marshal_with(file)
    @utils.ip_limiter.limit_ip_access
    def get(self, filename):
        return get_file(filename)