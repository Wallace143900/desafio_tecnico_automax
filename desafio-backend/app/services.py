import requests
from sqlalchemy.orm import Session
from . import crud, schemas

FAKE_STORE_API_URL = "https://fakestoreapi.com/carts"


def _map_products_external(products):
    mapped = []
    for p in products or []:
        mapped.append({
            "productId": p.get("productId") or p.get("id"),
            "quantity": p.get("quantity") or p.get("qty") or 0
        })
    return mapped


def fetch_and_store_carts(db: Session):
    resp = requests.get(FAKE_STORE_API_URL, timeout=30)
    resp.raise_for_status()
    carts = resp.json()

    for cart in carts:
        cart_data = schemas.CartCreate(
            user_id=cart["userId"],
            date=cart.get("date"),
            products=[schemas.Product(**p) 
                      for p in _map_products_external(cart.get("products", []))
                      
                      ]
        )
        crud.create_cart(db, cart_data)
