# recommender.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from collections import defaultdict
from datetime import datetime

# Import the *callable* collection accessors from your db module.
# If your db.py exposes functions like products_collection(), neighbors_collection(), transactions_collection()
# keep the parentheses when calling (e.g. products_collection()).
from ..db import products_collection, neighbors_collection, transactions_collection

router = APIRouter(prefix="/recommend", tags=["recommender"])

def normalize_product(doc: dict) -> dict:
    out = dict(doc)
    out["sku"] = doc["_id"]

    out["display_name"] = (
        doc.get("name")
        or doc.get("product_name")
        or doc.get("title")
        or str(doc["_id"])
    )

    del out["_id"]
    return out

@router.get("/sku/{sku}", summary="Recommend similar items for a SKU")
def recommend_by_sku(sku: str, k: int = Query(8, ge=1, le=50)):
    """
    Return top-k neighbors for a given SKU, with product metadata.
    """
    doc = neighbors_collection().find_one({"_id": sku})
    if not doc or "neighbors" not in doc:
        raise HTTPException(status_code=404, detail="neighbors not found")

    neighbors = doc["neighbors"][:k]
    skus = [n["sku"] for n in neighbors]

    prods_cursor = products_collection().find(
        {"_id": {"$in": skus}},
        {"_id": 1, "name": 1, "images": 1, "category": 1, "mrp": 1}
    )
    prods = list(prods_cursor)
    prod_map = {p["_id"]: p for p in prods}

    results = []
    for n in neighbors:
        item = prod_map.get(n["sku"])

        product = normalize_product(item) if item else None

        results.append({
            "sku": n["sku"],
            "score": float(n.get("score", 0.0)),
            "product": product
        })

    return {"sku": sku, "recommendations": results}


@router.get("/user/{user_id}", summary="Recommend products for user")
def recommend_for_user(user_id: int, k: int = Query(10, gt=0, le=50)):
    """
    Recommend products for a user by aggregating their purchases and scoring neighbors.
    """
    # 1) aggregate user's purchases
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": "$sku", "qty": {"$sum": "$quantity"}}},
        {"$sort": {"qty": -1}}
    ]
    bought = list(transactions_collection().aggregate(pipeline))
    if not bought:
        # cold start -> popular items
        pop_cursor = products_collection().find({}, {"_id": 1}).sort("units_sold", -1).limit(k)
        popular_ids = [p["_id"] for p in pop_cursor]
        return {
            "user_id": user_id,
            "recommendations": popular_ids,
            "computed_at": datetime.utcnow().isoformat()
        }

    # 2) score neighbors by qty * similarity
    score = defaultdict(float)
    bought_map = {b["_id"]: b["qty"] for b in bought}
    for sku, qty in bought_map.items():
        nbr_doc = neighbors_collection().find_one({"_id": sku})
        if not nbr_doc or "neighbors" not in nbr_doc:
            continue
        for nb in nbr_doc["neighbors"]:
            score[nb["sku"]] += qty * float(nb.get("score", 0.0))

    # 3) exclude already bought
    for sku in bought_map.keys():
        score.pop(sku, None)

    # 4) sort and pad with popular if needed
    sorted_skus = [sku for sku, _ in sorted(score.items(), key=lambda x: -x[1])]
    if len(sorted_skus) < k:
        needed = k - len(sorted_skus)
        popular_cursor = products_collection().find(
            {"_id": {"$nin": sorted_skus}}
        ).sort("units_sold", -1).limit(needed)
        popular_add = [p["_id"] for p in popular_cursor]
        sorted_skus.extend(popular_add)

    return {
        "user_id": user_id,
        "recommendations": sorted_skus[:k],
        "computed_at": datetime.utcnow().isoformat()
    }
