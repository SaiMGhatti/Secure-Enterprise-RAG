from pathlib import Path

from app.ingestion.loader import discover_documents
from app.ingestion.parsers.factory import ParserFactory


ROOT = Path("data/documents")


def main():

    processed = 0
    failed = 0

    for file_path in discover_documents(ROOT):

        print("=" * 80)
        print(f"File: {file_path}")
        print(f"Type: {file_path.suffix}")

        try:

            parser = ParserFactory.get_parser(file_path)

            document = parser.parse(file_path)

            print(f"Title: {document.title}")
            print(f"Characters: {len(document.text)}")

            print("\nPreview:")
            print(document.text[:500])

            processed += 1

        except Exception as exc:

            failed += 1

            print(
                f"ERROR processing {file_path}: {exc}"
            )

    print("\n" + "=" * 80)
    print(f"Processed: {processed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()