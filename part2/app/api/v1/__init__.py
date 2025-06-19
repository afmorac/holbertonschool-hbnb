from flask import Flask
from flask_restx import Api
from api.v1.views.index import api as index_ns

app = Flask(__name__)
api = Api(app, title='HBnB API', version='1.0', description='HBnB clone API')

api.add_namespace(index_ns, path='/api/v1')
