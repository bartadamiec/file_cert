# Np. jak wygląda JSON odpowiedzi
from pydantic import BaseModel

class SignRequest(BaseModel): # DTA, waliduje czy wszytko przesyła się do endpointu
    filename: str  # np. "umowa.pdf"
    password: str


class VerifyRequest(BaseModel):
    filename: str  # np. "umowa.pdf"
    signer: str