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
