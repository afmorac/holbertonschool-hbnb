import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from models.amenity import Amenity

a = Amenity(
    name="Hot Tub",
    description="Private outdoor jacuzzi with mountain view"
)

print(a.to_dict())
