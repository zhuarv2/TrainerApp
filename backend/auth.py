import os
from dotenv import load_dotenv
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from backend.database import SessionLocal
from backend.models import User

password_hasher = PasswordHash.recommended()

def hash_password(password:str)->str:
    password_hash = password_hasher.hash(password)
    return password_hash

def verify_password(password:str, password_hash)->bool:
    return password_hasher.verify(password, password_hash)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALG = os.getenv("ALG")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_token_access(data:dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, ALG)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token:str=Depends(oauth2_scheme)):
    session = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, ALG)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id==int(user_id)).first()
            if user is None:
                raise HTTPException(status_code=401, detail="User not found")
            return user
        finally:
            session.close()
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
