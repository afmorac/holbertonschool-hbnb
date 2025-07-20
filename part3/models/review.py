from persistence.database import db
from models.base_model import BaseModel
import uuid

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # ✅ Foreign keys
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
