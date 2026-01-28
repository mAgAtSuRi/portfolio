from crud.users_repository import UsersRepository
from models.users import User


class UsersFacade:
    def __init__(self, session):
        self.user_repo = UsersRepository(session)

    def create_user(self, username, email, hashed_password):
        user = User(username, email, hashed_password)
        self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def update_password_user(self, user_id, new_password):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('User not found')
        new_hashed_password = user.hash_password(new_password)
        user.hashed_password = new_hashed_password

    def update_email_user(self, user_id, new_email):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('User not found')
        user.email = new_email

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('User not found')
        self.user_repo.delete(user)
