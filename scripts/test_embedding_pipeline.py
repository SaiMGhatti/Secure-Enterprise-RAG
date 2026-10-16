from pathlib import Path

from app.ingestion.loader import discover_documents
from app.ingestion.parsers.factory import ParserFactory
from app.ingestion.document_builder import build_document_record
from app.ingestion.chunker import chunk_document

from app.retrieval.embeddings import EmbeddingService
from app.retrieval.embed_chunk import EmbeddedChunk


ROOT = Path("data/documents")


def main():
    embedding_service = EmbeddingService()

    total_documents = 0
    total_chunks = 0

    for file_path in discover_documents(ROOT):

        parser = ParserFactory.get_parser(file_path)

        parsed_document = parser.parse(file_path)

        record = build_document_record(parsed_document)

        chunks = chunk_document(record)

        texts = [chunk.text for chunk in chunks]

        embeddings = embedding_service.embed_documents(texts)

        embedded_chunks = [
            EmbeddedChunk.from_chunk(chunk, embedding)
            for chunk, embedding in zip(chunks, embeddings)
        ]

        total_documents += 1
        total_chunks += len(embedded_chunks)

        print("=" * 80)
        print(f"Document: {record.file_name}")
        print(f"Chunks: {len(embedded_chunks)}")

        if embedded_chunks:
            first = embedded_chunks[0]

            print(f"Chunk ID: {first.chunk_id}")
            print(f"Embedding dimensions: {len(first.embedding)}")
            print(f"ACL roles: {first.allowed_roles}")

    print("\n" + "=" * 80)
    print(f"Documents processed: {total_documents}")
    print(f"Total chunks embedded: {total_chunks}")


if __name__ == "__main__":
    main()