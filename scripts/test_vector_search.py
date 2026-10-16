from app.models.user import User
from app.retrieval.vector_search import vector_search


def print_results(results):

    if not results:
        print("No authorized results found.")
        return

    for rank, result in enumerate(results, start=1):

        source = result["_source"]

        print(
            f"\nRank {rank}"
            f"\nScore: {result['_score']}"
            f"\nFile: {source['metadata'].get('file_name')}"
            f"\nCategory: {source['category']}"
            f"\nRoles: {source['allowed_roles']}"
            f"\nUsers: {source['allowed_users']}"
            f"\nGroups: {source['allowed_groups']}"
            f"\nText: {source['text'][:300]}"
        )


def main():

    employee = User(
        user_id="employee_001",
        departments=["HR"],
        roles=["employee"],
        groups=["general"],
    )

    finance_user = User(
        user_id="finance_001",
        departments=["Finance"],
        roles=["employee", "finance"],
        groups=["finance"],
    )

    security_user = User(
        user_id="security_001",
        departments=["IT"],
        roles=["it", "security"],
        groups=["security"],
    )

    tests = [
        (
            employee,
            "How many days of vacation can employees take?"
        ),
        (
            employee,
            "Who can approve financial transactions?"
        ),
        (
            finance_user,
            "Who can approve financial transactions?"
        ),
        (
            security_user,
            "How should employees respond to security incidents?"
        ),
    ]

    for user, query in tests:

        print("\n" + "=" * 80)

        print(f"USER: {user.user_id}")
        print(f"ROLES: {user.roles}")
        print(f"GROUPS: {user.groups}")
        print(f"QUERY: {query}")

        results = vector_search(
            query=query,
            user=user,
            k=3,
        )

        print_results(results)


if __name__ == "__main__":
    main()