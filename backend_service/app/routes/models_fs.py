# models_fs.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from bson import ObjectId
from ..db import db
import gridfs
import io

router = APIRouter(prefix="/models", tags=["models"])

fs = gridfs.GridFS(db)

@router.post("/upload", summary="Upload model file to GridFS")
async def upload_model(file: UploadFile = File(...), name: str | None = None):
    """
    Uploads a file to GridFS. Returns the GridFS id (string).
    Use header: Content-Type: multipart/form-data
    """
    contents = await file.read()
    fid = fs.put(contents, filename=file.filename, contentType=file.content_type, name=name)
    # save metadata doc
    meta = {
        "filename": file.filename,
        "gridfs_id": fid,
        "content_type": file.content_type,
        "name": name,
    }
    db.models.insert_one({**meta})
    return {"file_id": str(fid), "filename": file.filename, "name": name}

@router.get("/download/{file_id}", summary="Download model file from GridFS")
def download_model(file_id: str):
    """
    Download a file stored in GridFS by id (string).
    Returns a StreamingResponse for direct download.
    """
    try:
        g = fs.get(ObjectId(file_id))
    except Exception:
        raise HTTPException(status_code=404, detail="file not found")
    stream = io.BytesIO(g.read())
    return StreamingResponse(stream, media_type=g.content_type, headers={"Content-Disposition": f"attachment; filename={g.filename}"})

@router.get("/", summary="List uploaded models")
def list_models(limit: int = 50):
    docs = list(db.models.find().sort([("_id", -1)]).limit(limit))
    out = []
    for d in docs:
        d["gridfs_id"] = str(d["gridfs_id"])
        d["_id"] = str(d["_id"])
        out.append(d)
    return out
