from app.models.chunk import DocumentChunk
from app.models.user import User


def can_access_document(
    user: User,
    chunk: DocumentChunk
) -> bool:

    # Explicit user permission
    if user.user_id in chunk.allowed_users:
        return True

    # Role-based permission
    if set(user.roles).intersection(chunk.allowed_roles):
        return True

    # Group-based permission
    if set(user.groups).intersection(chunk.allowed_groups):
        return True

    return False