# crop_classifier.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, pandas as pd
from typing import Dict, Any, List
from ..models_loader import load_model

router = APIRouter(prefix="/crop", tags=["crop"])

# Accept any features as a dict (will be converted to DataFrame)
class CropRequest(BaseModel):
    features: Dict[str, Any]

class CropResponse(BaseModel):
    predicted_label: str
    predicted_proba: List[float] | None = None

@router.post("/predict", response_model=CropResponse)
def crop_predict(req: CropRequest):
    MODEL_NAME = "crop_pipeline"
    MODEL_PATH = os.getenv("CROP_PIPELINE_PATH", "app/models/crop_pipeline.pkl")
    try:
        pipeline = load_model(MODEL_NAME, MODEL_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Build DataFrame from the incoming dict; keep keys' order irrelevant
    X = pd.DataFrame([req.features])

    try:
        pred = pipeline.predict(X)[0]
        proba = None
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba(X)[0].tolist()
        # if label encoder used and pipeline returns numeric label, it might be handled inside pipeline
        return {"predicted_label": str(pred), "predicted_proba": proba}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"prediction error: {e}")
