from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class Product(BaseModel):
    productId: int
    quantity: int


class CartBase(BaseModel):
    user_id: int
    date: Optional[datetime] = None
    products: List[Product]


class CartItem(BaseModel):
    user_id: int
    products: List[Dict]


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int

    class Config:
        orm_mode = True
