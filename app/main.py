from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="Agentic SOC Assistant",
    description="AI-powered SOC Analyst Assistant for cybersecurity investigation and automation.",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/", tags=["System"])
async def root():
    return {
        "application": "Agentic SOC Assistant",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "healthy",
    }