from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

SECRET = "MODERATION_SECRET"

oauth = OAuth2PasswordBearer(tokenUrl="login")


def create_token(username):

    return jwt.encode(
        {"user": username},
        SECRET,
        algorithm="HS256"
    )


def verify(token: str = Depends(oauth)):

    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(401, "Invalid Token")
