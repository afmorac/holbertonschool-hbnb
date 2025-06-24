from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.full_name = kwargs.get("full_name", "")
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.admin_flag = kwargs.get("admin_flag", False)

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
