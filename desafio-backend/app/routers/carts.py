from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database
from ..errors.exceptions import CartNotFoundException

router = APIRouter(prefix="/carts", tags=["carts"])


def map_products(products):
    mapped = []
    for p in products:
        mapped.append({
            "productId": p.get("productId") or p.get("id"),
            "quantity": p.get("quantity") or p.get("qty")
        })
    return mapped


@router.get("/", response_model=List[schemas.Cart])
def read_carts(db: Session = Depends(database.get_db)):
    carts = crud.get_carts(db)
    for c in carts:
        c.products = map_products(c.products)
    return carts


@router.get(
    "/{cart_id}",
    response_model=schemas.Cart
)
def read_cart(
    cart_id: int,
    db: Session = Depends(database.get_db)
):
    db_cart = crud.get_cart(db, cart_id)
    if db_cart is None:
        raise CartNotFoundException(cart_id)
    db_cart.products = map_products(db_cart.products)
    return db_cart


@router.post(
    "/",
    response_model=schemas.Cart
)
def create_cart_endpoint(
    cart: schemas.CartCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_cart(db, cart)
