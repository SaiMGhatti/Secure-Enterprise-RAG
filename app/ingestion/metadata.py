import hashlib
from pathlib import Path


def generate_document_id(file_path: Path) -> str:

    source = str(
        file_path.resolve()
    )

    return hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()[:16]