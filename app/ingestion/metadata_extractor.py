import re
from pathlib import Path


def extract_metadata(text: str, file_path: Path) -> dict:

    metadata = {
        "category": file_path.parent.name,
        "department": None,
        "effective_date": None,
        "access_classification": None,
        "allowed_roles": [],
        "allowed_users": [],
        "allowed_groups": [],
    }

    department_match = re.search(
        r"Policy Owner:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if department_match:
        metadata["department"] = (
            department_match.group(1).strip()
        )

    date_match = re.search(
        r"Effective Date:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if date_match:
        metadata["effective_date"] = (
            date_match.group(1).strip()
        )

    classification_match = re.search(
        r"Access Classification:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if classification_match:
        metadata["access_classification"] = (
            classification_match.group(1).strip()
        )

    roles_match = re.search(
        r"Allowed Roles:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if roles_match:
        metadata["allowed_roles"] = [
            role.strip()
            for role in roles_match.group(1).split(",")
            if role.strip()
        ]

    users_match = re.search(
        r"Allowed Users:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if users_match:
        metadata["allowed_users"] = [
            user.strip()
            for user in users_match.group(1).split(",")
            if user.strip()
        ]

    groups_match = re.search(
        r"Allowed Groups:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if groups_match:
        metadata["allowed_groups"] = [
            group.strip()
            for group in groups_match.group(1).split(",")
            if group.strip()
        ]

    return metadata