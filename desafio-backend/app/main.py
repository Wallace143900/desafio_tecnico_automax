from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .routers import carts
from .schemas import CartItem
from .models import Cart

app = FastAPI(title="Automax Cart API")

Base.metadata.create_all(bind=engine)

Cart.metadata.create_all(bind=engine)

app.include_router(carts.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/carts")
def create_cart(cart: CartItem, db: Session = Depends(get_db)):
    db_cart = Cart(user_id=cart.user_id, products=cart.products)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return {"message": "Carrinho criado com sucesso", "cart": db_cart.id}


@app.get("/carts")
def read_carts(db: Session = Depends(get_db)):
    carts = db.query(Cart).all()
    return carts