from pathlib import Path

from app.models.document_record import DocumentRecord
from app.models.parsed_document import ParsedDocument

from app.ingestion.content_hash import (
    calculate_content_hash
)

from app.ingestion.metadata import (
    generate_document_id
)

from app.ingestion.metadata_extractor import (
    extract_metadata
)


def build_document_record(
    document: ParsedDocument
) -> DocumentRecord:

    file_path = Path(
        document.source_path
    )

    metadata = extract_metadata(
        document.text,
        file_path
    )

    content_hash = calculate_content_hash(
        document.text
    )

    document_id = generate_document_id(
        file_path
    )

    return DocumentRecord(
        document_id=document_id,

        source_path=document.source_path,
        file_name=document.file_name,
        file_type=document.file_type,

        title=document.title,

        category=metadata["category"],
        department=metadata["department"],

        effective_date=metadata["effective_date"],
        access_classification=(
            metadata["access_classification"]
        ),

        version=1,
        content_hash=content_hash,

        allowed_roles=metadata["allowed_roles"],
        allowed_users=metadata["allowed_users"],
        allowed_groups=metadata["allowed_groups"],

        text=document.text
    )