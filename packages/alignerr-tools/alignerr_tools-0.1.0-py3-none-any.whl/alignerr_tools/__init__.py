"""
Alignerr Tools - Labelbox project automation utilities.

This package provides utilities for working with Labelbox projects,
including project promotion, group management, project sharing, and rates querying.

Usage:
    from alignerr_tools import promotion, rates

    promotion.promote_all_users_to_production(client, project_id)
    promotion.promote_user_to_production(client, project_id, user_ids)
    promotion.promote_project_to_production(client, project_id)
    promotion.promote_project_to_status(client, project_id, status)
    rates.get_project_rates(client, project_id)
"""

__version__ = "0.1.0"
__author__ = "Labelbox Alignerr Team"
__email__ = "support@labelbox.com"

from .enums import (
    AlignerrEvaluationStatus,
    AlignerrStatus,
    BillingMode,
    Organization,
    ProjectStatus,
    RateType,
)
from .group_management import add_users_to_groups, remove_users_from_group
from .models import ValidationMixin
from .project_sharing import (
    share_project_with_alignerr,
    share_project_with_users,
    unshare_project_from_alignerr,
    unshare_project_from_users,
)

# Import modules for organized access
from .promotion import (
    get_alignerr_project_statuses,
    promote_all_users_to_production,
    promote_project_to_production,
    promote_project_to_status,
    promote_user_to_production,
)
from .rates import (
    bulk_set_project_alignerr_rates,
    get_available_user_roles,
    get_project_rates,
    set_project_alignerr_rate,
    set_project_rate,
)

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "promote_all_users_to_production",
    "promote_user_to_production",
    "promote_project_to_production",
    "promote_project_to_status",
    "get_alignerr_project_statuses",
    "add_users_to_groups",
    "remove_users_from_group",
    "share_project_with_users",
    "unshare_project_from_users",
    "share_project_with_alignerr",
    "unshare_project_from_alignerr",
    "get_project_rates",
    "set_project_rate",
    "get_available_user_roles",
    "set_project_alignerr_rate",
    "bulk_set_project_alignerr_rates",
    "ValidationMixin",
    "ProjectStatus",
    "AlignerrStatus",
    "AlignerrEvaluationStatus",
    "Organization",
    "BillingMode",
    "RateType",
]
