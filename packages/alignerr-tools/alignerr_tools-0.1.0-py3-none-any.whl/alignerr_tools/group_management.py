"""
Group management functions for Alignerr tools.

This module provides functions to add and remove users from groups
within the Labelbox platform.
"""

from typing import Any, Dict, List

from .models import ValidationMixin


def add_users_to_groups(
    client: Any,
    group_ids: List[str],
    user_roles: List[Dict[str, Any]],
) -> Any:
    """
    Add users to groups with specific roles.

    This function allows you to add multiple users to multiple groups with
    specific roles. Each user can have a different role in each group.

    Args:
        client: The Labelbox client instance
        group_ids: List of group IDs to add users to
        user_roles: List of dictionaries containing user and role information
                   Each dictionary should have:
                   - userId: The user ID
                   - roleId: The role ID for the user

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If group_ids is empty or if validation fails
        Exception: If the GraphQL mutation fails

    Example:
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> group_ids = ["group1", "group2"]
        >>> user_roles = [
        ...     {"userId": "user1", "roleId": "role1"},
        ...     {"userId": "user2", "roleId": "role2"}
        ... ]
        >>> result = add_users_to_groups(client, group_ids, user_roles)l
    """
    if not group_ids:
        raise ValueError("group_ids cannot be empty")

    if not user_roles:
        raise ValueError("user_roles cannot be empty")

    # Validate IDs using simple validation functions
    validated_group_ids = ValidationMixin.validate_group_ids(group_ids)
    validated_user_roles = ValidationMixin.validate_user_roles(user_roles)

    # Create the mutation
    mutation = """
    mutation AddUsersToGroupsAlnrPyApi(
        $groupIds: [ID!]!, $userRoles: [UserRoleInput!]!
    ) {
        addUsersToGroups(
            groupIds: $groupIds,
            userRoles: $userRoles
        ) {
            success
            message
        }
    }
    """

    variables = {
        "groupIds": validated_group_ids,
        "userRoles": validated_user_roles,
    }

    result = client.execute(mutation, variables, experimental=True)
    return result


def remove_users_from_group(
    client: Any,
    group_id: str,
    user_ids: List[str],
) -> Any:
    """
    Remove users from a specific group.

    This function removes multiple users from a single group.

    Args:
        client: The Labelbox client instance
        group_id: The ID of the group to remove users from
        user_ids: List of user IDs to remove from the group

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If group_id is empty or if validation fails
        Exception: If the GraphQL mutation fails

    Example:
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> group_id = "group123"
        >>> user_ids = ["user1", "user2", "user3"]
        >>> result = remove_users_from_group(client, group_id, user_ids)
    """
    if not group_id:
        raise ValueError("group_id cannot be empty")

    if not user_ids:
        raise ValueError("user_ids cannot be empty")

    # Validate IDs using simple validation functions
    validated_group_id = ValidationMixin.validate_group_id(group_id)
    validated_user_ids = ValidationMixin.validate_user_ids(user_ids)

    # Create the mutation
    mutation = """
    mutation RemoveUsersFromGroupAlnrPyApi($groupId: ID!, $userIds: [ID!]!) {
        removeUsersFromGroup(
            groupId: $groupId,
            userIds: $userIds
        ) {
            success
            message
        }
    }
    """

    variables = {
        "groupId": validated_group_id,
        "userIds": validated_user_ids,
    }

    result = client.execute(mutation, variables, experimental=True)
    return result
