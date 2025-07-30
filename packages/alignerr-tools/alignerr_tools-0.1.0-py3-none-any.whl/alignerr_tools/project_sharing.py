"""
Project sharing functions for Alignerr tools.

This module provides functions to share projects with users and groups
within the Labelbox platform.
"""

from typing import Any, List

from .enums import Organization
from .models import ValidationMixin


def share_project_with_users(client: Any, project_id: str, user_ids: List[str]) -> Any:
    """
    Share a project with users within the Labelbox platform.

    Args:
        client: The Labelbox client instance
        project_id: The project ID to share
        user_ids: List of user IDs to share the project with

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If project_id is not a valid 25-character ID
        Exception: If the GraphQL mutation fails

    Example:
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> result = share_project_with_users(
        ...     client, "cm1pk2jhg0avt07z9h3b9fy9p", ["user1", "user2"]
        ... )
    """
    # Validate project ID
    validated_project_id = ValidationMixin.validate_project_id(project_id)

    mutation = """
    mutation ShareProjectAlnrPyApi($projectId: ID!, $userIds: [ID!]!) {
        shareProject(
            projectId: $projectId,
            userIds: $userIds
        ) {
            success
            message
        }
    }
    """

    variables = {
        "projectId": validated_project_id,
        "userIds": user_ids,
    }

    result = client.execute(mutation, variables, experimental=True)
    return result


def unshare_project_from_users(
    client: Any, project_id: str, user_ids: List[str]
) -> Any:
    """
    Unshare a project from specific users.

    Args:
        client: The Labelbox client instance
        project_id: The project ID to unshare
        user_ids: List of user IDs to unshare the project from

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If project_id is not a valid 25-character ID
        Exception: If the GraphQL mutation fails

    Example:
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> result = unshare_project_from_users(
        ...     client, "cm1pk2jhg0avt07z9h3b9fy9p", ["user1", "user2"]
        ... )
    """
    # Validate project ID
    validated_project_id = ValidationMixin.validate_project_id(project_id)

    mutation = """
    mutation UnshareProjectAlnrPyApi($projectId: ID!, $userIds: [ID!]!) {
        unshareProject(
            projectId: $projectId,
            userIds: $userIds
        ) {
            success
            message
        }
    }
    """

    variables = {
        "projectId": validated_project_id,
        "userIds": user_ids,
    }

    result = client.execute(mutation, variables, experimental=True)
    return result


def share_project_with_alignerr(client: Any, project_id: str) -> Any:
    """
    Share a project with the Alignerr organization.

    Args:
        client: The Labelbox client instance
        project_id: The project ID to share

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If project_id is not a valid 25-character ID
        Exception: If the GraphQL mutation fails

    Example:
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> result = share_project_with_alignerr(client, "cm1pk2jhg0avt07z9h3b9fy9p")
    """
    # Validate project ID
    validated_project_id = ValidationMixin.validate_project_id(project_id)

    mutation = """
    mutation AddExternalOrgToProjectAlnrPyApi(
        $projectId: ID!, $organizationId: ID!
    ) {
        shareProjectWithExternalOrganization(data: {
            projectId: $projectId,
            organizationId: $organizationId
        }) {
            id
            sharedWithOrganizations {
                id
                name
            }
        }
    }
    """

    variables = {
        "projectId": validated_project_id,
        "organizationId": Organization.Alignerr,
    }

    result = client.execute(mutation, variables, experimental=True)
    return result


def unshare_project_from_alignerr(client: Any, project_id: str) -> Any:
    """
    Unshare a project from the Alignerr organization.

    Args:
        client: The Labelbox client instance
        project_id: The project ID to unshare

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If project_id is not a valid 25-character ID
        Exception: If the GraphQL mutation fails

    Example:
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> result = unshare_project_from_alignerr(client, "cm1pk2jhg0avt07z9h3b9fy9p")
    """
    # Validate project ID
    validated_project_id = ValidationMixin.validate_project_id(project_id)

    mutation = """
    mutation RemoveExternalOrgFromProjectAlnrPyApi(
        $projectId: ID!, $organizationId: ID!
    ) {
        unshareProjectWithExternalOrganization(data: {
            projectId: $projectId,
            organizationId: $organizationId
        }) {
            id
            sharedWithOrganizations {
                id
                name
            }
        }
    }
    """

    variables = {
        "projectId": validated_project_id,
        "organizationId": Organization.Alignerr,
    }

    result = client.execute(mutation, variables, experimental=True)
    return result
