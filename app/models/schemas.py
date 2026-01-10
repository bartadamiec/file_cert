# Np. jak wygląda JSON odpowiedzi
from pydantic import BaseModel

class SignRequest(BaseModel): # DTA, waliduje czy wszytko przesyła się do endpointu
    filename: str  # np. "umowa.pdf"
    p12_filename: str  # np. "moj_cert.p12"
    password: str


class VerifyRequest(BaseModel):
    filename: str  # np. "umowa.pdf"