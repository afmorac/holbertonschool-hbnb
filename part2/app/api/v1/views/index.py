from flask_restx import Namespace, Resource

api = Namespace('index', description='Index endpoint')

@api.route('/')
class Index(Resource):
    def get(self):
        return {"message": "Welcome to the HBnB API!"}
