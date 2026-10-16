from abc import ABC, abstractmethod
from pathlib import Path

from app.models.parsed_document import ParsedDocument


class DocumentParser(ABC):

    @abstractmethod
    def parse(self, file_path: Path) -> ParsedDocument:
        pass