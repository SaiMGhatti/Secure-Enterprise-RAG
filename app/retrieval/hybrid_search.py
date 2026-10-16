from app.models.user import User
from app.retrieval.embeddings import EmbeddingService
from app.retrieval.opensearch_client import get_opensearch_client
from app.retrieval.index import INDEX_NAME
from app.retrieval.acl_filter import build_acl_filter


embedding_service = EmbeddingService()


def vector_search(
    query: str,
    user: User,
    k: int = 10,
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
                                "k": k,
                            }
                        }
                    }
                ],
                "filter": [
                    build_acl_filter(user)
                ],
            }
        },
    }

    response = client.search(
        index=INDEX_NAME,
        body=search_body,
    )

    return response["hits"]["hits"]


def bm25_search(
    query: str,
    user: User,
    k: int = 10,
):
    client = get_opensearch_client()

    search_body = {
        "size": k,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "text": {
                                "query": query,
                            }
                        }
                    }
                ],
                "filter": [
                    build_acl_filter(user)
                ],
            }
        },
    }

    response = client.search(
        index=INDEX_NAME,
        body=search_body,
    )

    return response["hits"]["hits"]

def reciprocal_rank_fusion(
    result_sets: dict[str, list[dict]],
    k: int = 60,
):

    fused_scores = {}
    documents = {}
    retrieval_sources = {}

    for search_type, results in result_sets.items():

        for rank, result in enumerate(
            results,
            start=1,
        ):

            chunk_id = result["_id"]

            score = 1 / (k + rank)

            fused_scores[chunk_id] = (
                fused_scores.get(
                    chunk_id,
                    0,
                )
                + score
            )

            documents[chunk_id] = result

            retrieval_sources.setdefault(
                chunk_id,
                [],
            ).append(search_type)

    ranked_ids = sorted(
        fused_scores,
        key=fused_scores.get,
        reverse=True,
    )

    merged_results = []

    for chunk_id in ranked_ids:

        result = documents[chunk_id].copy()

        result["rrf_score"] = (
            fused_scores[chunk_id]
        )

        result["retrieval_sources"] = (
            retrieval_sources[chunk_id]
        )

        merged_results.append(result)

    return merged_results

def hybrid_search(
    query: str,
    user: User,
    candidate_k: int = 20,
):

    vector_results = vector_search(
        query=query,
        user=user,
        k=candidate_k,
    )

    bm25_results = bm25_search(
        query=query,
        user=user,
        k=candidate_k,
    )

    fused_results = reciprocal_rank_fusion(
        {
            "vector": vector_results,
            "bm25": bm25_results,
        }
    )

    return fused_results[:candidate_k]