# Obsługa plików (/upload, /sign, /verify)
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.signer import sign_pdf_service
from fastapi.responses import FileResponse
from app.services.validator import verify_pdf_service
from app.services.report_generator import report_generator_service
import shutil
from app.models.schemas import SignRequest,  VerifyRequest
from pydantic import BaseModel
import os
from pathlib import Path

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


@router.post("/verify")
def verify_file(request: VerifyRequest):
    pdf_to_check = os.path.join("storage", request.filename)

    if not os.path.exists(pdf_to_check):
        raise HTTPException(status_code=404, detail="File doesn't exists!")

    is_valid, results = verify_pdf_service(pdf_to_check)

    report_generator_service(pdf_to_check, results)

    return FileResponse(path = Path(f'storage/{request.filename[:-4]}_report.pdf'), filename=f"{request.filename[:-4]}_report.pdf")
     #     {
     #    "filename": request.filename,
     #    "status": "valid" if is_valid else "invalid",
     #    "results": results,
     #    "report_generated": True
     # }