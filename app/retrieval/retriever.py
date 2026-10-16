from app.models.user import User
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.reranker import Reranker


reranker = Reranker()


def retrieve(
    query: str,
    user: User,
    candidate_k: int = 20,
    top_k: int = 5,
):
    candidates = hybrid_search(
        query=query,
        user=user,
        candidate_k=candidate_k,
    )

    return reranker.rerank(
        query=query,
        results=candidates,
        top_k=top_k,
    )