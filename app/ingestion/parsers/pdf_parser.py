from pathlib import Path

import fitz

from app.models.parsed_document import ParsedDocument
from app.ingestion.parsers.base import DocumentParser


class PDFParser(DocumentParser):

    def parse(self, file_path: Path) -> ParsedDocument:

        pages = []

        with fitz.open(file_path) as document:

            for page_number, page in enumerate(document):

                text = page.get_text("text")

                if text.strip():
                    pages.append(
                        f"\n--- Page {page_number + 1} ---\n"
                        f"{text.strip()}"
                    )

        full_text = "\n".join(pages)

        return ParsedDocument(
            source_path=str(file_path),
            file_name=file_path.name,
            file_type="pdf",
            text=full_text,
            title=file_path.stem
        )