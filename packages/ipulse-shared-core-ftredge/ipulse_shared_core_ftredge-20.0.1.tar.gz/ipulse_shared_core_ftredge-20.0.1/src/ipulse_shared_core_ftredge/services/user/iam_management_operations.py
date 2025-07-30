"""
IAM Management Operations - Handle user permissions and access rights
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from ...models.user_status import IAMUnitRefAssignment
from ipulse_shared_base_ftredge.enums.enums_status import ApprovalStatus
from ipulse_shared_base_ftredge.enums.enums_iam import IAMUnitType
from ...exceptions import IAMPermissionError, UserAuthError


class IAMManagementOperations:
    """
    Handles IAM permissions and access rights management
    """

    def __init__(
        self,
        user_account_ops,  # UserManagementOperations instance
        logger: Optional[logging.Logger] = None
    ):
        self.user_account_ops = user_account_ops
        self.logger = logger or logging.getLogger(__name__)

    # IAM Permission Operations

    async def add_user_permission(
        self,
        user_uid: str,
        domain: str,
        permission_name: str,
        iam_unit_type: IAMUnitType,
        source: str,
        expires_at: Optional[datetime] = None,
        updater_uid: Optional[str] = None
    ) -> bool:
        """Add an IAM permission to a user"""
        try:
            user_status = await self.user_account_ops.get_userstatus(user_uid)
            if not user_status:
                raise IAMPermissionError(
                    detail="User status not found",
                    user_uid=user_uid,
                    domain=domain,
                    permission=permission_name,
                    operation="add_user_permission"
                )

            user_status.add_iam_unit_ref_assignment(
                domain=domain,
                iam_unit_ref=permission_name,
                iam_unit_type=iam_unit_type,
                source=source,
                expires_at=expires_at
            )

            user_status.updated_at = datetime.now(timezone.utc)
            user_status.updated_by = updater_uid or f"IAMManagement.add_permission:{source}"

            await self.user_account_ops.update_userstatus(
                user_uid=user_uid,
                status_data=user_status.model_dump(exclude_none=True),
                updater_uid=updater_uid or f"IAMManagement:{source}"
            )

            self.logger.info(f"Added {iam_unit_type.value} permission '{permission_name}' to user {user_uid} in domain '{domain}'")
            return True

        except Exception as e:
            self.logger.error(f"Error adding permission to user {user_uid}: {e}", exc_info=True)
            raise IAMPermissionError(
                detail=f"Failed to add permission: {str(e)}",
                user_uid=user_uid,
                domain=domain,
                permission=permission_name,
                operation="add_user_permission",
                original_error=e
            )

    async def remove_user_permission(
        self,
        user_uid: str,
        domain: str,
        permission_name: str,
        iam_unit_type: IAMUnitType,
        updater_uid: Optional[str] = None
    ) -> bool:
        """Remove an IAM permission from a user"""
        try:
            user_status = await self.user_account_ops.get_userstatus(user_uid)
            if not user_status:
                raise IAMPermissionError(
                    detail="User status not found",
                    user_uid=user_uid,
                    domain=domain,
                    permission=permission_name,
                    operation="remove_user_permission"
                )

            # Check if permission exists
            if (domain not in user_status.iam_domain_permissions or
                iam_unit_type.value not in user_status.iam_domain_permissions[domain] or
                permission_name not in user_status.iam_domain_permissions[domain][iam_unit_type.value]):
                self.logger.warning(f"Permission '{permission_name}' not found for user {user_uid} in domain '{domain}'")
                return False

            # Remove the permission
            del user_status.iam_domain_permissions[domain][iam_unit_type.value][permission_name]

            # Clean up empty structures
            if not user_status.iam_domain_permissions[domain][iam_unit_type.value]:
                del user_status.iam_domain_permissions[domain][iam_unit_type.value]
            if not user_status.iam_domain_permissions[domain]:
                del user_status.iam_domain_permissions[domain]

            user_status.updated_at = datetime.now(timezone.utc)
            user_status.updated_by = updater_uid or "IAMManagement.remove_permission"

            await self.user_account_ops.update_userstatus(
                user_uid=user_uid,
                status_data=user_status.model_dump(exclude_none=True),
                updater_uid=updater_uid or "IAMManagement"
            )

            self.logger.info(f"Removed {iam_unit_type.value} permission '{permission_name}' from user {user_uid} in domain '{domain}'")
            return True

        except Exception as e:
            self.logger.error(f"Error removing permission from user {user_uid}: {e}", exc_info=True)
            raise IAMPermissionError(
                detail=f"Failed to remove permission: {str(e)}",
                user_uid=user_uid,
                domain=domain,
                permission=permission_name,
                operation="remove_user_permission",
                original_error=e
            )

    async def get_user_permissions(
        self,
        user_uid: str,
        domain: Optional[str] = None,
        iam_unit_type: Optional[IAMUnitType] = None,
        include_expired: bool = False
    ) -> Dict[str, Dict[str, Dict[str, IAMUnitRefAssignment]]]:
        """Get user's IAM permissions with optional filtering"""
        try:
            user_status = await self.user_account_ops.get_userstatus(user_uid)
            if not user_status:
                return {}

            permissions = user_status.iam_domain_permissions

            # Filter by domain if specified
            if domain:
                permissions = {domain: permissions.get(domain, {})}

            # Filter by IAM unit type if specified
            if iam_unit_type:
                filtered_permissions = {}
                for dom, domain_perms in permissions.items():
                    if iam_unit_type.value in domain_perms:
                        filtered_permissions[dom] = {iam_unit_type.value: domain_perms[iam_unit_type.value]}
                permissions = filtered_permissions

            # Filter expired permissions if requested
            if not include_expired:
                filtered_permissions = {}
                for dom, domain_perms in permissions.items():
                    filtered_domain = {}
                    for unit_type, unit_perms in domain_perms.items():
                        filtered_unit = {
                            perm_name: assignment
                            for perm_name, assignment in unit_perms.items()
                            if assignment.is_valid()
                        }
                        if filtered_unit:
                            filtered_domain[unit_type] = filtered_unit
                    if filtered_domain:
                        filtered_permissions[dom] = filtered_domain
                permissions = filtered_permissions

            return permissions

        except Exception as e:
            self.logger.error(f"Error getting permissions for user {user_uid}: {e}", exc_info=True)
            raise IAMPermissionError(
                detail=f"Failed to get user permissions: {str(e)}",
                user_uid=user_uid,
                domain=domain,
                operation="get_user_permissions",
                original_error=e
            )

    async def has_user_permission(
        self,
        user_uid: str,
        domain: str,
        permission_name: str,
        iam_unit_type: IAMUnitType = IAMUnitType.GROUPS
    ) -> bool:
        """Check if user has a specific permission"""
        try:
            permissions = await self.get_user_permissions(
                user_uid=user_uid,
                domain=domain,
                iam_unit_type=iam_unit_type,
                include_expired=False
            )

            return (domain in permissions and
                    iam_unit_type.value in permissions[domain] and
                    permission_name in permissions[domain][iam_unit_type.value])

        except Exception as e:
            self.logger.error(f"Error checking permission for user {user_uid}: {e}", exc_info=True)
            return False

    async def cleanup_expired_permissions(self, user_uid: str, updater_uid: Optional[str] = None) -> int:
        """Remove all expired permissions for a user"""
        try:
            user_status = await self.user_account_ops.get_userstatus(user_uid)
            if not user_status:
                return 0

            removed_count = user_status.remove_expired_iam_unit_refs()

            if removed_count > 0:
                user_status.updated_at = datetime.now(timezone.utc)
                user_status.updated_by = updater_uid or "IAMManagement.cleanup_expired"

                await self.user_account_ops.update_userstatus(
                    user_uid=user_uid,
                    status_data=user_status.model_dump(exclude_none=True),
                    updater_uid=updater_uid or "IAMManagement"
                )

                self.logger.info(f"Cleaned up {removed_count} expired permissions for user {user_uid}")

            return removed_count

        except Exception as e:
            self.logger.error(f"Error cleaning up expired permissions for user {user_uid}: {e}", exc_info=True)
            raise IAMPermissionError(
                detail=f"Failed to cleanup expired permissions: {str(e)}",
                user_uid=user_uid,
                operation="cleanup_expired_permissions",
                original_error=e
            )

    # Legacy group methods for backward compatibility

    async def add_user_group(
        self,
        user_uid: str,
        domain: str,
        group_name: str,
        source: str,
        expires_at: Optional[datetime] = None,
        updater_uid: Optional[str] = None
    ) -> bool:
        """Add a group to a user (legacy method)"""
        return await self.add_user_permission(
            user_uid=user_uid,
            domain=domain,
            permission_name=group_name,
            iam_unit_type=IAMUnitType.GROUPS,
            source=source,
            expires_at=expires_at,
            updater_uid=updater_uid
        )

    async def remove_user_group(
        self,
        user_uid: str,
        domain: str,
        group_name: str,
        updater_uid: Optional[str] = None
    ) -> bool:
        """Remove a group from a user (legacy method)"""
        return await self.remove_user_permission(
            user_uid=user_uid,
            domain=domain,
            permission_name=group_name,
            iam_unit_type=IAMUnitType.GROUPS,
            updater_uid=updater_uid
        )

    async def get_user_groups(
        self,
        user_uid: str,
        domain: Optional[str] = None,
        include_expired: bool = False
    ) -> Dict[str, Dict[str, IAMUnitRefAssignment]]:
        """Get user's groups (legacy method)"""
        permissions = await self.get_user_permissions(
            user_uid=user_uid,
            domain=domain,
            iam_unit_type=IAMUnitType.GROUPS,
            include_expired=include_expired
        )

        # Flatten to match legacy format
        groups = {}
        for domain_name, domain_perms in permissions.items():
            if IAMUnitType.GROUPS.value in domain_perms:
                groups[domain_name] = domain_perms[IAMUnitType.GROUPS.value]

        return groups

    async def has_user_group(
        self,
        user_uid: str,
        domain: str,
        group_name: str
    ) -> bool:
        """Check if user has a specific group (legacy method)"""
        return await self.has_user_permission(
            user_uid=user_uid,
            domain=domain,
            permission_name=group_name,
            iam_unit_type=IAMUnitType.GROUPS
        )


