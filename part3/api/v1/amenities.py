from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from persistence.facade import DBFacade
from services.amenity_service import AmenityService

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

facade = DBFacade()
service = AmenityService()

@api.route('/')
class AmenityList(Resource):
    @api.doc('get_all_amenities')
    def get(self):
        """Get all amenities (Public)"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @jwt_required()
    @api.expect(amenity_model)
    def post(self):
        """Create new amenity (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        amenity = service.create_amenity(data)
        return amenity.to_dict(), 201

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    def get(self, amenity_id):
        """Get amenity by ID (Public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update amenity (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        amenity = service.update_amenity(amenity_id, data)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
