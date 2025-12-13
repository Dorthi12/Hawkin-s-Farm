from .products import router as products_router
from .recommender import router as recommender_router
from .price import router as price_router
from .models_fs import router as models_fs_router

__all__ = [
    "products_router",
    "recommender_router",
    "price_router",
    "models_fs_router",
]
