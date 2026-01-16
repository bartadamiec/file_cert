# pydantic models
from pydantic import BaseModel

class SignRequest(BaseModel): # DTA, validating if everything is the type we want
    filename: str  # e.g. "paper.pdf"
    password: str # the same password used to login


class VerifyRequest(BaseModel):
    filename: str  # e.g. "paper.pdf"
    signer: str # someone who we want to check if this someone sign the file