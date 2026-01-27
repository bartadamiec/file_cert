# settings
from fastapi.security import OAuth2PasswordBearer
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ROOT_CA_PASSWORD = os.getenv("ROOT_CA_PASSWORD")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
CERTS_DIR = "app/certs"
ROOT_CA_KEY_PATH = os.path.join(CERTS_DIR, "root_ca.key")
ROOT_CA_CERT_PATH = os.path.join(CERTS_DIR, "root_ca.crt")
MONGO_PATH = "mongodb://localhost:27017/"
STORAGE = "./storage"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")