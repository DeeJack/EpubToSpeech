from os import getenv

def register_config(app):
    app.config['DATABASE'] = "books.db"
    app.config['UPLOAD_FOLDER'] = "static/uploads"
    app.config['FILE_SIZE_MAX'] = 5 * 1024 * 1024 # 5 MB
