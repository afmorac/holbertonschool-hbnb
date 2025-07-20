from services.repositories.user_repository import UserRepository
from models.user import User

class DBFacade:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, data):
        user = User(**data)
        user.hash_password(data['password'])  # Hashea la contraseña antes de guardar
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)
