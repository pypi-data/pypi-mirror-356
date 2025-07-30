"""
User Management Services Module

This module contains all user-related services organized into specialized operation classes:
- UserManagementOperations: Core CRUD operations for user profiles and status
- SubscriptionManagementOperations: Subscription plan management and operations
- IAMManagementOperations: Firebase Auth claims and permissions management
- UserDeletionOperations: User deletion and cleanup operations
- UserCoreService: Orchestrating service that composes all operation classes
- User-specific exceptions: Specialized exception classes for user operations
"""

from .user_account_operations import UserAccountOperations
from .subscription_management_operations import (
    SubscriptionManagementOperations,
    SubscriptionPlanDocument
)
from .iam_management_operations import IAMManagementOperations
from .user_auth_operations import UserAuthOperations
from .user_holistic_operations import UserHolisticOperations
from .user_core_service import UserCoreService, UserTypeDefaultsDocument

__all__ = [
    # Operation classes
    'UserAccountOperations',
    'SubscriptionManagementOperations',
    'IAMManagementOperations',
    'UserAuthOperations',
    'UserHolisticOperations',

    # Main orchestrating service
    'UserCoreService',

    # Supporting models
    'SubscriptionPlanDocument',
    'UserTypeDefaultsDocument'
]
