from typing import Any, List, Optional

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str

    text: str

    category: str
    department: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None

    chunk_index: int
    version: int
    content_hash: str

    # Security metadata — MUST be inherited by every chunk
    allowed_roles: List[str] = Field(default_factory=list)
    allowed_users: List[str] = Field(default_factory=list)
    allowed_groups: List[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)