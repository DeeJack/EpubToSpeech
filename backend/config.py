from os import getenv
import os

DATABASE = "books.db"
UPLOAD_FOLDER = os.path.join('static', 'uploads')
FILE_SIZE_MAX = 5 * 1024 * 1024 # 5 MB
LOG_FOLDER = "logs"
ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_FOLDER = "database"
DATABASE_FILE = "books.db"

def register_config(app):
    app.config['DATABASE'] = DATABASE
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['FILE_SIZE_MAX'] = FILE_SIZE_MAX
    app.config['LOG_FOLDER'] = LOG_FOLDER
    app.config['ROOT_FOLDER'] = ROOT_FOLDER
