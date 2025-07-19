from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService
from persistence.facade import DBFacade

api = Namespace('admin', description='Admin operations')

user_model = api.model('AdminUser', {
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'password': fields.String
})

facade = DBFacade()
service = UserService()

@api.route('/users/<string:user_id>')
class AdminUserUpdate(Resource):
    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Admin can update any user, including email and password"""
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            existing = facade.get_user_by_email(email)
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        user = service.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
