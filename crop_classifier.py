# crop_classifier.py
import joblib

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
import traceback

@router.post("/predict", response_model=CropResponse)
def crop_predict(req: CropRequest):
    MODEL_NAME = "crop_pipeline"
    MODEL_PATH = os.getenv("CROP_PIPELINE_PATH", "app/models/crop_pipeline.pkl")

    pipeline = load_model(MODEL_NAME, MODEL_PATH)
    LABEL_ENCODER_PATH = os.getenv(
        "CROP_LABEL_ENCODER_PATH",
        "app/models/label_encoder.pkl"
    )

    label_encoder = joblib.load(LABEL_ENCODER_PATH)

    #X = pd.DataFrame([req.features])
    # Map frontend feature names → training feature names
    feature_map = {
        "nitrogen": "N",
        "phosphorus": "P",
        "potassium": "K"
    }

    mapped_features = {}

    for key, value in req.features.items():
        if key in feature_map:
            mapped_features[feature_map[key]] = value
        else:
            mapped_features[key] = value

    # Ensure all required features exist
    required_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

    missing = [f for f in required_features if f not in mapped_features]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required features: {missing}"
        )

    X = pd.DataFrame([mapped_features])

    try:
        print("INPUT COLUMNS:", X.columns.tolist())
        pred_encoded = pipeline.predict(X)[0]

        # Decode label
        pred_label = label_encoder.inverse_transform([pred_encoded])[0]

        proba = None
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba(X)[0].tolist()

        return {
            "predicted_label": str(pred_label),
            "predicted_proba": proba
        }

    except Exception as e:
        #traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {e}"
        )
