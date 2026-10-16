from pydantic import BaseModel


class SourceCitation(BaseModel):
    source_id: str
    document_id: str
    file_name: str | None = None
    category: str
    section: str | None = None
    page_number: int | None = None


class RetrievalContext(BaseModel):
    context_text: str
    sources: list[SourceCitation]