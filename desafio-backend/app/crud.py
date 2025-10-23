from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import models, schemas


def get_cart(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()


def get_carts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[models.Cart]:
    q = db.query(models.Cart)
    if user_id is not None:
        q = q.filter(models.Cart.user_id == user_id)
    if start_date is not None:
        q = q.filter(models.Cart.date >= start_date)
    if end_date is not None:
        q = q.filter(models.Cart.date <= end_date)
    return q.offset(skip).limit(limit).all()


def create_cart(db: Session, cart: schemas.CartCreate):
    db_cart = models.Cart(
        user_id=cart.user_id,
        date=cart.date,
        products=[p.model_dump() for p in cart.products],
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def update_cart(db: Session, cart_id: int, cart: schemas.CartCreate):
    db_cart = get_cart(db, cart_id)
    if not db_cart:
        return None
    db_cart.user_id = cart.user_id
    db_cart.date = cart.date
    db_cart.products = [p.model_dump() for p in cart.products]
    db.commit()
    db.refresh(db_cart)
    return db_cart


def delete_cart(db: Session, cart_id: int):
    db_cart = get_cart(db, cart_id)
    if not db_cart:
        return False
    db.delete(db_cart)
    db.commit()
    return True
