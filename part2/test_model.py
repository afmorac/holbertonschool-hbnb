import sys
import os

# Añadir el path de 'app' al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from models.base_model import BaseModel

obj = BaseModel()
print(obj.to_dict())
