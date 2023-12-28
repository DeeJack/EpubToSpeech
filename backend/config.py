import dotenv
dotenv.load_dotenv()
from os import getenv
import os

DATABASE = "books.db"
UPLOAD_FOLDER = os.path.join('static', 'uploads')
FILE_SIZE_MAX = 5 * 1024 * 1024 # 5 MB
LOG_FOLDER = "logs"
ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATABASE_FOLDER = "database"
DATABASE_FILE = "books.db"
HOST = '127.0.0.1'
PORT = 5000
API_URL = f'http://{HOST}:{PORT}/internal'
OPENAI_API_KEY = getenv('OPENAI_API_KEY')
AZURE_TTS_KEY = getenv('AZURE_TTS_KEY')
AZURE_TTS_REGION = getenv('AZURE_TTS_REGION')
AZURE_TTS_VOICE = getenv('AZURE_TTS_VOICE')
ELEVENLABS_API_KEY = getenv('ELEVENLABS_API_KEY')

def register_config(app):
    app.config['DATABASE'] = DATABASE
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['FILE_SIZE_MAX'] = FILE_SIZE_MAX
    app.config['MAX_CONTENT_LENGTH'] = FILE_SIZE_MAX # flask's max content length
    app.config['LOG_FOLDER'] = LOG_FOLDER
    app.config['ROOT_FOLDER'] = ROOT_FOLDER
    app.config['DATABASE_FOLDER'] = DATABASE_FOLDER
    app.config['DATABASE_FILE'] = DATABASE_FILE
    app.config['HOST'] = HOST
    app.config['PORT'] = PORT
    app.config['API_URL'] = API_URL
    app.config['OPENAI_API_KEY'] = OPENAI_API_KEY
    app.config['AZURE_TTS_KEY'] = AZURE_TTS_KEY
    app.config['AZURE_TTS_REGION'] = AZURE_TTS_REGION
    app.config['AZURE_TTS_VOICE'] = AZURE_TTS_VOICE
    app.config['ELEVENLABS_API_KEY'] = ELEVENLABS_API_KEY