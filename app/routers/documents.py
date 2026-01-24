# endpoints for files (/upload, /sign, /verify)
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

# uploading file to /storage
@router.post("/upload")
async def upload_file(
        file: UploadFile = File(),
        current_user: str = Depends(get_current_user)): # must be valid session

    if not file.filename.endswith(".pdf"): # file extension validation
        raise HTTPException(status_code=400, detail="Invalid extension. Must be .pdf file")

    save_path = f"storage/{current_user}_{file.filename}"
    os.makedirs("storage", exist_ok=True) # make storage dir if not exists

    with open(save_path, "wb") as buffer: # saving file on the server
        shutil.copyfileobj(file.file, buffer)
    return file.filename

# signing file from storage
@router.post("/sign")
def sign_file(    # without async due to asyncio error
        request: SignRequest,
        current_user: str = Depends(get_current_user)):  # must be valid session

    input_pdf_path = os.path.join("storage", f"{current_user}_{request.filename}") # path to file that will be signed
    p12_path = os.path.join("storage", f"{current_user}.p12") # user's container path

    # validation
    if not os.path.exists(input_pdf_path):
        raise HTTPException(status_code=404, detail="Upload PDF file first")
    if not os.path.exists(p12_path):
        raise HTTPException(status_code=404, detail="Cert not found")

    output_filename = f"{current_user}_" + request.filename.replace(".pdf", "_signed.pdf") # marking signed document
    output_pdf_path = os.path.join("storage", output_filename)

    # signing function
    try:
        sign_pdf_service(
            input_pdf_path=input_pdf_path,
            output_pdf_path=output_pdf_path, # path where signed document will be stored
            p12_path=p12_path, # path to container with metadata
            p12_password=request.password # password to container (same as to log in)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sign Error: {str(e)}")

    return FileResponse(path=output_pdf_path, filename=output_filename[len(current_user) + 1:]) # filename in storage is in format: <username>_<filename>_signed.pdf, endpoint returns without <username>_


@router.post("/verify")
def verify_file(
        request: VerifyRequest,
        current_user: str = Depends(get_current_user)):  # must be valid session
    # pdf to check path, client sends <filename>.pdf without, username or _signed suffix
    pdf_to_check = os.path.join("storage", f"{request.signer}_{request.filename[:-4]}_signed.pdf")

    if not os.path.exists(pdf_to_check):
        raise HTTPException(status_code=404, detail="File doesn't exists!")

    is_valid, results = verify_pdf_service(pdf_to_check) # verify_pdf_service returns boolean and results in JSON format

    pdf_report = report_generator_service(pdf_to_check, results) # returns path to report

    return FileResponse(path = Path(pdf_report), filename=f"{request.filename[:-4]}_report.pdf") # removing ".pdf" from filename