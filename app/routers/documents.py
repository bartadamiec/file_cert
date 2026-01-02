# Obsługa plików (/upload, /sign, /verify)
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.signer import sign_pdf_service
import os
import shutil
from pydantic import BaseModel

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File()):
    if not file.filename.endswith(".pdf"): # Walidacja czy to plik .pdf
        raise HTTPException(status_code=400, detail="Invalid extension. Must be .pdf file")

    save_path = f"storage/{file.filename}"
    os.makedirs("storage", exist_ok=True) # Upewnienie czy folder istnieje

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file.filename

class SignRequest(BaseModel): # DTA, waliduje czy wszytko przesyła się do endpointu
    filename: str  # np. "umowa.pdf"
    p12_filename: str  # np. "moj_cert.p12"
    password: str

@router.post("/sign")
def sign_file(request: SignRequest): # bez async, bo błąd asyncio
    input_pdf_path = os.path.join("storage", request.filename)
    p12_path = os.path.join("certs", request.p12_filename)

    if not os.path.exists(input_pdf_path):
        raise HTTPException(status_code=404, detail="Plik PDF nie istnieje w folderze storage")
    if not os.path.exists(p12_path):
        raise HTTPException(status_code=404, detail="Certyfikat nie istnieje w folderze certs")

    output_filename = request.filename.replace(".pdf", "_signed.pdf")
    output_pdf_path = os.path.join("storage", output_filename)

    # Funkcja podpisująca
    try:
        sign_pdf_service(
            input_pdf_path=input_pdf_path,
            output_pdf_path=output_pdf_path, # ścieżka, gdzie pojawi się podpisany dokument
            p12_path=p12_path, # ścieżka do kontenera, który zawiera metadane
            p12_password=request.password # wyciągnięcie hasła z kontenera
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd podpisu: {str(e)}")

    return {
        "status": "success",
        "message": "Plik został podpisany",
        "signed_file": output_filename
    }