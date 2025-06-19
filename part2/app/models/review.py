from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comment = kwargs.get("comment", "")
        self.rating = kwargs.get("rating", 0)
        self.place_id = kwargs.get("place_id", "")
        self.user_id = kwargs.get("user_id", "")
