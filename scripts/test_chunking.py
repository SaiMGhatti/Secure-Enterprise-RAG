from pathlib import Path

from app.ingestion.loader import discover_documents
from app.ingestion.parsers.factory import ParserFactory
from app.ingestion.document_builder import build_document_record
from app.ingestion.chunker import chunk_document


ROOT = Path("data/documents")


def main():
    total_documents = 0
    total_chunks = 0

    for file_path in discover_documents(ROOT):

        parser = ParserFactory.get_parser(file_path)

        parsed_document = parser.parse(file_path)

        record = build_document_record(parsed_document)

        chunks = chunk_document(record)

        total_documents += 1
        total_chunks += len(chunks)

        print("=" * 80)
        print(f"Document: {record.file_name}")
        print(f"Document ID: {record.document_id}")
        print(f"Category: {record.category}")
        print(f"Chunks: {len(chunks)}")

        for chunk in chunks[:2]:
            print("\n--- Chunk ---")
            print(f"Chunk ID: {chunk.chunk_id}")
            print(f"Chunk Index: {chunk.chunk_index}")
            print(f"Roles: {chunk.allowed_roles}")
            print(f"Text:\n{chunk.text[:300]}")

    print("\n" + "=" * 80)
    print(f"Documents processed: {total_documents}")
    print(f"Total chunks: {total_chunks}")


if __name__ == "__main__":
    main()