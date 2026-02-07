📌 Image Moderation System

Live Demo:
https://image-moderation-system.onrender.com/

📖 Overview

This project is an AI-powered image moderation backend that analyzes uploaded images and detects unsafe content using deep learning models. It provides confidence scores and a secure admin dashboard for review.

The system uses:

FastAPI for backend APIs

YOLO for object/violence detection

CNN for NSFW detection

PostgreSQL for data storage

JWT for authentication

Render Cloud for deployment

🏗️ System Architecture
User → FastAPI → ML Models → PostgreSQL → Admin Dashboard

⚙️ Tech Stack

Backend: FastAPI (Python)

ML: PyTorch (YOLO), TensorFlow (CNN)

Database: PostgreSQL

Auth: JWT

Deployment: Render Cloud

Frontend: HTML + JavaScript

📂 Project Structure
image-moderation-system/
│
├── backend/
├── models/
├── uploads/
├── frontend/
├── docker-compose.yml
├── requirements.txt
└── README.md

🚀 Live Deployment

Backend API and Docs:

https://image-moderation-system.onrender.com/docs


Admin Panel:

https://image-moderation-system.onrender.com/frontend/admin.html

🧪 Local Setup
1. Clone Repository
git clone <your-repo-url>
cd image-moderation-system

2. Start PostgreSQL
docker-compose up

3. Install Dependencies
pip install -r requirements.txt

4. Run Backend
uvicorn backend.main:app --reload


Server runs at:

http://localhost:8000

5. Open API Docs
http://localhost:8000/docs

🔐 Authentication
Login Endpoint
POST /login


Credentials:

Username: admin
Password: admin


Response:

access_token


Copy this token for authorization.

📤 Upload Image
Endpoint
POST /upload

Steps

Open /docs

Select /upload

Click "Try it out"

Upload image

Execute

Response:

{
  "filename": "image.jpg",
  "nsfw": 0.03,
  "violence": 0.01,
  "status": "SAFE"
}

🛡️ Admin Access
Authorize in Swagger

Open /docs

Click "Authorize"

Paste:

Bearer <your_token>


Authorize

View All Records
GET /admin/images


Returns moderation logs from database.

📊 Admin Dashboard
Open in Browser
frontend/admin.html


or (Deployed)

https://image-moderation-system.onrender.com/frontend/admin.html

Steps

Paste JWT token

Click Load

View moderation table

💾 Database

Each uploaded image is stored with:

Filename

NSFW score

Violence score

Status

Timestamp (optional)

Stored in PostgreSQL.

🧠 Testing Workflow

Login → Get Token

Upload Images

Check Scores

View Admin Table

Verify Database Records

☁️ Deployment (Render)

This project is deployed using Render with:

GitHub CI/CD

Free PostgreSQL

Environment Variables

Auto Build & Deploy

Database credentials are stored using:

DATABASE_URL

