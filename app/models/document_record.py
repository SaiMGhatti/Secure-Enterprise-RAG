from pydantic import BaseModel, Field
from typing import List, Optional


class DocumentRecord(BaseModel):
    document_id: str

    source_path: str
    file_name: str
    file_type: str

    title: Optional[str] = None

    category: str
    department: Optional[str] = None

    effective_date: Optional[str] = None
    access_classification: Optional[str] = None

    version: int = 1
    content_hash: str

    allowed_roles: List[str] = Field(default_factory=list)
    allowed_users: List[str] = Field(default_factory=list)
    allowed_groups: List[str] = Field(default_factory=list)

    text: str