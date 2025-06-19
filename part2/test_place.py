import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from models.place import Place

p = Place(
    title="Cabin in the Woods",
    description="Peaceful retreat surrounded by nature.",
    price=120.5,
    lat=18.4655,
    lon=-66.1057,
    amenities=["WiFi", "Jacuzzi", "Fireplace"]
)

print(p.to_dict())
