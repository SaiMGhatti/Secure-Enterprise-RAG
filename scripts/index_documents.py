from pathlib import Path

from app.ingestion.loader import discover_documents
from app.ingestion.parsers.factory import ParserFactory
from app.ingestion.document_builder import build_document_record
from app.ingestion.chunker import chunk_document

from app.retrieval.embeddings import EmbeddingService
from app.retrieval.embed_chunk import EmbeddedChunk
from app.retrieval.indexer import index_chunks


ROOT = Path("data/documents")


def main():

    embedding_service = EmbeddingService()

    all_embedded_chunks = []

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

        all_embedded_chunks.extend(embedded_chunks)

        print(
            f"{record.file_name}: "
            f"{len(embedded_chunks)} chunks"
        )

    index_chunks(all_embedded_chunks)

    print("\nIndexing complete")


if __name__ == "__main__":
    main()