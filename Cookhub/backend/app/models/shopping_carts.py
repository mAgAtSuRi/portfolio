from ..db.base import Base
from sqlalchemy import Column, Integer, ForeignKey


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    total_cost = Column(Integer, default=0)