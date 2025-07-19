from persistence.database import db
import uuid

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    owner_id = db.Column(db.String(60), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'owner_id': self.owner_id
        }
