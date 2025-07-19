from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.review_service import ReviewService
from persistence.facade import DBFacade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'place_id': fields.String(required=True)
})

facade = DBFacade()
service = ReviewService()

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    def post(self):
        """Create a new review (Only for logged in users)"""
        current_user = get_jwt_identity()
        data = request.json
        data['user_id'] = current_user['id']

        # Optional: validate that place exists
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Invalid place_id'}, 400

        review = service.create_review(data)
        return review.to_dict(), 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @jwt_required()
    @api.expect(review_model)
    def put(self, review_id):
        """Update a review (Only owner or admin)"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        is_admin = current_user.get('is_admin', False)
        if not is_admin and review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        updated_review = service.update_review(review_id, data)
        return updated_review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (Only owner or admin)"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        is_admin = current_user.get('is_admin', False)
        if not is_admin and review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        service.delete_review(review_id)
        return {'message': 'Review deleted'}, 200
