from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.auth import resolve_user
from app.models.user import User
from app.rag import service
from app.rag.llm import LLMError

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="Secure Enterprise RAG",
    version="1.0.0",
    description="Enterprise RAG system with document-level authorization",
)


@app.get("/", include_in_schema=False)
async def ui():
    return FileResponse(STATIC_DIR / "index.html")


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)


def current_user(authorization: str | None = Header(default=None)) -> User:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    user = resolve_user(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token")
    return user


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "secure-rag"
    }


@app.post("/query", response_model=service.QueryResult)
def query(request: QueryRequest, user: User = Depends(current_user)):
    try:
        return service.answer_query(request.query, user)
    except LLMError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc