import utils.ip_limiter
from datetime import datetime
from flask import Blueprint, Flask
from flask_restx import Api, Resource, fields
import utils.ip_limiter

log_blueprint = Blueprint("log_blueprint", __name__, url_prefix="/api")

api = Api(
    log_blueprint,
    title="Log Service",
    version="1.0",
    description="A service for writing logs",
)

namespace = api.namespace("log", description="Log operations")

def write_file(file, message):
    message = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}'
    
    with open(file, 'a') as f:
        f.write(message + '\n')

def write_error(message):
    write_file('error.log', message)
        
def write_database(query):
    write_file('database.log', query)
        
def write_external_api(message):
    write_file('external_api.log', message)
        
message = api.model(
    "Message",
    {
        "message": fields.String(required=True, description="The message to log"),
    },
)

@namespace.route("/error")
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Log an error', params={'message': 'The error message'})
class Error(Resource):
    @namespace.expect(message)
    @api.marshal_with(message)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write_error(api.payload["message"])
        return "OK", 200
    
@namespace.route("/database")
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Log a database query', params={'query': 'The database query'})
class Database(Resource):
    @namespace.expect(message)
    @api.marshal_with(message)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write_database(api.payload["query"])
        return "OK", 200
    
@namespace.route("/external_api")
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Log an external API call', params={'message': 'The external API call'})
class ExternalAPI(Resource):
    @namespace.expect(message)
    @api.marshal_with(message)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write_external_api(api.payload["message"])
        return "OK", 200