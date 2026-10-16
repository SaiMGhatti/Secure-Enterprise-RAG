from app.retrieval.opensearch_client import get_opensearch_client


INDEX_NAME = "secure-rag-chunks"


def create_index():
    client = get_opensearch_client()

    if client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists")
        return

    mapping = {
        "settings": {
            "index": {
                "knn": True
            }
        },
        "mappings": {
            "properties": {
                "chunk_id": {
                    "type": "keyword"
                },
                "document_id": {
                    "type": "keyword"
                },
                "text": {
                    "type": "text"
                },
                "category": {
                    "type": "keyword"
                },
                "department": {
                    "type": "keyword"
                },
                "section": {
                    "type": "keyword"
                },
                "page_number": {
                    "type": "integer"
                },
                "chunk_index": {
                    "type": "integer"
                },
                "version": {
                    "type": "integer"
                },
                "content_hash": {
                    "type": "keyword"
                },
                "allowed_roles": {
                    "type": "keyword"
                },
                "allowed_users": {
                    "type": "keyword"
                },
                "allowed_groups": {
                    "type": "keyword"
                },
                "metadata": {
                    "type": "object"
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384
                }
            }
        }
    }

    client.indices.create(
        index=INDEX_NAME,
        body=mapping,
    )

    print(f"Created index: {INDEX_NAME}")