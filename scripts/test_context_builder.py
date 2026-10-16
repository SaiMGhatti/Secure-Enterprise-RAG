from app.models.user import User

from app.retrieval.retriever import (
    retrieve,
)

from app.rag.context_builder import (
    build_retrieval_context,
)


def main():

    finance_user = User(
        user_id="finance_001",
        roles=[
            "employee",
            "finance",
            "manager",
        ],
        groups=[
            "finance"
        ],
    )

    query = (
        "Who can approve vendor payments?"
    )

    results = retrieve(
        query=query,
        user=finance_user,
        candidate_k=20,
        top_k=5,
    )

    context = build_retrieval_context(
        results
    )

    print(
        "\nGENERATED CONTEXT\n"
    )

    print(
        context.context_text
    )

    print(
        "\nSOURCES\n"
    )

    for source in context.sources:

        print(
            f"{source.source_id} | "
            f"{source.file_name} | "
            f"{source.section} | "
            f"Page {source.page_number}"
        )


if __name__ == "__main__":
    main()