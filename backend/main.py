import os
import shutil

from fastapi import FastAPI, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend.model import load_models
from backend.classifier import predict_nsfw, predict_violence
from backend.database import SessionLocal, ImageLog
from backend.schemas import ImageResponse
from backend.auth import create_token, verify


# ---------------- APP ----------------

app = FastAPI(title="Image Moderation API")


# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- BASE DIR ----------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------- STATIC FILES ----------------

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend"
)


# ---------------- UPLOAD DIR ----------------

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "temp")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------- MODELS ----------------

yolo, nsfw_model = load_models()


# ---------------- DATABASE ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"status": "Image Moderation API Running"}


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

    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
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

    # Auto delete temp file (recommended)
    if os.path.exists(path):
        os.remove(path)

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
