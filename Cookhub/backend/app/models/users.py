from ..db.base import Base
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import validates
import bcrypt
import re


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    def __init__(self, username, email, password=None, is_admin=False):
        super().__init__()
        self.username = username
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hashed_password = self.hash_password(password)

    def hash_password(self, password):
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode("utf-8")

    def verify_password(self, password):
        password_bytes = password.encode("utf-8")
        hashed_bytes = self.hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    @validates('email')
    def validate_email(self, key, value):
        if not value or not value.strip():
            raise ValueError("Email can't be empty")
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format")
        return value.strip()