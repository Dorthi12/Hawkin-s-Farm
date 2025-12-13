from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import (
    products_router,
    recommender_router,
    price_router,
    models_fs_router,
)

app = FastAPI(title="Hawkins Farm - ML Service")

# -----------------------------------------
# CORS SETUP (updated & correct)
# -----------------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "*",   # optional (allow everything during dev)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------

# Register Routers
app.include_router(products_router)
app.include_router(recommender_router)
app.include_router(price_router)
app.include_router(models_fs_router)
