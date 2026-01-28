from ..db.base import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey


class Recipes(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Integer)  # attention prix stocké en centimes (1234 = 12,34)
