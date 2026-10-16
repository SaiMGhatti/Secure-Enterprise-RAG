from app.models.user import User
from app.retrieval.embeddings import EmbeddingService
from app.retrieval.opensearch_client import get_opensearch_client
from app.retrieval.index import INDEX_NAME


embedding_service = EmbeddingService()


def build_acl_filter(user: User) -> dict:
    permissions = []

    if user.user_id:
        permissions.append(
            {
                "term": {
                    "allowed_users": user.user_id
                }
            }
        )

    if user.roles:
        permissions.append(
            {
                "terms": {
                    "allowed_roles": user.roles
                }
            }
        )

    if user.groups:
        permissions.append(
            {
                "terms": {
                    "allowed_groups": user.groups
                }
            }
        )

    return {
        "bool": {
            "should": permissions,
            "minimum_should_match": 1
        }
    }


def vector_search(
    query: str,
    user: User,
    k: int = 5,
    candidate_k: int = 20,
):
    client = get_opensearch_client()

    query_embedding = embedding_service.embed_text(query)

    search_body = {
        "size": k,
        "query": {
            "bool": {
                "must": [
                    {
                        "knn": {
                            "embedding": {
                                "vector": query_embedding,
                                "k": candidate_k
                            }
                        }
                    }
                ],
                "filter": [
                    build_acl_filter(user)
                ]
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body=search_body,
    )

    return response["hits"]["hits"]