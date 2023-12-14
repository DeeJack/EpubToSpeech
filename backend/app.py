from flask import Flask, Blueprint, jsonify
# from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from flask_cors import CORS

from flask_restx import Api, Resource

from dotenv import load_dotenv
import os

import config

from services.data.log_service import log_blueprint
from services.data.audio_storage_service import file_blueprint

load_dotenv()

app = Flask(__name__)
api = Api(app, doc='/api/docs')

config.register_config(app)

app.register_blueprint(log_blueprint)
app.register_blueprint(file_blueprint)

@api.route('/api/')
@api.doc(params={'id': 'An ID'}, description='Get a book by its ID')
class Home(Resource):
    def get(self):
        return {'Hello': 'World'}

# Swagger UI route
SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    # app.run(debug=True, host=os.environ.get('HOST'), port=os.environ.get('PORT'))
    app.run(debug=True)
