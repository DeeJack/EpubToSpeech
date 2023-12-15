from flask import Blueprint, Flask, current_app, request
from flask_restx import Api, Resource, fields, abort, Namespace
import utils.ip_limiter
import os

def save_file(file, filename):
    if os.path.basename(filename) != filename:
        abort(400)
    file.save(os.path.join(current_app.config['ROOT_FOLDER'], current_app.config['UPLOAD_FOLDER'], filename))
    # with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
    #     f.write(file)
        
def get_file(filename):
    print(os.path.basename(filename), filename)
    if os.path.basename(filename) != filename:
        abort(400)
    try:
        with open(os.path.join(current_app.config['ROOT_FOLDER'], current_app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
            return f.read().decode('utf-8')
    except FileNotFoundError as e:
        print(e)
        abort(404)
    except:
        abort(500)
        
# file_blueprint = Blueprint('audio_storage_blueprint', __name__, url_prefix='/internal')
# api = Api(
#     file_blueprint,
#     title='Audio Storage Service',
#     version='1.0',
#     description='A service for storing audio files',
# )

audio_namespace = Namespace('audio_storage', description='Audio storage operations')

file = audio_namespace.model(
    'file',
    {
        'file': fields.String(required=True, description='The file to store'),
        'filename': fields.String(required=True, description='The name of the file to store'),
    },
)

@audio_namespace.route('/store-file')
@audio_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Store a file', params={'file': 'The file to store'})
class StoreFile(Resource):
    @audio_namespace.expect(file)
    @audio_namespace.marshal_with(file)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        if 'file' not in request.files:
            abort(400, 'No file part')
        if 'filename' not in request.form:
            abort(400, 'No filename part')
        
        file = request.files['file']
        filename = request.form['filename']
        
        save_file(file, filename)
        return 'OK', 200
    
@audio_namespace.route('/get-file/<string:filename>')
@audio_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Get a file', params={'filename': 'The file to get'})
class GetFile(Resource):
    @utils.ip_limiter.limit_ip_access
    def get(self, filename):
        return {'content': get_file(filename)}, 200