# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from api.v1.users import api as users_ns
    from api.v1.auth import api as auth_ns
    from api.v1.places import api as places_ns
    from api.v1.reviews import api as reviews_ns
    from api.v1.admin import api as admin_ns
    from api.v1.amenities import api as amenities_ns

    api = Api(app, doc='/docs')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app
