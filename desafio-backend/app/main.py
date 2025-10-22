from fastapi import FastAPI
from .database import engine, Base
from .routers import carts
from .models import Cart
from .errors.middleware import ExceptionMiddleware

app = FastAPI(title="Automax Cart API")

Base.metadata.create_all(bind=engine)

Cart.metadata.create_all(bind=engine)

app.include_router(carts.router)

app.add_middleware(ExceptionMiddleware)