# Image Moderation System

## Start Database
docker-compose up

## Install
pip install -r requirements.txt

## Start API
uvicorn backend.main:app --reload

## Login
POST /login
admin / admin

## Upload
POST /upload

## Admin Panel
Open frontend/admin.html
