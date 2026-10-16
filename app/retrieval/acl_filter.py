from app.models.user import User


def build_acl_filter(user: User) -> dict:
    permissions = []

    if user.user_id:
        permissions.append({"term": {"allowed_users": user.user_id}})

    if user.roles:
        permissions.append({"terms": {"allowed_roles": user.roles}})

    if user.groups:
        permissions.append({"terms": {"allowed_groups": user.groups}})

    # Fail closed: no department or no grants means no results
    if not user.departments or not permissions:
        return {"match_none": {}}

    return {
        "bool": {
            "filter": [
                {"terms": {"category": user.departments}},
                {
                    "bool": {
                        "should": permissions,
                        "minimum_should_match": 1,
                    }
                },
            ]
        }
    }
