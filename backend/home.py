from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get('HOST'), port=os.environ.get('PORT'))