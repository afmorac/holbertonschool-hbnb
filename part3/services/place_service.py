from models.place import Place
from persistence.database import db

class PlaceService:
    def create_place(self, data, owner_id):
        title = data.get('title')
        description = data.get('description', '')
        price = data.get('price', 0.0)

        if not title:
            return None

        place = Place(
            title=title,
            description=description,
            price=price,
            owner_id=owner_id
        )
        db.session.add(place)
        db.session.commit()
        return place

    def update_place(self, place_id, data):
        place = Place.query.get(place_id)
        if not place:
            return None

        place.title = data.get('title', place.title)
        place.description = data.get('description', place.description)
        place.price = data.get('price', place.price)
        db.session.commit()
        return place

    def delete_place(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            return False

        db.session.delete(place)
        db.session.commit()
        return True
