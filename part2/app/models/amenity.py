from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
