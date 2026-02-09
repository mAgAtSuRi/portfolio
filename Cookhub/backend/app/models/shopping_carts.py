from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class ShoppingCarts(Base):
    __tablename__ = "shopping_carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    total_cost = Column(Integer, default=0)

    users = relationship("User", back_populates="shopping_carts")
    shopping_cart_items = relationship("ShoppingCartItems", back_populates="shopping_carts")
