from app.authorization.policy import can_access_document
from app.models.chunk import DocumentChunk
from app.models.user import User


def test_employee_can_access_hr_document():

    user = User(
        user_id="user-001",
        roles=["employee"],
        groups=["US_EMPLOYEES"],
    )

    chunk = DocumentChunk(
        chunk_id="chunk-001",
        document_id="HR-001",
        text="Employees receive 15 vacation days.",
        category="HR",
        department="HR",
        allowed_roles=["employee", "manager"],
    )

    assert can_access_document(user, chunk)


def test_employee_cannot_access_finance_document():

    user = User(
        user_id="user-001",
        roles=["employee"],
        groups=["US_EMPLOYEES"],
    )

    chunk = DocumentChunk(
        chunk_id="chunk-002",
        document_id="FIN-001",
        text="Executive compensation information.",
        category="Finance",
        department="Finance",
        allowed_roles=["finance_manager", "executive"],
    )

    assert not can_access_document(user, chunk)