from fastapi import FastAPI
from app.routers import documents
app = FastAPI(title="File Cert API")

@app.get("/")
async def root():
    return {"message": "System File Cert działa poprawnie"}

app.include_router(documents.router, prefix="/api", tags=["documents"])