from sqlalchemy_repository import SqlAlchemyRepository
from ..models.shopping_cart_items import ShoppingCartItem


class ShoppingCartItemRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, ShoppingCartItem)

    def find_by_shopping_cart(self, shopping_cart_id):
        return (
            self.session.query(self.model)
            .filter_by(shopping_cart_id=shopping_cart_id)
            .all()
        )

    def find_by_ingredient(self, ingredient_id):
        return (
            self.session.query(self.model).filter_by(ingredient_id=ingredient_id).all()
        )

    def get_by_cart_and_ingredient(self, shopping_cart_id, ingredient_id):
        return (
            self.session.query(self.model)
            .filter_by(shopping_cart_id=shopping_cart_id, ingredient_id=ingredient_id)
            .first()
        )
