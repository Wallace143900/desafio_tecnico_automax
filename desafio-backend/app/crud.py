from sqlalchemy.orm import Session
from . import models, schemas


def get_cart(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()


def get_carts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cart).offset(skip).limit(limit).all()


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
