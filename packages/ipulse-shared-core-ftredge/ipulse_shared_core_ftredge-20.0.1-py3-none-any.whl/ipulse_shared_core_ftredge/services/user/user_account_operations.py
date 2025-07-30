"""
User Management Operations - CRUD operations for UserProfile and UserStatus
"""
import os
import logging
from typing import Dict, Any, Optional, Set, List, Tuple
from google.cloud import firestore
from pydantic import ValidationError as PydanticValidationError

from ...models.user_profile import UserProfile
from ...models.user_status import UserStatus, IAMUnitRefAssignment
from ...exceptions import ServiceError, ResourceNotFoundError, UserProfileError, UserStatusError, UserValidationError, UserCreationError, UserDeletionError
from ..base import BaseFirestoreService


class UserAccountOperations:
    """
    Handles CRUD operations for UserProfile and UserStatus documents
    """

    def __init__(
        self,
        firestore_client: firestore.Client,
        logger: Optional[logging.Logger] = None,
        timeout: float = 10.0,
        profile_collection: Optional[str] = None,
        status_collection: Optional[str] = None
    ):
        self.db = firestore_client
        self.logger = logger or logging.getLogger(__name__)
        self.timeout = timeout

        self.profile_collection_name = profile_collection or UserProfile.get_collection_name()
        self.status_collection_name = status_collection or UserStatus.get_collection_name()

        # Archival configuration
        self.archive_profile_on_delete = os.getenv('ARCHIVE_USER_PROFILE_ON_DELETE', 'true').lower() == 'true'
        self.archive_status_on_delete = os.getenv('ARCHIVE_USER_STATUS_ON_DELETE', 'true').lower() == 'true'

        # Archive collection names
        self.archive_profile_collection_name = os.getenv(
            'ARCHIVE_PROFILE_COLLECTION_NAME',
            f"~archive_core_user_userprofiles"
        )
        self.archive_status_collection_name = os.getenv(
            'ARCHIVE_STATUS_COLLECTION_NAME',
            f"~archive_core_user_userstatuss"
        )

        # Initialize DB services
        self._profile_db_service = BaseFirestoreService[UserProfile](
            db=self.db,
            collection_name=self.profile_collection_name,
            resource_type=UserProfile.OBJ_REF,
            logger=self.logger,
            timeout=self.timeout
        )

        self._status_db_service = BaseFirestoreService[UserStatus](
            db=self.db,
            collection_name=self.status_collection_name,
            resource_type=UserStatus.OBJ_REF,
            logger=self.logger,
            timeout=self.timeout
        )

    # UserProfile Operations

    async def get_userprofile(self, user_uid: str) -> Optional[UserProfile]:
        """Get a user profile by user UID"""
        profile_id = f"{UserProfile.OBJ_REF}_{user_uid}"
        try:
            profile_data = await self._profile_db_service.get_document(profile_id)
            return UserProfile(**profile_data) if profile_data else None
        except ResourceNotFoundError:
            self.logger.info(f"UserProfile not found for user_uid: {user_uid}")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching UserProfile for {user_uid}: {e}", exc_info=True)
            raise UserProfileError(
                detail=f"Failed to fetch user profile: {str(e)}",
                user_uid=user_uid,
                operation="get_userprofile",
                original_error=e
            )

    async def create_userprofile(self, user_profile: UserProfile) -> UserProfile:
        """Create a new user profile"""
        try:
            creator_uid = user_profile.created_by or f"UserManagement.create_profile:uid_{user_profile.user_uid}"
            created_data = await self._profile_db_service.create_document(
                user_profile.id,
                user_profile,
                creator_uid=creator_uid
            )
            self.logger.info(f"UserProfile created for {user_profile.user_uid}")
            return UserProfile(**created_data)
        except Exception as e:
            self.logger.error(f"Error creating UserProfile for {user_profile.user_uid}: {e}", exc_info=True)
            raise UserProfileError(
                detail=f"Failed to create user profile: {str(e)}",
                user_uid=user_profile.user_uid,
                operation="create_userprofile",
                original_error=e
            )

    async def update_userprofile(self, user_uid: str, profile_data: Dict[str, Any], updater_uid: str) -> UserProfile:
        """Update a user profile"""
        profile_id = f"{UserProfile.OBJ_REF}_{user_uid}"

        # Remove system fields that shouldn't be updated
        update_data = profile_data.copy()
        update_data.pop('user_uid', None)
        update_data.pop('id', None)
        update_data.pop('created_at', None)
        update_data.pop('created_by', None)

        try:
            updated_doc_dict = await self._profile_db_service.update_document(
                profile_id,
                update_data,
                updater_uid=updater_uid
            )
            self.logger.info(f"UserProfile for {user_uid} updated successfully by {updater_uid}")
            return UserProfile(**updated_doc_dict)
        except ResourceNotFoundError:
            raise UserProfileError(
                detail="User profile not found",
                user_uid=user_uid,
                operation="update_userprofile"
            )
        except Exception as e:
            self.logger.error(f"Error updating UserProfile for {user_uid}: {e}", exc_info=True)
            raise UserProfileError(
                detail=f"Failed to update user profile: {str(e)}",
                user_uid=user_uid,
                operation="update_userprofile",
                original_error=e
            )

    async def delete_userprofile(self, user_uid: str, deleted_by: str = "system_deletion") -> bool:
        """Delete (archive and delete) user profile"""
        import os

        profile_doc_id = f"userprofile_{user_uid}"

        # Archival configuration
        archive_profile_on_delete = os.getenv('ARCHIVE_USER_PROFILE_ON_DELETE', 'true').lower() == 'true'
        archive_profile_collection_name = os.getenv(
            'ARCHIVE_PROFILE_COLLECTION_NAME',
            f"~archive_core_user_userprofiles"
        )

        try:
            # Get profile data for archival
            profile_data = await self._profile_db_service.get_document(profile_doc_id)

            if profile_data:
                # Archive if enabled
                if archive_profile_on_delete:
                    await self._profile_db_service.archive_document(
                        document_data=profile_data,
                        doc_id=profile_doc_id,
                        archive_collection=archive_profile_collection_name,
                        archived_by=deleted_by
                    )

                # Delete the original document
                await self._profile_db_service.delete_document(profile_doc_id)
                self.logger.info(f"Successfully deleted user profile: {profile_doc_id}")
                return True
            else:
                self.logger.warning(f"User profile {profile_doc_id} not found for deletion")
                return True  # Consider non-existent as successfully deleted

        except Exception as e:
            self.logger.error(f"Failed to delete user profile {profile_doc_id}: {e}", exc_info=True)
            raise UserProfileError(
                detail=f"Failed to delete user profile: {str(e)}",
                user_uid=user_uid,
                operation="delete_userprofile",
                original_error=e
            )

    # UserStatus Operations

    async def get_userstatus(self, user_uid: str) -> Optional[UserStatus]:
        """Get a user status by user UID"""
        status_id = f"{UserStatus.OBJ_REF}_{user_uid}"
        try:
            status_data = await self._status_db_service.get_document(status_id)
            return UserStatus(**status_data) if status_data else None
        except ResourceNotFoundError:
            self.logger.info(f"UserStatus not found for user_uid: {user_uid}")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching UserStatus for {user_uid}: {e}", exc_info=True)
            raise UserStatusError(
                detail=f"Failed to fetch user status: {str(e)}",
                user_uid=user_uid,
                operation="get_userstatus",
                original_error=e
            )

    async def create_userstatus(
        self,
        user_uid: str,
        organizations_uids: Optional[Set[str]] = None,
        iam_domain_permissions: Optional[Dict[str, Dict[str, Dict[str, IAMUnitRefAssignment]]]] = None,
        sbscrptn_based_insight_credits: int = 0,
        extra_insight_credits: int = 0,
        voting_credits: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None
    ) -> UserStatus:
        """Create a new user status"""
        user_status_id = f"{UserStatus.OBJ_REF}_{user_uid}"
        effective_created_by = created_by or f"UserManagement.create_status:uid_{user_uid}"

        user_status_data = {
            'id': user_status_id,
            'user_uid': user_uid,
            'organizations_uids': organizations_uids or set(),
            'iam_domain_permissions': iam_domain_permissions or {},
            'subscriptions_history': {},
            'active_subscription': None,
            'sbscrptn_based_insight_credits': sbscrptn_based_insight_credits,
            'extra_insight_credits': extra_insight_credits,
            'voting_credits': voting_credits,
            'metadata': metadata or {},
            'created_by': effective_created_by,
            'updated_by': effective_created_by,
            'schema_version': UserStatus.VERSION
        }

        try:
            user_status = UserStatus(**user_status_data)
        except PydanticValidationError as e:
            self.logger.error(f"Pydantic validation error for UserStatus {user_uid}: {e}", exc_info=True)
            raise UserValidationError(
                detail=f"Validation failed: {e.errors() if hasattr(e, 'errors') else str(e)}",
                user_uid=user_uid,
                validation_field="user_status_data",
                original_error=e
            )

        try:
            await self._status_db_service.create_document(
                doc_id=user_status.id,
                data=user_status,
                creator_uid=effective_created_by
            )
            self.logger.info(f"UserStatus created for {user_uid} with id {user_status.id}")

            # Return the latest status to ensure consistency
            final_user_status = await self.get_userstatus(user_uid)
            if not final_user_status:
                raise UserStatusError(
                    detail="UserStatus disappeared after creation",
                    user_uid=user_uid,
                    operation="create_userstatus"
                )
            return final_user_status

        except Exception as e:
            self.logger.error(f"Failed to create UserStatus for {user_uid}: {e}", exc_info=True)
            raise UserStatusError(
                detail=f"Failed to create user status: {str(e)}",
                user_uid=user_uid,
                operation="create_userstatus",
                original_error=e
            )

    async def update_userstatus(self, user_uid: str, status_data: Dict[str, Any], updater_uid: str) -> UserStatus:
        """Update a user status"""
        user_status_id = f"{UserStatus.OBJ_REF}_{user_uid}"

        # Remove system fields that shouldn't be updated
        update_data = status_data.copy()
        update_data.pop('user_uid', None)
        update_data.pop('id', None)
        update_data.pop('created_at', None)
        update_data.pop('created_by', None)

        try:
            updated_doc_dict = await self._status_db_service.update_document(
                user_status_id,
                update_data,
                updater_uid=updater_uid
            )
            self.logger.info(f"UserStatus for {user_uid} updated successfully by {updater_uid}")
            return UserStatus(**updated_doc_dict)
        except ResourceNotFoundError:
            raise UserStatusError(
                detail="User status not found",
                user_uid=user_uid,
                operation="update_userstatus"
            )
        except Exception as e:
            self.logger.error(f"Error updating UserStatus for {user_uid}: {e}", exc_info=True)
            raise UserStatusError(
                detail=f"Failed to update user status: {str(e)}",
                user_uid=user_uid,
                operation="update_userstatus",
                original_error=e
            )

    async def delete_userstatus(self, user_uid: str, deleted_by: str = "system_deletion") -> bool:
        """Delete (archive and delete) user status"""
        import os

        status_doc_id = f"userstatus_{user_uid}"

        # Archival configuration
        archive_status_on_delete = os.getenv('ARCHIVE_USER_STATUS_ON_DELETE', 'true').lower() == 'true'
        archive_status_collection_name = os.getenv(
            'ARCHIVE_STATUS_COLLECTION_NAME',
            f"~archive_core_user_userstatuss"
        )

        try:
            # Get status data for archival
            status_data = await self._status_db_service.get_document(status_doc_id)

            if status_data:
                # Archive if enabled
                if archive_status_on_delete:
                    await self._status_db_service.archive_document(
                        document_data=status_data,
                        doc_id=status_doc_id,
                        archive_collection=archive_status_collection_name,
                        archived_by=deleted_by
                    )

                # Delete the original document
                await self._status_db_service.delete_document(status_doc_id)
                self.logger.info(f"Successfully deleted user status: {status_doc_id}")
                return True
            else:
                self.logger.warning(f"User status {status_doc_id} not found for deletion")
                return True  # Consider non-existent as successfully deleted

        except Exception as e:
            self.logger.error(f"Failed to delete user status {status_doc_id}: {e}", exc_info=True)
            raise UserStatusError(
                detail=f"Failed to delete user status: {str(e)}",
                user_uid=user_uid,
                operation="delete_userstatus",
                original_error=e
            )

    # Combined Operations

    async def get_user_core_docs(self, user_uid: str) -> Tuple[Optional[UserProfile], Optional[UserStatus]]:
        """Get both user profile and status in one call"""
        try:
            profile = await self.get_userprofile(user_uid)
            status = await self.get_userstatus(user_uid)
            return profile, status
        except Exception as e:
            self.logger.error(f"Error fetching complete user data for {user_uid}: {e}", exc_info=True)
            raise UserCreationError(
                detail=f"Failed to fetch complete user data: {str(e)}",
                user_uid=user_uid,
                original_error=e
            )

    async def user_core_docs_exist(self, user_uid: str) -> Tuple[bool, bool]:
        """Check if user profile and/or status exist"""
        try:
            profile, status = await self.get_user_core_docs(user_uid)
            return profile is not None, status is not None
        except Exception as e:
            self.logger.error(f"Error checking user existence for {user_uid}: {e}", exc_info=True)
            return False, False

    # Restoration Operations

    async def restore_user_from_archive(
        self,
        user_uid: str,
        restore_profile: bool = True,
        restore_status: bool = True,
        restored_by: str = "system_restore"
    ) -> Dict[str, bool]:
        """Restore user documents from archive collections"""
        results = {"profile_restored": False, "status_restored": False}

        # Restore profile
        if restore_profile:
            try:
                profile_doc_id = f"userprofile_{user_uid}"
                profile_restored = await self._profile_db_service.restore_document(
                    doc_id=profile_doc_id,
                    source_collection=self.archive_profile_collection_name,
                    target_collection=self.profile_collection_name,
                    restored_by=restored_by
                )
                results["profile_restored"] = profile_restored
                if profile_restored:
                    self.logger.info(f"Restored UserProfile {profile_doc_id} from archive")
            except Exception as e:
                self.logger.error(f"Failed to restore UserProfile for {user_uid}: {e}", exc_info=True)

        # Restore status
        if restore_status:
            try:
                status_doc_id = f"userstatus_{user_uid}"
                status_restored = await self._status_db_service.restore_document(
                    doc_id=status_doc_id,
                    source_collection=self.archive_status_collection_name,
                    target_collection=self.status_collection_name,
                    restored_by=restored_by
                )
                results["status_restored"] = status_restored
                if status_restored:
                    self.logger.info(f"Restored UserStatus {status_doc_id} from archive")
            except Exception as e:
                self.logger.error(f"Failed to restore UserStatus for {user_uid}: {e}", exc_info=True)

        return results

    async def restore_userprofile_from_archive(
        self,
        user_uid: str,
        restored_by: str = "system_restore"
    ) -> bool:
        """Restore user profile from archive"""
        try:
            profile_doc_id = f"userprofile_{user_uid}"
            return await self._profile_db_service.restore_document(
                doc_id=profile_doc_id,
                source_collection=self.archive_profile_collection_name,
                target_collection=self.profile_collection_name,
                restored_by=restored_by
            )
        except Exception as e:
            self.logger.error(f"Failed to restore UserProfile for {user_uid}: {e}", exc_info=True)
            return False

    async def restore_userstatus_from_archive(
        self,
        user_uid: str,
        restored_by: str = "system_restore"
    ) -> bool:
        """Restore user status from archive"""
        try:
            status_doc_id = f"userstatus_{user_uid}"
            return await self._status_db_service.restore_document(
                doc_id=status_doc_id,
                source_collection=self.archive_status_collection_name,
                target_collection=self.status_collection_name,
                restored_by=restored_by
            )
        except Exception as e:
            self.logger.error(f"Failed to restore UserStatus for {user_uid}: {e}", exc_info=True)
            return False

    async def validate_user_core_data(
        self,
        profile_data: Optional[Dict[str, Any]] = None,
        status_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, List[str]]:
        """Validate user profile and status data without creating documents"""
        errors = []

        if profile_data:
            try:
                UserProfile(**profile_data)
            except PydanticValidationError as e:
                errors.append(f"Profile validation error: {str(e)}")

        if status_data:
            try:
                UserStatus(**status_data)
            except PydanticValidationError as e:
                errors.append(f"Status validation error: {str(e)}")

        return len(errors) == 0, errors
