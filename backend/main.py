import os
import shutil
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session

from backend.model import load_models
from backend.classifier import *
from backend.database import *
from backend.schemas import *
from backend.auth import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

yolo, nsfw_model = load_models()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- LOGIN ----------------

@app.post("/login")
def login(username: str, password: str):

    if username == "admin" and password == "admin":

        token = create_token(username)

        return {"access_token": token}

    return {"error": "invalid"}


# ---------------- UPLOAD ----------------

@app.post("/upload", response_model=ImageResponse)
async def upload(
    file: UploadFile,
    db: Session = Depends(get_db)
):

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path,"wb") as f:
        shutil.copyfileobj(file.file, f)

    nsfw = predict_nsfw(path, nsfw_model)
    violence = predict_violence(path, yolo)

    status = "SAFE"

    if nsfw > 0.6 or violence > 0.6:
        status = "FLAGGED"

    record = ImageLog(
        filename=file.filename,
        nsfw_score=nsfw,
        violence_score=violence,
        status=status
    )

    db.add(record)
    db.commit()

    return {
        "filename": file.filename,
        "nsfw": nsfw,
        "violence": violence,
        "status": status
    }


# ---------------- ADMIN ----------------

@app.get("/admin/images")
def get_all(
    db: Session = Depends(get_db),
    user=Depends(verify)
):

    return db.query(ImageLog).all()
