import uuid
from datetime import datetime


class BaseModel:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))
        now = datetime.utcnow()
        self.created_at = kwargs.get("created_at", now)
        self.updated_at = kwargs.get("updated_at", now)

    def to_dict(self):
        result = self.__dict__.copy()
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result
