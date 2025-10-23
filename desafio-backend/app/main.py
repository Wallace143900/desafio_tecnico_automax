import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .routers import carts
from .errors.middleware import ExceptionMiddleware
from .services import fetch_and_store_carts

app = FastAPI(title="Automax Cart API")


Base.metadata.create_all(bind=engine)


default_origins = [
    "http://localhost:5173",
    "https://desafio-frontend-alpha.vercel.app",
]
extra_origins = os.getenv("ALLOWED_ORIGINS", "")
if extra_origins:
    default_origins += [o.strip().rstrip("/") for o in extra_origins.split(",") if o.strip()]

normalized_origins = [o.rstrip("/") for o in default_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=normalized_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(carts.router)


app.add_middleware(ExceptionMiddleware)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/sync", tags=["sync"])
def sync_carts(db: Session = Depends(get_db)):
    fetch_and_store_carts(db)
    return {"status": "ok", "message": "Carts sincronizados"}


@app.get("/")
def root():
    return {"status": "ok", "service": "Automax Cart API"}


@app.get("/healthz")
def healthz():
    return {"ok": True}
