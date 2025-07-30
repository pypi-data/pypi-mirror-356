"""
Enhanced UserCoreService - Comprehensive user management orchestration

This service orchestrates all user-related operations by composing specialized
operation classes for different concerns:
- Firebase Auth User Management
- User Account Management (UserProfile and UserStatus CRUD operations)
- User Deletion Operations
- Subscription Management
- IAM Management
- Default Values by UserType

Can be used by Firebase Cloud Functions, Core microservice APIs, admin tools, and tests.
"""
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
from google.cloud import firestore
from pydantic import BaseModel

from ...models.user_profile import UserProfile
from ...models.user_status import UserStatus, IAMUnitRefAssignment
from ...models.user_auth import UserAuth
from ...models.subscription import Subscription
from ...exceptions import ServiceError, ResourceNotFoundError, UserCreationError
from ..base import BaseFirestoreService
from ipulse_shared_base_ftredge.enums.enums_iam import IAMUnitType

# Import specialized operation classes
from .user_account_operations import UserAccountOperations
from .subscription_management_operations import SubscriptionManagementOperations, SubscriptionPlanDocument
from .iam_management_operations import IAMManagementOperations
from .user_auth_operations import UserAuthOperations
from .user_holistic_operations import UserHolisticOperations


# Model for user type defaults from Firestore
class UserTypeDefaultsDocument(BaseModel):
    """Model for user type defaults documents stored in Firestore"""
    id: str
    default_iam_domain_permissions: Optional[Dict[str, Dict[str, Dict[str, IAMUnitRefAssignment]]]] = None
    default_subscription_based_insight_credits: Optional[int] = None
    default_extra_insight_credits: Optional[int] = None
    default_voting_credits: Optional[int] = None
    default_subscription_plan_if_unpaid: Optional[str] = None
    default_secondary_usertypes: Optional[List[str]] = None
    default_organizations_uids: Optional[List[str]] = None
    default_subscription_plan_id: Optional[str] = None


