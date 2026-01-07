# Logowanie (/login, /register)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import get_password_hash, verify_password, create_access_token
from typing import Annotated
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "jan@firma.pl": {
        "username": "jan@firma.pl",
        "password": "tajnehaslo"
    }
}

fake_users_db['jan@firma.pl']['password'] = get_password_hash(fake_users_db['jan@firma.pl']['password'])

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = fake_users_db.get(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    password = form_data.password
    hashed_password = user['password']
    if not verify_password(password, hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"sub": user['username']})

    return {
        "access_token" : token,
        "token_type" : "bearer"
    }