from pathlib import Path

from app.ingestion.loader import discover_documents
from app.ingestion.parsers.factory import ParserFactory
from app.ingestion.document_builder import (
    build_document_record
)


ROOT = Path("data/documents")


def main():

    processed = 0
    failed = 0

    for file_path in discover_documents(ROOT):

        try:

            parser = ParserFactory.get_parser(
                file_path
            )

            parsed_document = parser.parse(
                file_path
            )

            record = build_document_record(
                parsed_document
            )

            print("=" * 80)

            print(
                f"Document: {record.file_name}"
            )

            print(
                f"ID: {record.document_id}"
            )

            print(
                f"Type: {record.file_type}"
            )

            print(
                f"Category: {record.category}"
            )

            print(
                f"Department: {record.department}"
            )

            print(
                f"Effective Date: "
                f"{record.effective_date}"
            )

            print(
                f"Classification: "
                f"{record.access_classification}"
            )

            print(
                f"Allowed Roles: "
                f"{record.allowed_roles}"
            )

            print(
                f"Content Hash: "
                f"{record.content_hash[:16]}..."
            )

            processed += 1

        except Exception as exc:

            failed += 1

            print(
                f"ERROR: {file_path}: {exc}"
            )

    print("\n" + "=" * 80)

    print(
        f"Processed: {processed}"
    )

    print(
        f"Failed: {failed}"
    )


if __name__ == "__main__":
    main()