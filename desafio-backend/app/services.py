import requests
from sqlalchemy.orm import Session
from . import crud, schemas

FAKE_STORE_API_URL = "https://fakestoreapi.com/carts"


def fetch_and_store_carts(db: Session):
    response = requests.get(FAKE_STORE_API_URL)
    if response.status_code == 200:
        carts = response.json()
        for cart in carts:
            cart_data = schemas.CartCreate(
                user_id=cart["userId"],
                date=cart["date"],
                products=[schemas.Product(**p) for p in cart["products"]]
            )
            crud.create_cart(db, cart_data)
    else:
        print("Erro ao buscar dados da API externa")
