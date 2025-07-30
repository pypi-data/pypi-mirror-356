"""
User Auth Operations - Handle Firebase Auth user creation, management, and deletion
"""
import os
import asyncio
import logging
from typing import Dict, Any, Optional, List
from firebase_admin import auth
from ...models.user_auth import UserAuth
from ...exceptions import UserAuthError


class UserAuthOperations:
    """
    Handles Firebase Auth operations for user creation, management, and deletion
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    # User Auth Operations

    async def create_userauth(
        self,
        user_auth: UserAuth
    ) -> str:
        """Create a new Firebase Auth user from UserAuth model and return the UID"""
        try:
            # Create user synchronously
            loop = asyncio.get_event_loop()
            user_record = await loop.run_in_executor(
                None,
                lambda: auth.create_user(
                    email=user_auth.email,
                    email_verified=user_auth.email_verified,
                    password=user_auth.password,
                    phone_number=user_auth.phone_number,
                    disabled=user_auth.disabled
                )
            )

            user_uid = user_record.uid
            self.logger.info(f"Successfully created Firebase Auth user with UID: {user_uid}")

            # Set custom claims if provided
            if user_auth.custom_claims:
                await self.set_userauth_custom_claims(user_uid, user_auth.custom_claims)

            return user_uid

        except auth.EmailAlreadyExistsError:
            raise UserAuthError(
                detail=f"User with email {user_auth.email} already exists",
                operation="create_userauth",
                additional_info={"email": str(user_auth.email)}
            )
        except Exception as e:
            self.logger.error(f"Failed to create Firebase Auth user: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to create Firebase Auth user: {str(e)}",
                operation="create_userauth",
                additional_info={"email": str(user_auth.email)},
                original_error=e
            )

    # Firebase Auth User Management

    async def get_userauth(self, user_uid: str) -> Optional[auth.UserRecord]:
        """Get Firebase Auth user by UID"""
        try:
            loop = asyncio.get_event_loop()
            user_record = await loop.run_in_executor(
                None,
                auth.get_user,
                user_uid
            )
            return user_record
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            self.logger.error(f"Failed to get Firebase Auth user {user_uid}: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to get Firebase Auth user: {str(e)}",
                user_uid=user_uid,
                operation="get_userauth",
                original_error=e
            )

    async def get_userauth_by_email(self, email: str) -> Optional[auth.UserRecord]:
        """Get Firebase Auth user by email"""
        try:
            loop = asyncio.get_event_loop()
            user_record = await loop.run_in_executor(
                None,
                auth.get_user_by_email,
                email
            )
            return user_record
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            self.logger.error(f"Failed to get Firebase Auth user by email {email}: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to get Firebase Auth user by email: {str(e)}",
                operation="get_userauth_by_email",
                additional_info={"email": email},
                original_error=e
            )

    async def update_userauth(
        self,
        user_uid: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        display_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        email_verified: Optional[bool] = None,
        disabled: Optional[bool] = None
    ) -> auth.UserRecord:
        """Update Firebase Auth user"""
        try:
            loop = asyncio.get_event_loop()
            user_record = await loop.run_in_executor(
                None,
                lambda: auth.update_user(
                    uid=user_uid,
                    email=email,
                    password=password,
                    display_name=display_name,
                    phone_number=phone_number,
                    email_verified=email_verified,
                    disabled=disabled
                )
            )

            self.logger.info(f"Successfully updated Firebase Auth user: {user_uid}")
            return user_record

        except auth.UserNotFoundError:
            raise UserAuthError(
                detail=f"Firebase Auth user not found",
                user_uid=user_uid,
                operation="update_userauth"
            )
        except Exception as e:
            self.logger.error(f"Failed to update Firebase Auth user {user_uid}: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to update Firebase Auth user: {str(e)}",
                user_uid=user_uid,
                operation="update_userauth",
                original_error=e
            )

    # Firebase Auth Custom Claims

    def generate_firebase_custom_claims(
        self,
        primary_usertype: str,
        secondary_usertypes: Optional[List[str]] = None,
        organizations_uids: Optional[List[str]] = None,
        user_approval_status: str = "pending"
    ) -> Dict[str, Any]:
        """Generate Firebase custom claims with minimal required fields"""
        try:
            claims = {
                "primary_usertype": primary_usertype,
                "secondary_usertypes": secondary_usertypes or [],
                "organizations_uids": organizations_uids or [],
                "user_approval_status": user_approval_status,
            }
            self.logger.info(f"Generated Firebase custom claims for usertype {primary_usertype}")
            return claims
        except Exception as e:
            self.logger.error(f"Error generating Firebase custom claims: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to generate Firebase custom claims: {str(e)}",
                operation="generate_firebase_custom_claims",
                original_error=e
            )

    async def set_userauth_custom_claims(
        self,
        user_uid: str,
        custom_claims: Dict[str, Any],
        merge_with_existing: bool = False
    ) -> bool:
        """Set Firebase Auth custom claims for a user with optional merging"""
        try:
            if merge_with_existing:
                # Get existing claims and merge
                user_record = await self.get_userauth(user_uid)
                if user_record and user_record.custom_claims:
                    existing_claims = user_record.custom_claims.copy()
                    existing_claims.update(custom_claims)
                    custom_claims = existing_claims

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                auth.set_custom_user_claims,
                user_uid,
                custom_claims
            )

            self.logger.info(f"Successfully set Firebase custom claims for user: {user_uid}")
            return True

        except auth.UserNotFoundError:
            raise UserAuthError(
                detail=f"Firebase Auth user not found",
                user_uid=user_uid,
                operation="set_userauth_custom_claims"
            )
        except Exception as e:
            self.logger.error(f"Failed to set Firebase custom claims for user {user_uid}: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to set Firebase custom claims: {str(e)}",
                user_uid=user_uid,
                operation="set_userauth_custom_claims",
                original_error=e
            )

    async def get_userauth_custom_claims(self, user_uid: str) -> Optional[Dict[str, Any]]:
        """Get Firebase Auth custom claims for a user"""
        try:
            user_record = await self.get_userauth(user_uid)
            return user_record.custom_claims if user_record else None
        except Exception as e:
            self.logger.error(f"Failed to get Firebase custom claims for user {user_uid}: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to get Firebase custom claims: {str(e)}",
                user_uid=user_uid,
                operation="get_userauth_custom_claims",
                original_error=e
            )

    # Firebase Auth User Deletion

    async def delete_userauth(self, user_uid: str) -> bool:
        """Delete Firebase Auth user"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                auth.delete_user,
                user_uid
            )

            self.logger.info(f"Successfully deleted Firebase Auth user: {user_uid}")
            return True

        except auth.UserNotFoundError:
            self.logger.warning(f"Firebase Auth user {user_uid} not found during deletion")
            return True  # Consider non-existent user as successfully deleted
        except Exception as e:
            self.logger.error(f"Failed to delete Firebase Auth user {user_uid}: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to delete Firebase Auth user: {str(e)}",
                user_uid=user_uid,
                operation="delete_userauth",
                original_error=e
            )

    # Utility Methods

    async def userauth_exists(self, user_uid: str) -> bool:
        """Check if Firebase Auth user exists"""
        user_record = await self.get_userauth(user_uid)
        return user_record is not None

    async def userauth_exists_by_email(self, email: str) -> bool:
        """Check if Firebase Auth user exists by email"""
        user_record = await self.get_userauth_by_email(email)
        return user_record is not None

    async def validate_userauth(self, user_uid: str) -> bool:
        """Validate that Firebase Auth user exists and is not disabled"""
        try:
            user_record = await self.get_userauth(user_uid)
            if not user_record:
                return False
            return not user_record.disabled
        except Exception:
            return False

    async def list_userauth(
        self,
        page_token: Optional[str] = None,
        max_results: int = 1000
    ) -> auth.ListUsersPage:
        """List Firebase Auth users with pagination"""
        try:
            loop = asyncio.get_event_loop()
            page = await loop.run_in_executor(
                None,
                lambda: auth.list_users(page_token=page_token, max_results=max_results)
            )
            return page
        except Exception as e:
            self.logger.error(f"Failed to list Firebase Auth users: {e}", exc_info=True)
            raise UserAuthError(
                detail=f"Failed to list Firebase Auth users: {str(e)}",
                operation="list_userauth",
                original_error=e
            )
