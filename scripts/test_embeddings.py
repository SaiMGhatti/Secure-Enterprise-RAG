from app.retrieval.embeddings import EmbeddingService


def main():
    embedding_service = EmbeddingService()

    text = """
    Employees must submit vacation requests at least
    two weeks before the planned vacation date.
    """

    vector = embedding_service.embed_text(text)

    print("Embedding generated successfully")
    print(f"Vector dimension: {len(vector)}")
    print(f"First 10 values: {vector[:10]}")


if __name__ == "__main__":
    main()