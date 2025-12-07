# Obsługa plików (/upload, /sign, /verify)
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
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