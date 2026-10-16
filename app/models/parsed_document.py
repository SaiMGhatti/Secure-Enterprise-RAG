from pydantic import BaseModel
from typing import Optional


class ParsedDocument(BaseModel):
    source_path: str
    file_name: str
    file_type: str
    text: str
    title: Optional[str] = None