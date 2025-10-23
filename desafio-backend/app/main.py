import os
import asyncio
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .routers import carts
from .errors.middleware import ExceptionMiddleware
from .services import fetch_and_store_carts

app = FastAPI(title="Automax Cart API")


Base.metadata.create_all(bind=engine)


# CORS: allow specific origins by default; support wildcard via env
default_origins = [
    "http://localhost:5173",
    "https://desafio-frontend-alpha.vercel.app",
]
env_origins = os.getenv("ALLOWED_ORIGINS", "")
if env_origins:
    default_origins += [o.strip().rstrip("/") for o in env_origins.split(",") if o.strip()]

use_wildcard = any(o == "*" for o in default_origins)
if use_wildcard:
    cors_allow_origins = ["*"]
    cors_allow_credentials = False  # required when using '*'
else:
    cors_allow_origins = [o.rstrip("/") for o in default_origins]
    cors_allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_credentials=cors_allow_credentials,
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


# Scheduler simples (opcional) para sincronizar periodicamente
_scheduler_task: asyncio.Task | None = None


async def _scheduler_loop(interval_minutes: int):
    while True:
        try:
            db = next(get_db())  # abre sessão
            fetch_and_store_carts(db)
        except Exception:
            pass
        finally:
            try:
                db.close()
            except Exception:
                pass
        await asyncio.sleep(max(1, interval_minutes) * 60)


@app.on_event("startup")
async def _maybe_start_scheduler():
    global _scheduler_task
    try:
        interval = int(os.getenv("SYNC_INTERVAL_MINUTES", "0"))
    except ValueError:
        interval = 0
    if interval > 0 and _scheduler_task is None:
        _scheduler_task = asyncio.create_task(_scheduler_loop(interval))


@app.on_event("shutdown")
async def _stop_scheduler():
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
