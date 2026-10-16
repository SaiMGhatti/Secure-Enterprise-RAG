from pathlib import Path

from app.ingestion.parsers.base import DocumentParser
from app.ingestion.parsers.pdf_parser import PDFParser
from app.ingestion.parsers.html_parser import HTMLParser
from app.ingestion.parsers.text_parser import TextParser


class ParserFactory:

    _parsers = {
        ".pdf": PDFParser,
        ".html": HTMLParser,
        ".htm": HTMLParser,
        ".txt": TextParser,
    }

    @classmethod
    def get_parser(cls, file_path: Path) -> DocumentParser:

        extension = file_path.suffix.lower()

        parser_class = cls._parsers.get(extension)

        if not parser_class:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return parser_class()