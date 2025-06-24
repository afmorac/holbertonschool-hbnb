from flask import Flask
from config import Config
from app.api import blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(blueprint)

    @app.route('/')
    def index():
        return 'HBnB API is running!!!!!!'

    return app
