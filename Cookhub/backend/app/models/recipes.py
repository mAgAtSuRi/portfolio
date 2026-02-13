from app.db.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class Recipes(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Integer)  # attention prix stocké en centimes (1234 = 12,34)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="recipes")
    ingredients = relationship("Ingredients", back_populates="recipe", cascade="all")
    shopping_cart_items = relationship("ShoppingCartItems", back_populates="recipes")