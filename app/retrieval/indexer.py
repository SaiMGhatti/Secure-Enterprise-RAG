from app.retrieval.embed_chunk import EmbeddedChunk
from app.retrieval.opensearch_client import get_opensearch_client
from app.retrieval.index import INDEX_NAME


def index_chunk(chunk: EmbeddedChunk):
    client = get_opensearch_client()

    document = {
        "chunk_id": chunk.chunk_id,
        "document_id": chunk.document_id,
        "text": chunk.text,

        "category": chunk.category,
        "department": chunk.department,
        "section": chunk.section,
        "page_number": chunk.page_number,

        "chunk_index": chunk.chunk_index,
        "version": chunk.version,
        "content_hash": chunk.content_hash,

        "allowed_roles": chunk.allowed_roles,
        "allowed_users": chunk.allowed_users,
        "allowed_groups": chunk.allowed_groups,

        "metadata": chunk.metadata,

        "embedding": chunk.embedding,
    }

    client.index(
        index=INDEX_NAME,
        id=chunk.chunk_id,
        body=document,
    )


def index_chunks(chunks: list[EmbeddedChunk]):
    client = get_opensearch_client()

    for chunk in chunks:
        index_chunk(chunk)

    client.indices.refresh(index=INDEX_NAME)

    print(f"Indexed {len(chunks)} chunks")