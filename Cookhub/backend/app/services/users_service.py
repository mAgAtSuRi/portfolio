from app.crud.users_repository import UsersRepository
from app.models.users import User
from sqlalchemy.exc import IntegrityError


class UsersFacade:
    def __init__(self, session):
        self.user_repo = UsersRepository(session)

    def create_user(self, username, email, password, is_admin):
        user = User(username, email, password, is_admin)
        try:
            self.user_repo.add(user)
            return user
        except IntegrityError:
            self.user_repo.session.rollback()
            raise ValueError("User with this email already exists")

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_user(self):
        return self.user_repo.list()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def update_password_user(self, user_id, new_password):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('User not found')
        new_hashed_password = user.hash_password(new_password)
        user.hashed_password = new_hashed_password
        self.user_repo.save()

    def update_email_user(self, user_id, new_email):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('User not found')
        try:
            user.email = new_email
            self.user_repo.save()
        except IntegrityError:
            raise ValueError("This email already exists")

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('User not found')
        self.user_repo.delete(user)
        return user
