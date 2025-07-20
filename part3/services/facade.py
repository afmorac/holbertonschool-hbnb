# AMENITY
def create_amenity(data):
    from models.amenity import Amenity
    from app import db
    amenity = Amenity(name=data.get('name'))
    db.session.add(amenity)
    db.session.commit()
    return amenity

def get_amenity(amenity_id):
    from models.amenity import Amenity
    return Amenity.query.get(amenity_id)

def get_all_amenities():
    from models.amenity import Amenity
    return Amenity.query.all()

def update_amenity(amenity_id, data):
    from models.amenity import Amenity
    from app import db
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        return None
    amenity.name = data.get('name', amenity.name)
    db.session.commit()
    return amenity

def delete_amenity(amenity_id):
    from models.amenity import Amenity
    from app import db
    amenity = Amenity.query.get(amenity_id)
    if amenity:
        db.session.delete(amenity)
        db.session.commit()

# PLACE
def create_place(data):
    from models.place import Place
    from app import db
    place = Place(
        title=data.get('title'),
        description=data.get('description'),
        price=data.get('price'),
        owner_id=data.get('owner_id')
    )
    db.session.add(place)
    db.session.commit()
    return place

def get_place(place_id):
    from models.place import Place
    return Place.query.get(place_id)

def get_all_places():
    from models.place import Place
    return Place.query.all()

def update_place(place_id, data):
    from models.place import Place
    from app import db
    place = Place.query.get(place_id)
    if not place:
        return None
    place.title = data.get('title', place.title)
    place.description = data.get('description', place.description)
    place.price = data.get('price', place.price)
    db.session.commit()
    return place

def delete_place(place_id):
    from models.place import Place
    from app import db
    place = Place.query.get(place_id)
    if place:
        db.session.delete(place)
        db.session.commit()

# REVIEW
def create_review(data):
    from models.review import Review
    from app import db
    review = Review(
        text=data.get('text'),
        rating=data.get('rating')
    )
    db.session.add(review)
    db.session.commit()
    return review

def get_review(review_id):
    from models.review import Review
    return Review.query.get(review_id)

def get_all_reviews():
    from models.review import Review
    return Review.query.all()

def update_review(review_id, data):
    from models.review import Review
    from app import db
    review = Review.query.get(review_id)
    if not review:
        return None
    review.text = data.get('text', review.text)
    review.rating = data.get('rating', review.rating)
    db.session.commit()
    return review

def delete_review(review_id):
    from models.review import Review
    from app import db
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
