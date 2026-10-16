from app.authorization.policy import can_access_document
from app.models.chunk import DocumentChunk
from app.models.user import User
from app.retrieval.acl_filter import build_acl_filter


def make_chunk(category: str, roles: list[str]) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=f"{category}-1",
        document_id=f"{category}-doc",
        text="sample",
        category=category,
        chunk_index=0,
        version=1,
        content_hash="hash",
        allowed_roles=roles,
    )


def test_same_role_in_other_department_is_denied():
    user = User(user_id="u1", departments=["HR"], roles=["manager"])
    finance_chunk = make_chunk("Finance", ["manager"])

    assert not can_access_document(user, finance_chunk)


def test_matching_department_and_role_is_allowed():
    user = User(user_id="u1", departments=["Finance"], roles=["manager"])

    assert can_access_document(user, make_chunk("Finance", ["manager"]))


def test_matching_department_without_role_is_denied():
    user = User(user_id="u1", departments=["Finance"], roles=["employee"])

    assert not can_access_document(user, make_chunk("Finance", ["manager"]))


def test_user_without_departments_is_denied():
    user = User(user_id="u1", roles=["employee"])

    assert not can_access_document(user, make_chunk("HR", ["employee"]))


def test_filter_requires_department_and_grant():
    user = User(user_id="u1", departments=["HR"], roles=["employee"])

    acl = build_acl_filter(user)

    must = acl["bool"]["filter"]
    assert {"terms": {"category": ["HR"]}} in must
    assert any("should" in clause.get("bool", {}) for clause in must)


def test_filter_fails_closed_without_departments():
    user = User(user_id="u1", roles=["employee"])

    assert build_acl_filter(user) == {"match_none": {}}
