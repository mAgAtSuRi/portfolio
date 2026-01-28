# Association table that allows to modify an ingredient without changing the ingredient in the recipe
from ..db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean


class ShoppingCartItems(Base):
    __tablename__ = "shopping_cart_items"

    id = Column(Integer, primary_key=True)
    shopping_cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Integer, nullable=False)
    checked = Column(Boolean, nullable=False, default=False)
