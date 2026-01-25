from ..db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean


class ShoppingCartItem(Base):
    id = Column(Integer, primary_key=True)
    shopping_cart_id = Column(Integer, ForeignKey("shopping_cart.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    checked = Column(Boolean, nullable=False)
