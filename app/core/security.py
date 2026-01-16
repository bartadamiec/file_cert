# JWT and password hashing
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.config import OAUTH2_SCHEME

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password: str):
    return password_context.hash(secret=password, scheme='bcrypt')

def verify_password(password: str, hashed_password: str):
    return password_context.verify(secret=password, hash=hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # Ustalanie czasu wygasania
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def get_current_user(token: str = Depends(OAUTH2_SCHEME)):
    try:
        encoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return encoded_token["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Expired token")