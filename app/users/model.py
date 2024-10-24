"""ORM model for user entity in database."""
from sqlalchemy import Boolean, Column, Integer, String

from app import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    full_name = Column(String)
    disabled = Column(Boolean)
    hashed_password = Column(String)
