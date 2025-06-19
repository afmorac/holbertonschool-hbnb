# part2/app/__init__.py

from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        return 'HBnB API is running'

    return app
