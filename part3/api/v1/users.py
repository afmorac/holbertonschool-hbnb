# api/v1/users.py

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService
from persistence.facade import DBFacade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'email': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'password': fields.String
})

facade = DBFacade()
service = UserService()

@api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Update user info (admin can update any, users only their own, except email/password)"""
        current_user = get_jwt_identity()
        data = request.json

        if not current_user:
            return {'error': 'Unauthorized'}, 401

        if not current_user.get('is_admin') and current_user.get('id') != user_id:
            return {'error': 'Unauthorized action'}, 403

        if not current_user.get('is_admin') and ('email' in data or 'password' in data):
            return {'error': 'You cannot modify email or password'}, 400

        if 'email' in data:
            existing = facade.get_user_by_email(data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        user = service.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model)
    def post(self):
        """Create a new user (admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        user = service.create_user(data)
        return user.to_dict(), 201
