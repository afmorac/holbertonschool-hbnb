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
