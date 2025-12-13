# products.py
from fastapi import APIRouter, HTTPException
from ..db import products_collection
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", summary="List products")
def list_products(limit: int = 50, skip: int = 0):
    col = products_collection()
    cursor = col.find().sort("units_sold", -1).skip(skip).limit(limit)
    out = []
    for doc in cursor:
        docout = {k: v for k, v in doc.items() if k != "_id"}
        docout["sku"] = doc["_id"]
        out.append(docout)
    return out

@router.get("/{sku}", summary="Get product by SKU")
def get_product(sku: str):
    doc = products_collection().find_one({"_id": sku})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    doc["sku"] = doc["_id"]
    del doc["_id"]
    return doc

@router.post("/batch", summary="Get products by a list of SKUs")
def get_products_batch(skus: List[str]):
    col = products_collection()
    docs = {d["_id"]: d for d in col.find({"_id": {"$in": skus}})}
    # preserve input order, filter missing
    return [docs[s] if isinstance(docs.get(s), dict) else None and None for s in skus]  # will be filtered by frontend
