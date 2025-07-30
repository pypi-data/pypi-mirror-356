"""
User Holistic Operations - Complete user lifecycle operations

Handles complete user creation and deletion operations that span across
Firebase Auth, UserProfile, and UserStatus in coordinated transactions.
"""
import logging
from typing import Dict, Any, Optional, Set, List, Tuple
from datetime import datetime, timezone

from ...models.user_profile import UserProfile
from ...models.user_status import UserStatus, IAMUnitRefAssignment
from ...models.user_auth import UserAuth
from .user_auth_operations import UserAuthOperations
from ...exceptions import (
    UserCreationError
)


class UserHolisticOperations:
    """
    Handles complete user lifecycle operations including coordinated creation and deletion
    of Firebase Auth users, UserProfile, and UserStatus documents.
    """

    def __init__(
        self,
        user_account_ops,  # UserManagementOperations instance
        user_auth_ops: Optional[UserAuthOperations] = None,
        subscription_ops=None,  # SubscriptionManagementOperations instance
        iam_ops=None,  # IAMManagementOperations instance
        logger: Optional[logging.Logger] = None
    ):
        self.user_account_ops = user_account_ops
        self.user_auth_ops = user_auth_ops or UserAuthOperations(logger)
        self.user_subscription_ops = subscription_ops
        self.iam_ops = iam_ops
        self.logger = logger or logging.getLogger(__name__)

    # Complete User Creation

    async def create_user(
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
        Create a complete user with Firebase Auth, UserProfile, and UserStatus
        Returns: (user_uid, user_profile, user_status)
        """
        user_uid = None
        profile_created = False
        status_created = False

        try:
            # Step 1: Create Firebase Auth user
            self.logger.info(f"Creating Firebase Auth user for email: {email}")
            user_auth = UserAuth(
                email=email,
                password=password,
                email_verified=email_verified,
                disabled=disabled,
                phone_number=mobile
            )
            user_uid = await self.user_auth_ops.create_userauth(user_auth)

            # Step 2: Create UserProfile
            self.logger.info(f"Creating UserProfile for user: {user_uid}")
            user_profile = UserProfile(
                user_uid=user_uid,
                primary_usertype=primary_usertype,
                secondary_usertypes=secondary_usertypes or [],
                email=email,
                organizations_uids=organizations_uids or set(),
                provider_id=provider_id,
                username=username or "",  # Will be auto-generated if empty
                first_name=first_name,
                last_name=last_name,
                mobile=mobile,
                metadata=metadata or {},
                created_by=created_by
            )

            user_profile = await self.user_account_ops.create_userprofile(user_profile)
            profile_created = True

            # Step 3: Create UserStatus
            self.logger.info(f"Creating UserStatus for user: {user_uid}")
            user_status = await self.user_account_ops.create_userstatus(
                user_uid=user_uid,
                primary_usertype=primary_usertype,
                organizations_uids=organizations_uids,
                secondary_usertypes=secondary_usertypes,
                initial_subscription_plan_id=initial_subscription_plan_id,
                iam_domain_permissions=iam_domain_permissions or {},
                sbscrptn_based_insight_credits=sbscrptn_based_insight_credits,
                extra_insight_credits=extra_insight_credits,
                voting_credits=voting_credits,
                metadata=metadata,
                created_by=created_by
            )
            status_created = True

            # Step 4: Set Firebase custom claims if requested
            if set_custom_claims:
                self.logger.info(f"Setting Firebase custom claims for user: {user_uid}")
                custom_claims = self.user_auth_ops.generate_firebase_custom_claims(
                    primary_usertype=primary_usertype,
                    secondary_usertypes=secondary_usertypes,
                    organizations_uids=list(organizations_uids) if organizations_uids else None
                )
                await self.user_auth_ops.set_userauth_custom_claims(user_uid, custom_claims)

            self.logger.info(f"Successfully created complete user: {user_uid}")
            return user_uid, user_profile, user_status

        except Exception as e:
            # Rollback on failure
            await self._rollback_user_creation(
                user_uid=user_uid,
                profile_created=profile_created,
                status_created=status_created,
                error_context=f"Failed during complete user creation: {str(e)}"
            )
            raise UserCreationError(
                detail=f"Failed to create complete user: {str(e)}",
                email=email,
                user_uid=user_uid,
                original_error=e
            )

    async def create_user_from_auth_model(
        self,
        user_auth: UserAuth,
        primary_usertype: str,
        organizations_uids: Optional[Set[str]] = None,
        secondary_usertypes: Optional[List[str]] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        initial_subscription_plan_id: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> Tuple[str, UserProfile, UserStatus]:
        """Create complete user from UserAuth model"""
        return await self.create_user(
            email=user_auth.email,
            primary_usertype=primary_usertype,
            password=user_auth.password,
            organizations_uids=organizations_uids,
            secondary_usertypes=secondary_usertypes,
            first_name=first_name,
            last_name=last_name,
            username=username,
            mobile=user_auth.phone_number,
            provider_id=user_auth.provider_id,
            email_verified=user_auth.email_verified,
            disabled=user_auth.disabled,
            initial_subscription_plan_id=initial_subscription_plan_id,
            metadata=user_auth.metadata,
            created_by=created_by,
            set_custom_claims=bool(user_auth.custom_claims)
        )

    async def _rollback_user_creation(
        self,
        user_uid: Optional[str],
        profile_created: bool,
        status_created: bool,
        error_context: str
    ) -> None:
        """Rollback user creation on failure"""
        self.logger.error(f"Rolling back user creation: {error_context}")

        if user_uid:
            # Delete UserStatus if created
            if status_created:
                try:
                    await self.user_account_ops.delete_userstatus(user_uid, "rollback_deletion")
                    self.logger.info(f"Rolled back UserStatus creation for: {user_uid}")
                except Exception as e:
                    self.logger.error(f"Failed to rollback UserStatus creation: {e}")

            # Delete UserProfile if created
            if profile_created:
                try:
                    await self.user_account_ops.delete_userprofile(user_uid, "rollback_deletion")
                    self.logger.info(f"Rolled back UserProfile creation for: {user_uid}")
                except Exception as e:
                    self.logger.error(f"Failed to rollback UserProfile creation: {e}")

            # Delete Firebase Auth user
            try:
                await self.user_auth_ops.delete_userauth(user_uid)
                self.logger.info(f"Rolled back Firebase Auth user creation for: {user_uid}")
            except Exception as e:
                self.logger.error(f"Failed to rollback Firebase Auth user creation: {e}")

    # Complete User Deletion

    async def delete_user(
        self,
        user_uid: str,
        delete_auth_user: bool = True,
        delete_profile: bool = True,
        delete_status: bool = True,
        deleted_by: str = "system_complete_deletion"
    ) -> Dict[str, Any]:
        """
        Delete complete user including Firebase Auth, UserProfile, and UserStatus
        with proper archival and error handling
        """
        results = {
            "user_uid": user_uid,
            "auth_deleted_successfully": False,
            "profile_deleted_successfully": False,
            "status_deleted_successfully": False,
            "errors": [],
            "deleted_by": deleted_by,
            "deleted_at": datetime.now(timezone.utc).isoformat()
        }

        # Step 1: Delete UserProfile (with archival)
        if delete_profile:
            try:
                profile_deleted = await self.user_account_ops.delete_userprofile(user_uid, deleted_by)
                results["profile_deleted_successfully"] = profile_deleted
                if profile_deleted:
                    self.logger.info(f"Successfully deleted UserProfile for user: {user_uid}")
            except Exception as e:
                error_msg = f"Failed to delete UserProfile: {str(e)}"
                self.logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

        # Step 2: Delete UserStatus (with archival)
        if delete_status:
            try:
                status_deleted = await self.user_account_ops.delete_userstatus(user_uid, deleted_by)
                results["status_deleted_successfully"] = status_deleted
                if status_deleted:
                    self.logger.info(f"Successfully deleted UserStatus for user: {user_uid}")
            except Exception as e:
                error_msg = f"Failed to delete UserStatus: {str(e)}"
                self.logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

        # Step 3: Delete Firebase Auth user
        if delete_auth_user:
            try:
                auth_deleted = await self.user_auth_ops.delete_userauth(user_uid)
                results["auth_deleted_successfully"] = auth_deleted
                if auth_deleted:
                    self.logger.info(f"Successfully deleted Firebase Auth user: {user_uid}")
            except Exception as e:
                error_msg = f"Failed to delete Firebase Auth user: {str(e)}"
                self.logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

        # Determine overall success
        total_operations = sum([delete_auth_user, delete_profile, delete_status])
        successful_operations = sum([
            results["auth_deleted_successfully"] if delete_auth_user else True,
            results["profile_deleted_successfully"] if delete_profile else True,
            results["status_deleted_successfully"] if delete_status else True
        ])

        results["overall_success"] = successful_operations == total_operations
        results["partial_success"] = successful_operations > 0

        if results["overall_success"]:
            self.logger.info(f"Successfully completed full deletion of user: {user_uid}")
        elif results["partial_success"]:
            self.logger.warning(f"Partial deletion completed for user {user_uid}. Errors: {results['errors']}")
        else:
            self.logger.error(f"Failed to delete user {user_uid}. Errors: {results['errors']}")

        return results

    async def batch_delete_users(
        self,
        user_uids: List[str],
        delete_auth_user: bool = True,
        deleted_by: str = "system_batch_complete_deletion"
    ) -> Dict[str, Dict[str, Any]]:
        """
        Batch delete multiple complete users
        Returns dictionary with user_uid as key and deletion result as value
        """
        results = {}

        for user_uid in user_uids:
            try:
                result = await self.delete_user(
                    user_uid=user_uid,
                    delete_auth_user=delete_auth_user,
                    deleted_by=deleted_by
                )
                results[user_uid] = result
            except Exception as e:
                self.logger.error(f"Failed to delete user {user_uid}: {e}", exc_info=True)
                results[user_uid] = {
                    "user_uid": user_uid,
                    "auth_deleted_successfully": False,
                    "profile_deleted_successfully": False,
                    "status_deleted_successfully": False,
                    "errors": [f"Batch deletion failed: {str(e)}"],
                    "overall_success": False,
                    "partial_success": False,
                    "deleted_by": deleted_by,
                    "deleted_at": datetime.now(timezone.utc).isoformat()
                }

        return results

    # Document-level batch operations

    async def batch_delete_user_core_docs(
        self,
        user_uids: List[str],
        deleted_by: str = "system_batch_deletion"
    ) -> Dict[str, Tuple[bool, bool, Optional[str]]]:
        """Batch delete multiple users' documents (profile and status only)"""
        batch_results: Dict[str, Tuple[bool, bool, Optional[str]]] = {}

        # Process sequentially to avoid overwhelming the database
        for user_uid in user_uids:
            self.logger.info(f"Batch deletion: Processing user_uid: {user_uid}")
            item_deleted_by = f"{deleted_by}_batch_item_{user_uid}"

            try:
                # Use delete_user but only for documents, not auth
                result = await self.delete_user(
                    user_uid=user_uid,
                    delete_auth_user=False,  # Only delete documents
                    delete_profile=True,
                    delete_status=True,
                    deleted_by=item_deleted_by
                )

                batch_results[user_uid] = (
                    result["profile_deleted_successfully"],
                    result["status_deleted_successfully"],
                    result["errors"][0] if result["errors"] else None
                )
            except Exception as e:
                self.logger.error(f"Batch deletion failed for user {user_uid}: {e}", exc_info=True)
                batch_results[user_uid] = (False, False, str(e))

        return batch_results

    # User Restoration

    async def restore_user_account_docs_from_archive(
        self,
        user_uid: str,
        restore_profile: bool = True,
        restore_status: bool = True,
        restored_by: str = "system_restore"
    ) -> Dict[str, bool]:
        """
        Restore complete user from archive (does not restore Firebase Auth user)
        Firebase Auth user needs to be recreated separately
        """
        results = {
            "profile_restored": False,
            "status_restored": False
        }

        if restore_profile:
            try:
                results["profile_restored"] = await self.user_account_ops.restore_userprofile_from_archive(
                    user_uid, restored_by
                )
            except Exception as e:
                self.logger.error(f"Failed to restore UserProfile for {user_uid}: {e}", exc_info=True)

        if restore_status:
            try:
                results["status_restored"] = await self.user_account_ops.restore_userstatus_from_archive(
                    user_uid, restored_by
                )
            except Exception as e:
                self.logger.error(f"Failed to restore UserStatus for {user_uid}: {e}", exc_info=True)

        return results

    # Utility Methods

    async def user_exists_fully(self, user_uid: str) -> Dict[str, bool]:
        """Check if complete user exists (Auth, Profile, Status)"""
        return {
            "auth_exists": await self.user_auth_ops.userauth_exists(user_uid),
            "profile_exists": (await self.user_account_ops.get_userprofile(user_uid)) is not None,
            "status_exists": (await self.user_account_ops.get_userstatus(user_uid)) is not None
        }

    async def validate_user_full_existance(self, user_uid: str) -> Dict[str, Any]:
        """Validate complete user integrity"""
        existence = await self.user_exists_fully(user_uid)

        validation_results = {
            "user_uid": user_uid,
            "exists": existence,
            "is_complete": all(existence.values()),
            "missing_components": [k for k, v in existence.items() if not v],
            "validation_errors": []
        }

        # Additional validation for existing components
        if existence["auth_exists"]:
            try:
                auth_valid = await self.user_auth_ops.validate_userauth(user_uid)
                validation_results["auth_valid"] = auth_valid
                if not auth_valid:
                    validation_results["validation_errors"].append("Firebase Auth user is disabled")
            except Exception as e:
                validation_results["validation_errors"].append(f"Auth validation error: {str(e)}")

        return validation_results
