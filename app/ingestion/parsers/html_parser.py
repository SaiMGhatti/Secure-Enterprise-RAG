from pathlib import Path

from bs4 import BeautifulSoup

from app.models.parsed_document import ParsedDocument
from app.ingestion.parsers.base import DocumentParser


class HTMLParser(DocumentParser):

    def parse(self, file_path: Path) -> ParsedDocument:

        html = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        soup = BeautifulSoup(html, "lxml")

        # Remove non-content elements
        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        title = None

        if soup.title:
            title = soup.title.get_text(
                strip=True
            )

        text = soup.get_text(
            separator="\n",
            strip=True
        )

        return ParsedDocument(
            source_path=str(file_path),
            file_name=file_path.name,
            file_type="html",
            text=text,
            title=title or file_path.stem
        )