# Ustawienia (np. ścieżka do folderu storage)
import os
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "wzpjvak-Y4xFR9IVbk8yPl7B8ubxWKF0ihdxWv0tnfE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
CERTS_DIR = "app/certs"
ROOT_CA_KEY_PATH = os.path.join(CERTS_DIR, "root_ca.key")
ROOT_CA_CERT_PATH = os.path.join(CERTS_DIR, "root_ca.crt")
MONGO_PATH = "mongodb://localhost:27017/"
STORAGE = "./storage"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")