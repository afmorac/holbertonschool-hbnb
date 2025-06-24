from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.price = kwargs.get("price", 0.0)
        self.lat = kwargs.get("lat", 0.0)
        self.lon = kwargs.get("lon", 0.0)
        self.amenities = kwargs.get("amenities", [])

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._lat = float(value)

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._lon = float(value)
