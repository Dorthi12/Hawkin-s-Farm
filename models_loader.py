# models_loader.py
import os
import joblib
import tempfile
import gridfs
from bson import ObjectId
from .db import db
from fastapi import HTTPException
import logging

LOGGER = logging.getLogger(__name__)

def load_from_disk(path: str):
    if not os.path.exists(path):
        return None
    return joblib.load(path)

def load_from_gridfs_by_name(name: str):
    """Find a models doc by name in db.models and load its GridFS bytes."""
    try:
        doc = db.models.find_one({"name": name}, sort=[("_id", -1)])
        if not doc:
            return None
        fs = gridfs.GridFS(db)
        gridfs_id = doc.get("gridfs_id")
        if not gridfs_id:
            return None
        g = fs.get(gridfs_id)
        content = g.read()
        # write to temp file and load
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(content)
            tmp.flush()
            return joblib.load(tmp.name)
    except Exception as e:
        LOGGER.exception("gridfs load failed")
        raise HTTPException(status_code=500, detail=f"GridFS load error: {e}")

def load_model(name: str, local_path: str):
    """
    Try to load a model pipeline:
      1) from local_path
      2) fallback to GridFS using db.models with field name
    Returns the loaded object or raises RuntimeError
    """
    mdl = load_from_disk(local_path)
    if mdl is not None:
        return mdl
    mdl = load_from_gridfs_by_name(name)
    if mdl is not None:
        return mdl
    raise RuntimeError(f"Model '{name}' not found on disk ({local_path}) or GridFS.")
