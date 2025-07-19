def create_amenity(data):
    from models.amenity import Amenity
    from app import db
    amenity = Amenity(name=data.get('name'))
    db.session.add(amenity)
    db.session.commit()
    return amenity

def update_amenity(amenity_id, data):
    from models.amenity import Amenity
    from app import db
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        return None
    amenity.name = data.get('name', amenity.name)
    db.session.commit()
    return amenity
