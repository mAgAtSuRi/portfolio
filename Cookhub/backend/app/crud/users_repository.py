from ..models.users import User
from app.crud.sqlalchemy_repository import SqlAlchemyRepository


class UsersRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, User)

    def get_by_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()
