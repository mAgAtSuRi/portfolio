from ..models.recipes import Recipe
from sqlalchemy_repository import SqlAlchemyRepository


class RecipesRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, Recipe)

    def find_by_user(self, user_id):
        return self.session.query(self.model).filter_by(user_id=user_id).all()
