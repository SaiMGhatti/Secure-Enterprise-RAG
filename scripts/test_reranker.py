from app.models.user import User
from app.retrieval.retriever import retrieve


def main():

    finance_user = User(
        user_id="finance_001",
        departments=["Finance"],
        roles=[
            "employee",
            "finance",
            "manager",
        ],
        groups=[
            "finance"
        ],
    )

    queries = [
        "Who can approve vendor payments?",
        "What controls are required before financial transactions are processed?",
        "What is the procedure for reimbursement?",
    ]

    for query in queries:

        print("\n" + "=" * 80)

        print(f"QUERY: {query}")

        results = retrieve(
            query=query,
            user=finance_user,
            candidate_k=20,
            top_k=5,
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):

            source = result["_source"]

            print(
                f"\nRank: {rank}"
                f"\nRerank Score: "
                f"{result['rerank_score']:.4f}"
                f"\nRRF Score: "
                f"{result.get('rrf_score', 0):.6f}"
                f"\nDocument: "
                f"{source['document_id']}"
                f"\nCategory: "
                f"{source['category']}"
                f"\nText: "
                f"{source['text'][:300]}"
            )


if __name__ == "__main__":
    main()