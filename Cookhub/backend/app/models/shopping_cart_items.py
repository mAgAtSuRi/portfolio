# Association table that allows to modify an ingredient without changing the ingredient in the recipe
from ..db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship


class ShoppingCartItems(Base):
    __tablename__ = "shopping_cart_items"

    id = Column(Integer, primary_key=True)
    shopping_cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    quantity = Column(Float, nullable=False)
    # unit_price stored in cents (e.g. 12.79€ -> 1279)
    unit_price = Column(Integer, nullable=False)
    checked = Column(Boolean, nullable=False, default=False)

    # recipes = relationship("Recipes", back_populates="shopping_cart_items")
    # ingredients = relationship("Ingredients", back_populates="shopping_cart_items")
    # shopping_carts = relationship("Shopping_carts", back_populates="shopping_cart_items")
