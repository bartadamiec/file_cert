# Logowanie (/login, /register)
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import get_password_hash, verify_password, create_access_token
from typing import Annotated # Metadata for type hints
from app.db.database import users_collection
from app.services.ca_service import ca_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if users_collection.find_one({"username": form_data.username}):
        raise HTTPException(status_code=400, detail="Username already used. Please try another username.")
    else:
        try:
            password = form_data.password
            username = form_data.username

            users_collection.insert_one(
                {
                    "username": username,
                    "password": get_password_hash(password)
                }
            )

            content = ca_service(username=username, password=password)
            headers = {
                "Content-Disposition": f"attachment; filename={username}.p12"
            }
            msg = {"message" : f"{username} successfully registered!"}
            print(msg)
            with open(f"storage/{username}.p12", "wb") as f:
                f.write(content)

            return Response(content=content, headers=headers, media_type='application/x-pkcs12')
        except Exception as e:
            users_collection.delete_one({"username":form_data.username})
            raise HTTPException(status_code=400, detail=f"{e}Something went wrong, please try again.")


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = users_collection.find_one({"username":form_data.username})
        password = form_data.password
        hashed_password = user['password']
        if not verify_password(password, hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    except TypeError:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"sub": user['username']})

    return {
        "access_token" : token,
        "token_type" : "bearer"
    }