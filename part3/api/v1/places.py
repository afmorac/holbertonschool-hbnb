from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.place_service import PlaceService
from persistence.facade import DBFacade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float
})

facade = DBFacade()
service = PlaceService()

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    def post(self):
        """Create a new place (Only for logged in users)"""
        current_user = get_jwt_identity()
        data = request.json
        data['owner_id'] = current_user['id']
        place = service.create_place(data)
        return place.to_dict(), 201


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @jwt_required()
    @api.expect(place_model)
    def put(self, place_id):
        """Update a place (Only owner or admin)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        is_admin = current_user.get('is_admin', False)
        if not is_admin and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        updated_place = service.update_place(place_id, data)
        return updated_place.to_dict(), 200

    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Only owner or admin)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        is_admin = current_user.get('is_admin', False)
        if not is_admin and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        service.delete_place(place_id)
        return {'message': 'Place deleted'}, 200
