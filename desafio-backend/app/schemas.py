from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Product(BaseModel):
    productId: int
    quantity: int


class CartBase(BaseModel):
    user_id: int
    date: Optional[datetime] = None
    products: List[Product] = []


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int

    model_config = {
        "from_attributes": True  
    }
