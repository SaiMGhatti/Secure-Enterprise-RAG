from pathlib import Path

from app.models.parsed_document import ParsedDocument
from app.ingestion.parsers.base import DocumentParser


class TextParser(DocumentParser):

    def parse(self, file_path: Path) -> ParsedDocument:

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return ParsedDocument(
            source_path=str(file_path),
            file_name=file_path.name,
            file_type="txt",
            text=text.strip(),
            title=file_path.stem
        )