from fastapi import FastAPI
from app.routers import documents, auth
app = FastAPI(title="File Cert API")

@app.get("/")
async def root():
    return {"message": "Welcome to File Cert API!"}

app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(auth.router, prefix="/api", tags=["documents"])