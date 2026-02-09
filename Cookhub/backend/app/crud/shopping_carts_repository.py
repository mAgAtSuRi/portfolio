from app.crud.sqlalchemy_repository import SqlAlchemyRepository
from app.models.shopping_carts import ShoppingCarts


class ShoppingCartRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, ShoppingCarts)

    def get_by_user(self, user_id):
        return self.session.query(self.model).filter_by(user_id=user_id).first()
