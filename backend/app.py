from flask import Flask, Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from flask_cors import CORS

from dotenv import load_dotenv

import config

from services import api

load_dotenv()

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}, r"/docs/*": {"origins": "*"}})

api.init_app(app)

config.register_config(app)

if __name__ == '__main__':
    # app.run(debug=True, host=os.environ.get('HOST'), port=os.environ.get('PORT'))
    app.run(debug=True, threaded=True)
