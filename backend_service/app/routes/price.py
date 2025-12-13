# price.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import os, joblib, numpy as np, pandas as pd
from ..models_loader import load_model   # uses disk or gridfs fallback

router = APIRouter(prefix="/price", tags=["price"])

class PriceRequest(BaseModel):
    mrp: float
    month: int
    units_sold: float
    category: str
    state: str

@router.post("/predict")
def price_predict(req: PriceRequest):
    """
    Loads the saved price_xgb_pipeline.pkl artifact (a dict with
    keys: 'xgb_model', 'num_imputer', 'encoder', 'features') and returns predicted price.
    """
    MODEL_NAME = "price_pipeline"
    MODEL_PATH = os.getenv("PRICE_MODEL_PATH", "app/models/price_xgb_pipeline.pkl")

    try:
        artifact = load_model(MODEL_NAME, MODEL_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"model load error: {e}")

    # artifact expected to be a dict saved by your Colab script
    if not isinstance(artifact, dict):
        raise HTTPException(status_code=500, detail="loaded artifact is not a dict")

    xgb_model = artifact.get("xgb_model")
    num_imp = artifact.get("num_imputer")
    enc = artifact.get("encoder")
    features = artifact.get("features")

    if xgb_model is None or num_imp is None or enc is None or features is None:
        raise HTTPException(status_code=500, detail="model artifact missing required pieces")

    # Build DataFrame and apply same preprocessing used in training
    sample = {
        "mrp": req.mrp,
        "month": req.month,
        "units_sold": req.units_sold,
        "category": req.category,
        "state": req.state
    }
    s = pd.DataFrame([sample])

    # replicate feature engineering done in Colab
    # NOTE: num_cols and cat_cols must match what you used in training script
    num_cols = ["log_mrp", "units_sold", "mrp"]
    cat_cols = ["category", "state"]

    # create derived features
    s["log_mrp"] = np.log1p(s["mrp"])
    s["month_sin"] = np.sin(2 * np.pi * s["month"] / 12)
    s["month_cos"] = np.cos(2 * np.pi * s["month"] / 12)

    # Impute numeric (num_imp was fit on training data)
    try:
        s[num_cols] = num_imp.transform(s[num_cols])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"numeric imputation error: {e}")

    # Encode categorical (encoder was fit on training)
    try:
        s[cat_cols] = enc.transform(s[cat_cols].astype(str))
    except Exception as e:
        # If encoding fails because of unseen categories, handle gracefully:
        # OrdinalEncoder with unknown_value was used; but still catch errors.
        raise HTTPException(status_code=500, detail=f"categorical encoding error: {e}")

    # Select features in the correct order expected by the model
    try:
        X = s[features].values  # features list was saved in artifact
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"feature selection error: {e}")

    # predict with XGBoost object (bst)
    try:
        import xgboost as xgb
        dmat = xgb.DMatrix(X)
        pred = xgb.Booster()
        # if artifact.xgb_model is an xgb.Booster object already, use it; else it's the returned object
        # Your script saved bst (xgb.Booster) under 'xgb_model'
        bst = xgb_model
        # If bst has a predict method expecting DMatrix:
        y_hat = bst.predict(dmat)
        predicted = float(y_hat[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"prediction error: {e}")

    return {"predicted_price": predicted}
