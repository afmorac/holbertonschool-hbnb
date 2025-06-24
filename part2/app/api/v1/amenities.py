from flask_restx import Namespace, Resource, fields
from app.services.app_facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Modelo para validación de entrada
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            data = api.payload
            new_amenity = facade.create_amenity(data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        return {"error": "Amenity not found"}, 404

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            data = api.payload
            updated = facade.update_amenity(amenity_id, data)
            if updated:
                return updated.to_dict(), 200
            return {"error": "Amenity not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400
