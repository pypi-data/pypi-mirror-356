"""
Rate management functions for Alignerr tools.

This module provides functions to query, set, and manage project rates
within the Labelbox platform, including support for both worker pay
rates and customer billing rates.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import labelbox as lb

from .enums import BillingMode, RateType
from .models import ValidationMixin


def _format_datetime(dt: datetime) -> str:
    """
    Format datetime to ISO string with Z suffix for GraphQL.

    Args:
        dt: datetime object (should be in UTC)

    Returns:
        str: ISO formatted string with Z suffix (e.g., "2024-01-15T10:30:00Z")
    """
    # If datetime is naive, assume UTC. If aware, convert to UTC.
    if dt.tzinfo is None:
        # Naive datetime - assume UTC
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        # Aware datetime - convert to UTC and format
        utc_dt = dt.utctimetuple()
        return datetime(*utc_dt[:6]).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_project_rates(client: lb.Client, project_id: str) -> Any:
    """
    Retrieve project rates for both production and evaluation projects.

    Args:
        client: The Labelbox client instance
        project_id: The project ID to query rates for

    Returns:
        dict: Project rates data including production and evaluation project rates

    Raises:
        ValueError: If project_id is not a valid 25-character ID
        Exception: If the GraphQL query fails

    Example:
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> rates = get_project_rates(client, "cm1pk2jhg0avt07z9h3b9fy9p")
        >>> print(rates)
    """
    # Validate project ID
    validated_project_id = ValidationMixin.validate_project_id(project_id)

    query = """query GetProjectRatesV2AlnrPyApi($projectId: ID!) {
      project(where: { id: $projectId }) {
        id
        name
        labelingFrontend { name }
        evaluationProject {
          id
          name
          ratesV2 {
            id
            userRole { id name }
            isBillRate
            billingMode
            rate
            effectiveSince
            effectiveUntil
          }
        }
        ratesV2 {
          id
          userRole { id name }
          isBillRate
          billingMode
          rate
          effectiveSince
          effectiveUntil
        }
      }
    }"""

    params = {"projectId": validated_project_id}

    return client.execute(query, params=params, experimental=True)


def set_project_rate(
    client: lb.Client,
    project_id: str,
    rate: float,
    rate_type: RateType,
    effective_from: Optional[datetime] = None,
    user_role_id: Optional[str] = None,
    billing_mode: BillingMode = BillingMode.ByHour,
    effective_until: Optional[datetime] = None,
) -> Any:
    """
    Set project rates using the SetProjectRateV2 mutation.

    Args:
        client: The Labelbox client instance
        project_id: The project ID to set rates for
        rate: The rate amount (maximum $1000)
        rate_type: Type of rate (WORKER_PAY or CUSTOMER_BILL)
        effective_from: Optional start date for the rate (UTC datetime)
        user_role_id: Required for WORKER_PAY rates, must be null for CUSTOMER_BILL
        billing_mode: Billing mode (defaults to BY_HOUR)
        effective_until: Optional end date for the rate (UTC datetime)

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If project_id or user_role_id are not valid 25-character IDs
        ValueError: If rate exceeds $1000 limit
        ValueError: If WORKER_PAY rate is missing user_role_id
        ValueError: If CUSTOMER_BILL rate includes user_role_id
        Exception: If the GraphQL mutation fails

    Example:
        >>> from datetime import datetime
        >>> client = labelbox.Client(api_key="your_api_key")
        >>> start_date = datetime(2024, 1, 15, 10, 30, 0)  # UTC
        >>> result = set_project_rate(
        ...     client,
        ...     "cm1pk2jhg0avt07z9h3b9fy9p",
        ...     rate=25.0,
        ...     rate_type=RateType.WorkerPay,
        ...     effective_from=start_date,
        ...     user_role_id="cjlvi914y1aa20714372uvzjv"
        ... )
    """
    # Validate project ID
    validated_project_id = ValidationMixin.validate_project_id(project_id)

    # Validate rate
    if not isinstance(rate, (int, float)) or rate <= 0 or rate > 1000:
        raise ValueError("Rate cannot exceed $1000")

    # Validate rate type and user_role_id requirements
    is_bill_rate = rate_type == RateType.CustomerBill

    if not is_bill_rate and not user_role_id:
        raise ValueError("user_role_id is required for worker pay rates")

    if is_bill_rate and user_role_id:
        raise ValueError("user_role_id must be null for customer bill rates")

    # Validate user_role_id if provided
    validated_user_role_id = None
    if user_role_id:
        validated_user_role_id = ValidationMixin.validate_user_id(
            user_role_id
        )  # Reusing user validation for role IDs

    mutation = """mutation SetProjectRateV2AlnrPyApi($input: SetProjectRateV2Input!) {
      setProjectRateV2(input: $input) {
        success
      }
    }"""

    input_data = {
        "projectId": validated_project_id,
        "isBillRate": is_bill_rate,
        "billingMode": billing_mode.value,
        "rate": float(rate),
    }

    if effective_from:
        input_data["effectiveSince"] = _format_datetime(effective_from)

    if validated_user_role_id:
        input_data["userRoleId"] = validated_user_role_id

    if effective_until:
        input_data["effectiveUntil"] = _format_datetime(effective_until)

    params = {"input": input_data}

    return client.execute(mutation, params=params, experimental=True)


def get_available_user_roles(client: lb.Client) -> Any:
    """
    Get available user roles for rate setting.

    Args:
        client: Labelbox client instance

    Returns:
        dict: Response with available user roles

    Raises:
        Exception: If the query fails

    Example:
        roles = get_available_user_roles(client)
        for role in roles["data"]["roles"]:
            print(f"Role: {role['name']} (ID: {role['id']})")
    """
    query = """query GetAvailableUserRolesAlnrPyApi {
      roles {
        id
        name
      }
    }"""

    return client.execute(query, experimental=True)


def set_project_alignerr_rate(
    client: lb.Client,
    project_id: str,
    user_id: str,
    rate: float,
    effective_from: Optional[datetime] = None,
    effective_until: Optional[datetime] = None,
) -> Any:
    """
    Set an individual Alignerr rate for a specific user.

    Args:
        client: Labelbox client instance
        project_id: ID of the project (25-character string)
        user_id: ID of the user (25-character string)
        rate: Rate amount
        effective_from: Start date (UTC datetime, optional)
        effective_until: End date (UTC datetime, optional)

    Returns:
        dict: Response from the GraphQL mutation

    Raises:
        ValueError: If project_id or user_id are not valid 25-character IDs
        ValueError: If rate is invalid
        Exception: If the mutation fails

    Example:
        >>> from datetime import datetime
        >>> start_date = datetime(2024, 1, 15, 0, 0, 0)  # UTC
        >>> set_project_alignerr_rate(
        ...     client,
        ...     "cm1pk2jhg0avt07z9h3b9fy9p",
        ...     "cjlvi914y1aa20714372uvzjv",
        ...     rate=30.0,
        ...     effective_from=start_date
        ... )
    """
    # Validate IDs
    validated_project_id = ValidationMixin.validate_project_id(project_id)
    validated_user_id = ValidationMixin.validate_user_id(user_id)

    # Validate rate
    if not isinstance(rate, (int, float)) or rate <= 0:
        raise ValueError("Rate must be a positive number")

    mutation = """mutation SetProjectAlignerrRateAlnrPyApi(
        $input: SetProjectAlignerrRateInput!
    ) {
      setProjectAlignerrRate(input: $input) {
        success
      }
    }"""

    input_data = {
        "projectId": validated_project_id,
        "userId": validated_user_id,
        "rate": float(rate),
    }

    if effective_from:
        input_data["effectiveSince"] = _format_datetime(effective_from)

    if effective_until:
        input_data["effectiveUntil"] = _format_datetime(effective_until)

    params = {"input": input_data}

    return client.execute(mutation, params=params, experimental=True)


def bulk_set_project_alignerr_rates(
    client: lb.Client,
    project_id: str,
    user_rates: List[Dict[str, Any]],
    effective_from: Optional[datetime] = None,
    effective_until: Optional[datetime] = None,
) -> List[Dict[str, Any]]:
    """
    Set Alignerr rates for multiple users in bulk.

    Args:
        client: Labelbox client instance
        project_id: ID of the project (25-character string)
        user_rates: List of dicts with 'userId' and 'rate' keys
        effective_from: Start date (UTC datetime, optional)
        effective_until: End date (UTC datetime, optional)

    Returns:
        list: List of responses from individual rate settings

    Raises:
        ValueError: If project_id or user IDs are not valid 25-character IDs
        ValueError: If user_rates is empty or has invalid structure
        Exception: If any mutation fails

    Example:
        >>> from datetime import datetime
        >>> start_date = datetime(2024, 1, 15, 0, 0, 0)  # UTC
        >>> user_rates = [
        ...     {"userId": "cjlvi914y1aa20714372uvzjv", "rate": 25.0},
        ...     {"userId": "cjlvi919b1aa50714k75euii5", "rate": 30.0}
        ... ]
        >>> bulk_set_project_alignerr_rates(
        ...     client,
        ...     "cm1pk2jhg0avt07z9h3b9fy9p",
        ...     user_rates,
        ...     effective_from=start_date
        ... )
    """
    # Validate project ID first
    validated_project_id = ValidationMixin.validate_project_id(project_id)

    if not user_rates:
        raise ValueError("user_rates cannot be empty")

    results = []
    for user_rate in user_rates:
        if not isinstance(user_rate, dict):
            raise ValueError("Each user_rate must be a dictionary")
        if "userId" not in user_rate or "rate" not in user_rate:
            raise ValueError("Each user_rate must contain 'userId' and 'rate' keys")

        user_id = user_rate["userId"]
        rate = user_rate["rate"]

        # Validate user ID
        validated_user_id = ValidationMixin.validate_user_id(user_id)

        if rate > 1000:
            raise ValueError(f"Rate for user {user_id} cannot exceed $1000")

        # Set the rate for this user
        result = set_project_alignerr_rate(
            client=client,
            project_id=validated_project_id,
            user_id=validated_user_id,
            rate=rate,
            effective_from=effective_from,
            effective_until=effective_until,
        )
        results.append(result)

    return results
