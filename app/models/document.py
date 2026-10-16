from enum import Enum
from pydantic import BaseModel, Field


class DocumentCategory(str, Enum):
    HR = "HR"
    IT = "IT"
    FINANCE = "Finance"
    LEGAL = "Legal"


class DocumentMetadata(BaseModel):
    document_id: str
    title: str
    category: DocumentCategory
    department: str

    allowed_roles: list[str] = Field(default_factory=list)
    allowed_users: list[str] = Field(default_factory=list)
    allowed_groups: list[str] = Field(default_factory=list)

    classification: str = "internal"
    version: int = 1