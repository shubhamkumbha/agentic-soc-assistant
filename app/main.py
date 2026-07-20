from fastapi import FastAPI

app = FastAPI(
    title="Agentic SOC Assistant",
    description="AI-powered SOC Analyst Assistant for cybersecurity investigation and automation.",
    version="0.1.0",
)


@app.get("/", tags=["System"])
async def root():
    return {
        "application": "Agentic SOC Assistant",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "healthy"
    }