class UserCoreService:
    """
    Enhanced UserCoreService - Orchestrates all user-related operations

    This service provides a unified interface for all user management operations
    by composing specialized operation classes. It maintains backward compatibility
    while providing enhanced functionality and better organization.
    """

    def __init__(
        self,
        firestore_client: firestore.Client,
        logger: Optional[logging.Logger] = None,
        default_timeout: float = 10.0,
        profile_collection: Optional[str] = None,
        status_collection: Optional[str] = None,
        subscriptionplans_defaults_collection: str = "papp_core_configs_subscriptionplans_defaults",
        users_defaults_collection: str = "papp_core_configs_users_defaults"
    ):
        """
        Initialize the Enhanced UserCoreService

        Args:
            firestore_client: Initialized Firestore client
            logger: Optional logger instance
            default_timeout: Default timeout for Firestore operations
            profile_collection: Collection name for user profiles
            status_collection: Collection name for user statuses
            subscriptionplans_defaults_collection: Collection name for subscription plans
            users_defaults_collection: Collection name for user defaults
        """
        self.db = firestore_client
        self.logger = logger or logging.getLogger(__name__)
        self.timeout = default_timeout

        self.profile_collection_name = profile_collection or UserProfile.get_collection_name()
        self.status_collection_name = status_collection or UserStatus.get_collection_name()

        # Initialize specialized operation classes in dependency order
        self.user_auth_ops = UserAuthOperations(
            logger=self.logger
        )

        self.user_account_ops = UserAccountOperations(
            firestore_client=self.db,
            logger=self.logger,
            timeout=self.timeout,
            profile_collection=self.profile_collection_name,
            status_collection=self.status_collection_name
        )

        self.subscription_ops = SubscriptionManagementOperations(
            firestore_client=self.db,
            user_account_ops=self.user_account_ops,
            logger=self.logger,
            timeout=self.timeout,
            subscription_plans_collection=subscriptionplans_defaults_collection
        )

        self.iam_ops = IAMManagementOperations(
            user_account_ops=self.user_account_ops,
            logger=self.logger
        )

        # Initialize holistic operations last as it depends on other operations
        self.user_holistic_ops = UserHolisticOperations(
            user_account_ops=self.user_account_ops,
            user_auth_ops=self.user_auth_ops,
            subscription_ops=self.subscription_ops,
            iam_ops=self.iam_ops,
            logger=self.logger
        )

        # Initialize defaults values per usertype service
        self.usertype_defaults_collection_name = users_defaults_collection
        self._user_defaults_db_service = BaseFirestoreService[UserTypeDefaultsDocument](
            db=self.db,
            collection_name=self.usertype_defaults_collection_name,
            resource_type="UserTypeDefault",
            logger=self.logger,
            timeout=self.timeout
        )


    ######################################################################
    ######################### UserAuth Operation #########################





    def generate_firebase_custom_claims(
        self,
        primary_usertype: str,
        secondary_usertypes: Optional[List[str]] = None,
        organizations_uids: Optional[List[str]] = None,
        user_approval_status: str = "pending"
    ) -> Dict[str, Any]:
        """Generate Firebase custom claims for a user"""
        return self.user_auth_ops.generate_firebase_custom_claims(
            primary_usertype=primary_usertype,
            secondary_usertypes=secondary_usertypes,
            organizations_uids=organizations_uids,
            user_approval_status=user_approval_status
        )



    ################################################################################################
    ######################### Fetching Default User/Subscription Values   #########################

    async def fetch_user_defaults(self, usertype_name: str) -> Optional[Dict[str, Any]]:
        """Fetch user type defaults from Firestore"""
        try:
            user_defaults_data = await self._user_defaults_db_service.get_document(usertype_name)
            if user_defaults_data:
                self.logger.info(f"User defaults found for usertype: {usertype_name}")
                # Convert UserTypeDefaultsDocument to dict for backward compatibility
                if isinstance(user_defaults_data, UserTypeDefaultsDocument):
                    return user_defaults_data.model_dump()
                return user_defaults_data
            else:
                self.logger.warning(f"User defaults not found for usertype: {usertype_name}")
                return None
        except ResourceNotFoundError:
            self.logger.warning(f"User defaults not found for usertype: {usertype_name}")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching user defaults for {usertype_name}: {e}", exc_info=True)
            raise ServiceError(
                operation="fetch_user_defaults",
                resource_type="UserTypeDefault",
                resource_id=usertype_name,
                error=e
            )

    async def _fetch_subscription_plan_details(self, plan_id: str) -> Optional[SubscriptionPlanDocument]:
        """Fetch subscription plan details (backward compatibility)"""
        return await self.subscription_ops.fetch_subscription_plan_details(plan_id)

    ###############################################################################
    ############################## User Account Operation #########################

    async def get_userprofile(self, user_uid: str) -> Optional[UserProfile]:
        """Get a user profile by user UID"""
        return await self.user_account_ops.get_userprofile(user_uid)

    async def get_userstatus(self, user_uid: str) -> Optional[UserStatus]:
        """Get a user status by user UID"""
        return await self.user_account_ops.get_userstatus(user_uid)

    async def create_userprofile(self, user_profile: UserProfile) -> UserProfile:
        """Create a new user profile"""
        return await self.user_account_ops.create_userprofile(user_profile)

    async def create_userstatus(
        self,
        user_uid: str,
        primary_usertype: str,
        organizations_uids: Optional[Set[str]] = None,
        secondary_usertypes: Optional[List[str]] = None,
        initial_subscription_plan_id: Optional[str] = None,
        iam_domain_permissions: Optional[Dict[str, Dict[str, Dict[str, IAMUnitRefAssignment]]]] = None,
        sbscrptn_based_insight_credits: int = 0,
        extra_insight_credits: int = 0,
        voting_credits: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None
    ) -> UserStatus:
        """Create a new user status with optional initial subscription"""
        user_status = await self.user_account_ops.create_userstatus(
            user_uid=user_uid,
            primary_usertype=primary_usertype,
            organizations_uids=organizations_uids,
            secondary_usertypes=secondary_usertypes,
            iam_domain_permissions=iam_domain_permissions,
            sbscrptn_based_insight_credits=sbscrptn_based_insight_credits,
            extra_insight_credits=extra_insight_credits,
            voting_credits=voting_credits,
            metadata=metadata,
            created_by=created_by
        )

        # Apply initial subscription if provided
        if initial_subscription_plan_id:
            try:
                await self.subscription_ops.apply_subscription_plan(
                    user_uid=user_uid,
                    plan_id=initial_subscription_plan_id,
                    source=f"initial_setup_by_{created_by or 'system'}"
                )
                # Fetch updated status with subscription
                updated_status = await self.get_userstatus(user_uid)
                return updated_status or user_status
            except Exception as e:
                self.logger.error(f"Failed to apply initial subscription plan {initial_subscription_plan_id} for {user_uid}: {e}")
                # Return the status without subscription rather than failing completely

        return user_status

    async def update_userprofile(self, user_uid: str, profile_data: Dict[str, Any], updater_uid: str) -> UserProfile:
        """Update a user profile"""
        return await self.user_account_ops.update_userprofile(user_uid, profile_data, updater_uid)

    async def update_userstatus(self, user_uid: str, status_data: Dict[str, Any], updater_uid: str) -> UserStatus:
        """Update a user status"""
        return await self.user_account_ops.update_userstatus(user_uid, status_data, updater_uid)

    ##########################################################################################
    ################################ Hollistic User Creation #################################

    async def create_user(
        self,
        email: str,
        provider_id: str,
        primary_usertype_name: str,
        initial_subscription_plan_id: Optional[str] = None,
        organizations_uids: Optional[Set[str]] = None,
        secondary_usertype_names: Optional[List[str]] = None,
        profile_custom_data: Optional[Dict[str, Any]] = None,
        status_custom_data: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
        use_firestore_defaults: bool = True,
        password: Optional[str] = None,
        email_verified: bool = False,
        disabled: bool = False
    ) -> Tuple[Optional[UserProfile], Optional[UserStatus], Optional[str]]:
        """
        Create a complete user with Firebase Auth, UserProfile, and UserStatus

        This method creates the complete user including Firebase Auth user with custom claims.
        It delegates to UserHolisticOperations for coordinated user creation.

        Returns:
            Tuple of (UserProfile, UserStatus, error_message)
            If successful, error_message is None
            If failed, one or both models may be None with error_message describing the failure
        """
        self.logger.info(f"Starting complete user creation for Email: {email}, Type: {primary_usertype_name}")
        effective_creator = created_by or f"UserCoreService.create_user:email_{email}"

        # Fetch user type defaults if enabled
        usertype_defaults: Dict[str, Any] = {}
        if use_firestore_defaults:
            fetched_defaults = await self.fetch_user_defaults(primary_usertype_name)
            if fetched_defaults:
                usertype_defaults = fetched_defaults
            else:
                #### TODO  : FIX HOW ERRORS ARE ACTUALLY REPORTED. SERVICEMON ?
                self.logger.error(f"User defaults not found for '{primary_usertype_name}', proceeding with empty defaults")
                raise UserCreationError(f"User defaults not found for '{primary_usertype_name}'")

        # Prepare data with defaults
        final_secondary_usertypes = secondary_usertype_names or usertype_defaults.get('default_secondary_usertypes', [])
        final_organizations_uids = organizations_uids or set(usertype_defaults.get('default_organizations_uids', []))

        # Extract custom data fields
        iam_domain_permissions = (status_custom_data or {}).get('iam_domain_permissions')
        if iam_domain_permissions is None and use_firestore_defaults:
            iam_domain_permissions = usertype_defaults.get('default_iam_domain_permissions', {})

        effective_initial_plan_id = initial_subscription_plan_id
        if effective_initial_plan_id is None and use_firestore_defaults:
            effective_initial_plan_id = usertype_defaults.get('default_subscription_plan_id')

        # Credits from defaults or custom data
        default_sbscrptn_credits = usertype_defaults.get('default_subscription_based_insight_credits', 0) if use_firestore_defaults else 0
        default_extra_credits = usertype_defaults.get('default_extra_insight_credits', 0) if use_firestore_defaults else 0
        default_voting_credits = usertype_defaults.get('default_voting_credits', 0) if use_firestore_defaults else 0

        sbscrptn_based_insight_credits = (status_custom_data or {}).get('sbscrptn_based_insight_credits', default_sbscrptn_credits)
        extra_insight_credits = (status_custom_data or {}).get('extra_insight_credits', default_extra_credits)
        voting_credits = (status_custom_data or {}).get('voting_credits', default_voting_credits)
        metadata = (status_custom_data or {}).get('metadata', {})

        # Extract profile fields from profile_custom_data
        first_name = (profile_custom_data or {}).get('first_name')
        last_name = (profile_custom_data or {}).get('last_name')
        username = (profile_custom_data or {}).get('username')
        mobile = (profile_custom_data or {}).get('mobile')

        try:
            # Delegate to UserHolisticOperations for complete user creation
            created_user_uid, created_profile, created_status = await self.user_holistic_ops.create_user(
                email=email,
                primary_usertype=primary_usertype_name,
                password=password,
                organizations_uids=final_organizations_uids,
                secondary_usertypes=final_secondary_usertypes,
                first_name=first_name,
                last_name=last_name,
                username=username,
                mobile=mobile,
                provider_id=provider_id,
                email_verified=email_verified,
                disabled=disabled,
                initial_subscription_plan_id=effective_initial_plan_id,
                iam_domain_permissions=iam_domain_permissions,
                sbscrptn_based_insight_credits=sbscrptn_based_insight_credits,
                extra_insight_credits=extra_insight_credits,
                voting_credits=voting_credits,
                metadata=metadata,
                created_by=effective_creator,
                set_custom_claims=True  # Always set custom claims for complete user creation
            )

            self.logger.info(f"Successfully created complete user {created_user_uid}")
            return created_profile, created_status, None

        except Exception as e:
            error_msg = f"Failed to create complete user for email {email}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return None, None, error_msg


    ##########################################################################################
    ################################ Subscription Operations #################################

    async def get_user_active_subscription(self, user_uid: str) -> Optional[Subscription]:
        """Get the user's currently active subscription"""
        return await self.subscription_ops.get_user_active_subscription(user_uid)

    async def change_user_subscription(self, user_uid: str, new_plan_id: str, source: Optional[str] = None) -> Optional[Subscription]:
        """Change a user's subscription to a new plan"""
        return await self.subscription_ops.change_user_subscription(user_uid, new_plan_id, source)

    async def cancel_user_subscription(self, user_uid: str, reason: Optional[str] = None, cancelled_by: Optional[str] = None) -> bool:
        """Cancel a user's active subscription"""
        return await self.subscription_ops.cancel_user_subscription(user_uid, reason, cancelled_by)


    async def _apply_subscription_plan(self, user_uid: str, plan_id: str, source: str = "system_default_config") -> Subscription:
        """Apply subscription plan (backward compatibility)"""
        return await self.subscription_ops.apply_subscription_plan(user_uid, plan_id, source)

    ##########################################################################################
    ################################ IAM Operations Operations #################################


    # Deletion Operations (delegated to UserHolisticOperations)

    async def delete_user_account_docs(
        self,
        user_uid: str,
        deleted_by: str = "system_deletion"
    ) -> Tuple[bool, bool, Optional[str]]:
        """Delete user documents (profile and status)"""
        # Use the new user_holistic_ops for coordinated deletion
        result = await self.user_holistic_ops.delete_user(
            user_uid=user_uid,
            delete_auth_user=False,  # Only delete profile and status
            delete_profile=True,
            delete_status=True,
            deleted_by=deleted_by
        )
        return (
            result["profile_deleted_successfully"],
            result["status_deleted_successfully"],
            result["errors"][0] if result["errors"] else None
        )

    async def delete_user_holistically_with_auth(
        self,
        user_uid: str,
        delete_auth_user: bool = True,
        deleted_by: str = "system_full_deletion"
    ) -> Dict[str, Any]:
        """Complete user deletion including Firebase Auth deletion"""
        return await self.user_holistic_ops.delete_user(user_uid, delete_auth_user, deleted_by=deleted_by)

    async def batch_delete_user_account_docs(
        self,
        user_uids: List[str],
        deleted_by: str = "system_batch_deletion"
    ) -> Dict[str, Tuple[bool, bool, Optional[str]]]:
        """Batch delete multiple users' documents"""
        results_holistic = await self.user_holistic_ops.batch_delete_users(user_uids, delete_auth_user=False, deleted_by=deleted_by)

        # Convert to expected format
        converted_results = {}
        for user_uid, result in results_holistic.items():
            error_msg = result["errors"][0] if result["errors"] else None
            converted_results[user_uid] = (
                result["profile_deleted_successfully"],
                result["status_deleted_successfully"],
                error_msg
            )

        return converted_results

    # Utility Methods

    async def get_user_account_docs(self, user_uid: str) -> Tuple[Optional[UserProfile], Optional[UserStatus]]:
        """Get both user profile and status"""
        return await self.user_account_ops.get_user_core_docs(user_uid)

    async def user_core_docs_exist(self, user_uid: str) -> Tuple[bool, bool]:
        """Check if user profile and/or status exist"""
        return await self.user_account_ops.user_core_docs_exist(user_uid)

    async def validate_user_account_data(
        self,
        profile_data: Optional[Dict[str, Any]] = None,
        status_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, List[str]]:
        """Validate user profile and status data without creating documents"""
        return await self.user_account_ops.validate_user_core_data(profile_data, status_data)

    # Enhanced Methods for Advanced Operations

    async def get_users_by_usertype(
        self,
        primary_usertype: str,
        limit: Optional[int] = None
    ) -> List[UserProfile]:
        """Get users by primary usertype (requires custom implementation)"""
        # This would require a more advanced query system
        # For now, we'll raise NotImplementedError to indicate this needs custom implementation
        raise NotImplementedError("get_users_by_usertype requires custom query implementation")

    async def get_users_by_organization(
        self,
        organization_uid: str,
        limit: Optional[int] = None
    ) -> List[UserProfile]:
        """Get users by organization (requires custom implementation)"""
        # This would require a more advanced query system
        raise NotImplementedError("get_users_by_organization requires custom query implementation")

    async def bulk_update_user_permissions(
        self,
        user_uids: List[str],
        domain: str,
        permissions_to_add: List[str],
        permissions_to_remove: List[str],
        updater_uid: str
    ) -> Dict[str, bool]:
        """Bulk update permissions for multiple users"""
        results = {}

        for user_uid in user_uids:
            try:
                # Add permissions
                for permission in permissions_to_add:
                    await self.iam_ops.add_user_permission(
                        user_uid=user_uid,
                        domain=domain,
                        permission_name=permission,
                        iam_unit_type=IAMUnitType.GROUPS,  # Default to groups
                        source=f"bulk_update_by_{updater_uid}",
                        updater_uid=updater_uid
                    )

                # Remove permissions
                for permission in permissions_to_remove:
                    await self.iam_ops.remove_user_permission(
                        user_uid=user_uid,
                        domain=domain,
                        permission_name=permission,
                        iam_unit_type=IAMUnitType.GROUPS,  # Default to groups
                        updater_uid=updater_uid
                    )

                results[user_uid] = True

            except Exception as e:
                self.logger.error(f"Failed to update permissions for user {user_uid}: {e}")
                results[user_uid] = False

        return results

    # Statistics and Analytics Methods

    async def get_user_statistics(self) -> Dict[str, int]:
        """Get basic user statistics (requires custom implementation)"""
        # This would require aggregation queries
        raise NotImplementedError("get_user_statistics requires custom aggregation implementation")

    async def get_subscription_statistics(self) -> Dict[str, int]:
        """Get subscription statistics (requires custom implementation)"""
        # This would require aggregation queries
        raise NotImplementedError("get_subscription_statistics requires custom aggregation implementation")

    # User 360 Operations (Complete User Lifecycle)

    async def create_complete_user_with_auth(
        self,
        email: str,
        primary_usertype: str,
        password: Optional[str] = None,
        organizations_uids: Optional[Set[str]] = None,
        secondary_usertypes: Optional[List[str]] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        mobile: Optional[str] = None,
        provider_id: str = "password",
        email_verified: bool = False,
        disabled: bool = False,
        initial_subscription_plan_id: Optional[str] = None,
        iam_domain_permissions: Optional[Dict[str, Dict[str, Dict[str, IAMUnitRefAssignment]]]] = None,
        sbscrptn_based_insight_credits: int = 0,
        extra_insight_credits: int = 0,
        voting_credits: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
        set_custom_claims: bool = True
    ) -> Tuple[str, UserProfile, UserStatus]:
        """
        Create complete user with Firebase Auth, UserProfile, and UserStatus

        This method directly delegates to UserHolisticOperations.create_user
        """
        return await self.user_holistic_ops.create_user(
            email=email,
            primary_usertype=primary_usertype,
            password=password,
            organizations_uids=organizations_uids,
            secondary_usertypes=secondary_usertypes,
            first_name=first_name,
            last_name=last_name,
            username=username,
            mobile=mobile,
            provider_id=provider_id,
            email_verified=email_verified,
            disabled=disabled,
            initial_subscription_plan_id=initial_subscription_plan_id,
            iam_domain_permissions=iam_domain_permissions,
            sbscrptn_based_insight_credits=sbscrptn_based_insight_credits,
            extra_insight_credits=extra_insight_credits,
            voting_credits=voting_credits,
            metadata=metadata,
            created_by=created_by,
            set_custom_claims=set_custom_claims
        )

    async def delete_complete_user(
        self,
        user_uid: str,
        delete_auth_user: bool = True,
        delete_profile: bool = True,
        delete_status: bool = True,
        deleted_by: str = "system_complete_deletion"
    ) -> Dict[str, Any]:
        """Delete complete user including Firebase Auth, UserProfile, and UserStatus"""
        return await self.user_holistic_ops.delete_user(
            user_uid=user_uid,
            delete_auth_user=delete_auth_user,
            delete_profile=delete_profile,
            delete_status=delete_status,
            deleted_by=deleted_by
        )

    async def user_exists_complete(self, user_uid: str) -> Dict[str, bool]:
        """Check if complete user exists (Auth, Profile, Status)"""
        return await self.user_holistic_ops.user_exists_fully(user_uid)

    async def validate_complete_user(self, user_uid: str) -> Dict[str, Any]:
        """Validate complete user integrity"""
        return await self.user_holistic_ops.validate_user_full_existance(user_uid)

    # User Auth Operations

    async def create_userauth(
        self,
        email: str,
        password: Optional[str] = None,
        email_verified: bool = False,
        disabled: bool = False,
        display_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        custom_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create Firebase Auth user"""
        user_auth = UserAuth(
            email=email,
            password=password,
            email_verified=email_verified,
            disabled=disabled,
            phone_number=phone_number,
            custom_claims=custom_claims
        )
        return await self.user_auth_ops.create_userauth(user_auth)

    async def delete_userauth(self, user_uid: str) -> bool:
        """Delete Firebase Auth user"""
        return await self.user_auth_ops.delete_userauth(user_uid)

    async def userauth_exists(self, user_uid: str) -> bool:
        """Check if Firebase Auth user exists"""
        return await self.user_auth_ops.userauth_exists(user_uid)

    # Custom Claims Operations (delegated to user_auth_ops)

    async def set_userauth_custom_claims(
        self,
        user_uid: str,
        custom_claims: Dict[str, Any],
        merge_with_existing: bool = False
    ) -> bool:
        """Set Firebase Auth custom claims for a user with optional merging"""
        return await self.user_auth_ops.set_userauth_custom_claims(user_uid, custom_claims, merge_with_existing)
