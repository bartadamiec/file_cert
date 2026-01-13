# Logika JWT i hashowania haseł
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

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
