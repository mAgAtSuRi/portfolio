from app.models.ingredients import Ingredients
from app.crud.sqlalchemy_repository import SqlAlchemyRepository
from app.models.shopping_cart_items import ShoppingCartItems

class IngredientsRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, Ingredients)

    def get_by_recipe(self, recipe_id):
        return self.session.query(self.model).filter_by(recipe_id=recipe_id).all()

    def get_cart_item_by_name(self, name, cart_id):
        return (
            self.session.query(ShoppingCartItems)
            .join(self.model)
            .filter(
                ShoppingCartItems.shopping_cart_id == cart_id,
                self.model.name == name,
                self.model.recipe_id.is_(None)
            )
            .first()
        )
