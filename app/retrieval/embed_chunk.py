from typing import Any

from pydantic import BaseModel, Field

from app.models.chunk import DocumentChunk


class EmbeddedChunk(BaseModel):
    chunk_id: str
    document_id: str

    text: str

    category: str
    department: str | None = None
    section: str | None = None
    page_number: int | None = None

    chunk_index: int
    version: int
    content_hash: str

    allowed_roles: list[str] = Field(default_factory=list)
    allowed_users: list[str] = Field(default_factory=list)
    allowed_groups: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    embedding: list[float]

    @classmethod
    def from_chunk(
        cls,
        chunk: DocumentChunk,
        embedding: list[float],
    ) -> "EmbeddedChunk":

        return cls(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            text=chunk.text,
            category=chunk.category,
            department=chunk.department,
            section=chunk.section,
            page_number=chunk.page_number,
            chunk_index=chunk.chunk_index,
            version=chunk.version,
            content_hash=chunk.content_hash,
            allowed_roles=chunk.allowed_roles,
            allowed_users=chunk.allowed_users,
            allowed_groups=chunk.allowed_groups,
            metadata=chunk.metadata,
            embedding=embedding,
        )