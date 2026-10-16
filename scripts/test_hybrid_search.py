from app.models.user import User
from app.retrieval.hybrid_search import hybrid_search


def main():

    users = {
        "employee": User(
            user_id="employee_001",
            departments=["HR"],
            roles=["employee"],
            groups=["general"],
        ),

        "finance": User(
            user_id="finance_001",
            departments=["Finance"],
            roles=[
                "employee",
                "finance",
            ],
            groups=["finance"],
        ),

        "security": User(
            user_id="security_001",
            departments=["IT"],
            roles=[
                "it",
                "security",
            ],
            groups=["security"],
        ),
    }

    tests = [
        (
            "employee",
            "vacation leave policy",
        ),
        (
            "finance",
            "vendor payment approval controls",
        ),
        (
            "security",
            "production access requirements",
        ),
    ]

    for user_name, query in tests:

        user = users[user_name]

        print("\n" + "=" * 80)

        print(f"USER: {user_name}")
        print(f"QUERY: {query}")

        results = hybrid_search(
            query=query,
            user=user,
            candidate_k=5,
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):

            source = result["_source"]

            print(
                f"\nRank: {rank}"
                f"\nRRF Score: "
                f"{result['rrf_score']:.6f}"
                f"\nDocument: "
                f"{source['document_id']}"
                f"\nCategory: "
                f"{source['category']}"
                f"\nRoles: "
                f"{source['allowed_roles']}"
                f"\nText: "
                f"{source['text'][:250]}"
            )


if __name__ == "__main__":
    main()