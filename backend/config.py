from os import getenv
import os

def register_config(app):
    app.config['DATABASE'] = "books.db"
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['FILE_SIZE_MAX'] = 5 * 1024 * 1024 # 5 MB
    app.config['LOG_FOLDER'] = "logs"
