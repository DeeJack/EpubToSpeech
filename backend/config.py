from flask import current_app
from os import getenv

current_app.config['DATABASE'] = "books.db"