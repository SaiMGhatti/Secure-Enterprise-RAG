from app.models.user import User

# LOCAL DEVELOPMENT ONLY. Identity is resolved server-side from the bearer token,
# so a caller can never choose their own departments or roles.
# Associate = employee; Manager = employee + manager.
_ASSOCIATE_ROLES = ["employee"]
_MANAGER_ROLES = ["employee", "manager"]

DEV_USERS: dict[str, User] = {
    f"dev-{dept.lower()}-{level}": User(
        user_id=f"{dept.lower()}_{level}",
        departments=[dept],
        roles=roles,
    )
    for dept in ("HR", "IT", "Finance", "Legal")
    for level, roles in (("associate", _ASSOCIATE_ROLES), ("manager", _MANAGER_ROLES))
}


def resolve_user(token: str | None) -> User | None:
    if not token:
        return None
    return DEV_USERS.get(token)
