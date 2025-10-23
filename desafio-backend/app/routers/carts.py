from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import crud, schemas
from ..database import SessionLocal
from ..errors.exceptions import CartNotFoundException

router = APIRouter(prefix="/carts", tags=["carts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def map_products(products):
    mapped = []
    for p in products or []:
        mapped.append({
            "productId": p.get("productId") or p.get("id"),
            "quantity": p.get("quantity") or p.get("qty") or 0
        })
    return mapped


@router.get("/", response_model=List[schemas.Cart])
def read_carts(
    db: Session = Depends(get_db),
    user_id: Optional[int] = Query(default=None),
    start_date: Optional[datetime] = Query(default=None),
    end_date: Optional[datetime] = Query(default=None),
):
    carts = crud.get_carts(db, user_id=user_id, start_date=start_date, end_date=end_date)
    for c in carts:
        c.products = map_products(c.products)
    return carts


@router.get("/{cart_id}", response_model=schemas.Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db, cart_id)
    if db_cart is None:
        raise CartNotFoundException(cart_id)
    db_cart.products = map_products(db_cart.products)
    return db_cart


@router.post("/", response_model=schemas.Cart)
def create_cart_endpoint(cart: 
                         schemas.CartCreate, db: Session = Depends(get_db)):
    return crud.create_cart(db, cart)


@router.put("/{cart_id}", response_model=schemas.Cart)
def update_cart_endpoint(cart_id: int, cart: schemas.CartCreate, db: 
                         Session = Depends(get_db)):
    updated = crud.update_cart(db, cart_id, cart)
    if not updated:
        raise CartNotFoundException(cart_id)
    updated.products = map_products(updated.products)
    return updated


@router.delete("/{cart_id}")
def delete_cart_endpoint(cart_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_cart(db, cart_id)
    if not ok:
        raise CartNotFoundException(cart_id)
    return {"status": "ok", "deleted_id": cart_id}
