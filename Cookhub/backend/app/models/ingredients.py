from ..db.base import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Float)
    price = Column(Integer)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True) #An ingredient can exist without recipe (ex: for shopping_cart)
