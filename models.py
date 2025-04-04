
from database import Base
from sqlalchemy import CheckConstraint, Column, Integer, String, ForeignKey

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, CheckConstraint('price >= 0', name='check_price_positive'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))