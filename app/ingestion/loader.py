from pathlib import Path
from typing import Iterator


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".html",
    ".htm",
    ".txt",
}


def discover_documents(
    root_directory: str
) -> Iterator[Path]:

    root = Path(root_directory)

    for file_path in root.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        yield file_path