"""
Simple validation functions for Labelbox IDs and data structures.

This module provides basic validation for Labelbox IDs and other data structures
used throughout the alignerr-tools package.
"""

import re
from typing import Any, Dict, List


def validate_labelbox_id(id_str: str, id_type: str = "ID") -> str:
    """
    Validate a Labelbox ID is exactly 25 alphanumeric characters.

    Args:
        id_str: The ID string to validate
        id_type: Description of the ID type for error messages

    Returns:
        str: The validated ID string

    Raises:
        ValueError: If the ID is invalid
    """
    if not isinstance(id_str, str):
        raise ValueError(f"{id_type} must be a string")
    if len(id_str) != 25:
        raise ValueError(f"{id_type} must be exactly 25 characters long")
    if not id_str.isalnum():
        raise ValueError(f"{id_type} must contain only alphanumeric characters")
    return id_str


def validate_group_id(group_id: str) -> str:
    """
    Validate a group ID is a valid UUID format (36 characters with hyphens).

    Args:
        group_id: The group ID string to validate

    Returns:
        str: The validated group ID string

    Raises:
        ValueError: If the group ID is invalid
    """
    if not isinstance(group_id, str):
        raise ValueError("Group ID must be a string")
    if len(group_id) != 36:
        raise ValueError("Group ID must be exactly 36 characters long")

    # UUID format: 8-4-4-4-12 (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    uuid_pattern = (
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    )
    if not re.match(uuid_pattern, group_id):
        raise ValueError(
            "Group ID must be a valid UUID format "
            "(xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"
        )

    return group_id


def validate_user_role(user_role: Dict[str, Any]) -> Any:
    """
    Validate a user role dictionary structure.

    Args:
        user_role: Dictionary with 'userId' and 'roleId' keys

    Returns:
        dict: The validated user role dictionary

    Raises:
        ValueError: If the user role structure is invalid
    """
    if not isinstance(user_role, dict):
        raise ValueError("User role must be a dictionary")
    if "userId" not in user_role or "roleId" not in user_role:
        raise ValueError("User role must contain 'userId' and 'roleId' keys")

    # Validate the IDs
    validated_role = {
        "userId": validate_labelbox_id(user_role["userId"], "User ID"),
        "roleId": validate_labelbox_id(user_role["roleId"], "Role ID"),
    }

    return validated_role


class ValidationMixin:
    """Helper class providing validation methods."""

    @staticmethod
    def validate_project_id(project_id: str) -> str:
        """Validate and return a project ID."""
        return validate_labelbox_id(project_id, "Project ID")

    @staticmethod
    def validate_user_id(user_id: str) -> str:
        """Validate and return a user ID."""
        return validate_labelbox_id(user_id, "User ID")

    @staticmethod
    def validate_group_id(group_id: str) -> str:
        """Validate and return a group ID."""
        return validate_group_id(group_id)

    @staticmethod
    def validate_user_ids(user_ids: List[str]) -> List[str]:
        """Validate and return a list of user IDs."""
        return [ValidationMixin.validate_user_id(uid) for uid in user_ids]

    @staticmethod
    def validate_group_ids(group_ids: List[str]) -> List[str]:
        """Validate and return a list of group IDs."""
        return [ValidationMixin.validate_group_id(gid) for gid in group_ids]

    @staticmethod
    def validate_user_roles(user_roles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and return a list of user role dictionaries."""
        validated_roles = []
        for role in user_roles:
            validated_role = validate_user_role(role)
            validated_roles.append(validated_role)
        return validated_roles
