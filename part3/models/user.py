from app import bcrypt

class User:
    def __init__(self, first_name, last_name, email):
        self.id = None  # se le asignará luego
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = None

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Serializa el usuario sin incluir la contraseña."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
