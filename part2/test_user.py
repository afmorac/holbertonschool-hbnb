import sys
import os

# Añadir 'app/' al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from models.user import User

# Crear una instancia de User con datos de prueba
u = User(
    email="andres@example.com",
    password="holberton123",
    full_name="Andrés M. C.",
    first_name="Andrés",
    last_name="Morales",
    admin_flag=True
)
# Imprimir los datos como diccionario
print(u.to_dict())
