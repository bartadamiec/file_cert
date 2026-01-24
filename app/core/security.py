# JWT and password hashing
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.config import OAUTH2_SCHEME

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password: str):
    """
    Hashing password

    :param password:  Password to hash
    :type password: str
    :return: Hashed password
    """
    return password_context.hash(secret=password, scheme='bcrypt')

def verify_password(password: str, hashed_password: str):
    """
    Checking if password matches with hash

    :param password: Raw password
    :param hashed_password: Hashed password
    :return: boolean
    """
    return password_context.verify(secret=password, hash=hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token with defined expiration time

    :param data: Dictionary containing payload data
    :param expires_delta: Optional time delta for expiration
    :return: Encoded JWT string
    """

    to_encode = data.copy()

    # setting the expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta # custom expiring time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # basic expiring time

    to_encode.update({"exp": expire}) # updating expiring time to token
    # encoding the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def get_current_user(token: str = Depends(OAUTH2_SCHEME)):
    """
    Validates the token and retrieves the current user identifier

    :param token: JWT token string provided by dependency
    :return: User identifier (subject) from token payload
    """
    try:
        # decoding the token to get payload
        encoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return encoded_token["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Expired token")