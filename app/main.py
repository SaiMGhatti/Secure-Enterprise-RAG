from fastapi import FastAPI

app = FastAPI(
    title="Secure Enterprise RAG",
    version="1.0.0",
    description="Enterprise RAG system with document-level authorization",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "secure-rag"
    }