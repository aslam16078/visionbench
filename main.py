
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from services.object_detection import detect_objects
app = FastAPI(
    title="VisionBench AI",
    description="Synthetic Visual Data Generation and AI Evaluation Platform",
    version="0.1.0",
)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "project": "VisionBench AI",
        "message": "Welcome to VisionBench AI",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "VisionBench AI",
        "version": "0.1.0",
    }


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image"
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detections = detect_objects(str(file_path))

    return {
        "filename": file.filename,
        "detections": detections,
        "total_objects": len(detections)
    }
