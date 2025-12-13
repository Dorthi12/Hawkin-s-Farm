# utils.py
from typing import List
from .db import products_collection
from pymongo import ASCENDING

def product_docs_to_dicts(skus: List[str]):
    """
    Fetch product docs for sku list, preserve order of skus.
    Returns list of product dicts (None items filtered out).
    """
    col = products_collection()
    docs = {d["_id"]: d for d in col.find({"_id": {"$in": skus}})}
    return [docs.get(s) for s in skus if docs.get(s)]

def ensure_indexes():
    col = products_collection()
    col.create_index([("category", ASCENDING)])
    col.create_index([("units_sold", -1)])
