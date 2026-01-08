from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.products import router as products_router
from app.routes.recommender import router as recommender_router
from app.routes.price import router as price_router
from app.routes.models_fs import router as models_fs_router
from app.routes.crop_classifier import router as crop_router


app = FastAPI(title="Hawkins Farm - ML Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(recommender_router)
app.include_router(price_router)
app.include_router(models_fs_router)
app.include_router(crop_router)

from app.routes.crop_classifier import router as debug_crop_router
app.include_router(debug_crop_router)
