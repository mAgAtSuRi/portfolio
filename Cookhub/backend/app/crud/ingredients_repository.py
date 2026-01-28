from ..models.ingredients import Ingredient
from sqlalchemy_repository import SqlAlchemyRepository


class IngredientsRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, Ingredient)

    def get_by_recipe(self, recipe_id):
        return self.session.query(self.model).filter_by(recipe_id=recipe_id).all()
