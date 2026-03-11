from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(title="Balance Hub OAuth")


@app.get("/")
async def root():
    return {"service": "Balance Hub OAuth", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/oauth/callback/{service_name}")
async def oauth_callback(service_name: str, code: str = None, error: str = None):
    """Endpoint для обработки OAuth колбэков"""
    if error:
        return {"error": error}
    # Логика обработки кода будет добавлена позже
    return {"service": service_name, "status": "code_received"}
