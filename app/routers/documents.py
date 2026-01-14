# Obsługa plików (/upload, /sign, /verify)
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.signer import sign_pdf_service
from fastapi.responses import FileResponse
from app.services.validator import verify_pdf_service
from app.services.report_generator import report_generator_service
from app.core.security import get_current_user
import shutil
from app.models.schemas import SignRequest,  VerifyRequest
import os
from pathlib import Path

router = APIRouter()

@router.post("/upload")
async def upload_file(
        file: UploadFile = File(),
        current_user: str = Depends(get_current_user)):

    if not file.filename.endswith(".pdf"): # Walidacja czy to plik .pdf
        raise HTTPException(status_code=400, detail="Invalid extension. Must be .pdf file")

    save_path = f"storage/{current_user}_{file.filename}"
    os.makedirs("storage", exist_ok=True) # Upewnienie czy folder istnieje

    with open(save_path, "wb") as buffer: # saving file on the server
        shutil.copyfileobj(file.file, buffer)
    return file.filename

@router.post("/sign")
def sign_file(
        request: SignRequest,
        current_user: str = Depends(get_current_user)): # bez async, bo błąd asyncio

    input_pdf_path = os.path.join("storage", f"{current_user}_{request.filename}")
    p12_path = os.path.join("storage", f"{current_user}.p12")

    if not os.path.exists(input_pdf_path):
        raise HTTPException(status_code=404, detail="Upload PDF file first")
    if not os.path.exists(p12_path):
        raise HTTPException(status_code=404, detail="Cert not found")

    output_filename = f"{current_user}_" + request.filename.replace(".pdf", "_signed.pdf")
    output_pdf_path = os.path.join("storage", output_filename)

    # Funkcja podpisująca
    try:
        sign_pdf_service(
            input_pdf_path=input_pdf_path,
            output_pdf_path=output_pdf_path, # ścieżka, gdzie pojawi się podpisany dokument
            p12_path=p12_path, # ścieżka do kontenera, który zawiera metadane
            p12_password=request.password # password to container
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sign Error: {str(e)}")

    return FileResponse(path=output_pdf_path, filename=output_filename[len(current_user) + 1:])

# @router.get("/sign")
# def download_file(request: DownloadFile):
#     file_path

@router.post("/verify")
def verify_file(
        request: VerifyRequest,
        current_user: str = Depends(get_current_user)):

    pdf_to_check = os.path.join("storage", f"{current_user}_{request.filename}")

    if not os.path.exists(pdf_to_check):
        raise HTTPException(status_code=404, detail="File doesn't exists!")

    is_valid, results = verify_pdf_service(pdf_to_check)

    pdf_report = report_generator_service(pdf_to_check, results)

    return FileResponse(path = Path(pdf_report), filename=f"{request.filename[:-4]}_report.pdf")
     #     {
     #    "filename": request.filename,
     #    "status": "valid" if is_valid else "invalid",
     #    "results": results,
     #    "report_generated": True
     # }