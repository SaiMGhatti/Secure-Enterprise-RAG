from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import DocumentChunk
from app.models.document_record import DocumentRecord


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ],
)


def chunk_document(record: DocumentRecord) -> list[DocumentChunk]:
    texts = text_splitter.split_text(record.text)

    chunks = []

    for index, text in enumerate(texts):
        chunk = DocumentChunk(
            chunk_id=f"{record.document_id}_{index}",
            document_id=record.document_id,
            text=text,
            category=record.category,
            department=record.department,
            section=None,
            page_number=None,
            chunk_index=index,
            version=record.version,
            content_hash=record.content_hash,

            # IMPORTANT:
            # inherit ACL from the parent document
            allowed_roles=record.allowed_roles.copy(),
            allowed_users=record.allowed_users.copy(),
            allowed_groups=record.allowed_groups.copy(),

            metadata={
                "title": record.title,
                "file_name": record.file_name,
                "file_type": record.file_type,
                "effective_date": record.effective_date,
                "access_classification": record.access_classification,
            },
        )

        chunks.append(chunk)

    return chunks