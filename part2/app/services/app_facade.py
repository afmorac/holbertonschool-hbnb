import re
from app.persistence.inmemory_repo import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review  

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # === USER METHODS ===
    def create_user(self, user_data):
        first = user_data.get("first_name", "").strip()
        last = user_data.get("last_name", "").strip()
        email = user_data.get("email", "").strip()

        if not first or not last or not email:
            raise ValueError("First name, last name, and email cannot be empty")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        user = User(first_name=first, last_name=last, email=email)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    # === AMENITY METHODS ===
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # === PLACE METHODS ===
    def create_place(self, place_data):
        title = place_data.get("title", "").strip()
        price = place_data.get("price", 0.0)
        lat = place_data.get("lat", 0.0)
        lon = place_data.get("lon", 0.0)
        owner_id = place_data.get("owner_id")

        if not title:
            raise ValueError("Title cannot be empty")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        if not owner_id or not self.user_repo.get(owner_id):
            raise ValueError("Owner not found")

        amenity_ids = place_data.get("amenities", [])
        for amenity_id in amenity_ids:
            if not self.amenity_repo.get(amenity_id):
                raise ValueError(f"Amenity {amenity_id} not found")

        new_place = Place(**place_data)
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner_id)
        place_dict = place.to_dict()

        if owner:
            place_dict["owner"] = owner.to_dict()

        amenities = []
        for amenity_id in place.amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity.to_dict())
        place_dict["amenities"] = amenities

        reviews = [
            review.to_dict()
            for review in self.review_repo.get_all()
            if review.place_id == place.id
        ]
        place_dict["reviews"] = reviews

        return place_dict

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [self.get_place(place.id) for place in places]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        return self.place_repo.get(place_id)

    # === REVIEW METHODS ===
    def create_review(self, review_data):
        comment = review_data.get("comment", "").strip()
        rating = review_data.get("rating", 0)
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if not comment:
            raise ValueError("Comment cannot be empty")
        if not user_id or not self.user_repo.get(user_id):
            raise ValueError("Invalid user ID")
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError("Invalid place ID")
        if not isinstance(rating, int) or not (0 <= rating <= 5):
            raise ValueError("Rating must be an integer between 0 and 5")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [
            review for review in self.review_repo.get_all()
            if review.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
