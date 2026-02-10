# settings
from fastapi.security import OAuth2PasswordBearer
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ROOT_CA_PASSWORD = os.getenv("ROOT_CA_PASSWORD")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 15
CERTS_DIR = "CERTS_DIR"
ROOT_CA_KEY = str(os.getenv("ROOT_CA_KEY"))
ROOT_CA_KEY_PATH = os.path.join(CERTS_DIR, ROOT_CA_KEY)
ROOT_CA_CERT = str(os.getenv("ROOT_CA_CERT"))
ROOT_CA_CERT_PATH = os.path.join(CERTS_DIR, ROOT_CA_CERT)
MONGO_PATH = os.getenv("MONGO_PATH")
DB_NAME = os.getenv("DB_NAME")
STORAGE = os.getenv("STORAGE")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")