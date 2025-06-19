import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from models.review import Review

r = Review(
    comment="Amazing place! So cozy and peaceful.",
    rating=5,
    place_id="1234-place-uuid",
    user_id="5678-user-uuid"
)

print(r.to_dict())
