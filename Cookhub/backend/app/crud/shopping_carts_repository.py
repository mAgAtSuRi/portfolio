from sqlalchemy_repository import SqlAlchemyRepository
from ..models.shopping_carts import ShoppingCart


class ShoppingCartRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, ShoppingCart)

    def get_by_user(self, user_id):
        return self.session.query(self.model).filter_by(user_id=user_id)
