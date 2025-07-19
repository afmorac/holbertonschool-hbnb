from models.amenity import Amenity
from persistence.database import db

class AmenityService:
    def create_amenity(self, data):
        name = data.get('name')
        if not name:
            return None
        amenity = Amenity(name=name)
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def update_amenity(self, amenity_id, data):
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None
        amenity.name = data.get('name', amenity.name)
        db.session.commit()
        return amenity
