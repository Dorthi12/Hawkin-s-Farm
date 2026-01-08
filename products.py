# products.py
from fastapi import APIRouter, HTTPException
from ..db import products_collection
from typing import List

router = APIRouter(prefix="/products", tags=["products"])


def normalize_product(doc: dict) -> dict:
    """
    Ensures every product has:
    - sku
    - display_name (UI-safe)
    """
    out = {k: v for k, v in doc.items() if k != "_id"}
    out["sku"] = doc["_id"]

    # Guaranteed display name for frontend
    out["display_name"] = (
        out.get("name")
        or out.get("product_name")
        or out.get("title")
        or str(out["sku"])
    )

    return out


@router.get("/", summary="List products")
def list_products(limit: int = 50, skip: int = 0):
    col = products_collection()
    cursor = col.find().sort("units_sold", -1).skip(skip).limit(limit)

    return [normalize_product(doc) for doc in cursor]


@router.get("/{sku}", summary="Get product by SKU")
def get_product(sku: str):
    doc = products_collection().find_one({"_id": sku})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")

    return normalize_product(doc)


@router.post("/batch", summary="Get products by a list of SKUs")
def get_products_batch(skus: List[str]):
    col = products_collection()
    docs = {d["_id"]: d for d in col.find({"_id": {"$in": skus}})}

    return [
        normalize_product(docs[s])
        for s in skus
        if s in docs
    ]
