from sqlalchemy import Column, Integer, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=func.now())
    products = Column(JSON)