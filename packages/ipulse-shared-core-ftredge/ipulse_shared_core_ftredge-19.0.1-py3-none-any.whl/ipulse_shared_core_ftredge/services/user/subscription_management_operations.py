"""
Subscription Management Operations - Handle user subscriptions and related operations
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from google.cloud import firestore
from pydantic import BaseModel

from ...models.subscription import Subscription
from ...exceptions import ResourceNotFoundError
from ..base import BaseFirestoreService
from ipulse_shared_base_ftredge.enums import SubscriptionPlan, SubscriptionStatus
from ...exceptions import SubscriptionError, UserStatusError


# Model for subscription plan data from Firestore
class SubscriptionPlanDocument(BaseModel):
    """Model for subscription plan documents stored in Firestore"""
    id: str
    plan_name: str
    plan_version: int
    display_name: str
    description: str
    default_iam_domain_permissions: Optional[Dict[str, Dict[str, List[str]]]] = None
    subscription_based_insight_credits_per_update: Optional[int] = None
    subscription_based_insight_credits_update_freq_h: Optional[int] = None
    extra_insight_credits_per_cycle: Optional[int] = None
    voting_credits_per_update: Optional[int] = None
    voting_credits_update_freq_h: Optional[int] = None
    plan_validity_cycle_length: Optional[int] = None
    plan_validity_cycle_unit: Optional[str] = None
    plan_per_cycle_price_usd: Optional[float] = None
    plan_auto_renewal: Optional[bool] = None
    fallback_plan_id_if_current_plan_expired: Optional[str] = None


class SubscriptionManagementOperations:
    """
    Handles subscription-related operations for users
    """

    def __init__(
        self,
        firestore_client: firestore.Client,
        user_account_ops,  # UserManagementOperations instance
        logger: Optional[logging.Logger] = None,
        timeout: float = 10.0,
        subscription_plans_collection: str = "papp_core_configs_subscriptionplans_defaults"
    ):
        self.db = firestore_client
        self.user_account_ops = user_account_ops
        self.logger = logger or logging.getLogger(__name__)
        self.timeout = timeout

        # Initialize subscription plans DB service
        self._subscription_plans_db_service = BaseFirestoreService[SubscriptionPlanDocument](
            db=self.db,
            collection_name=subscription_plans_collection,
            resource_type="SubscriptionPlan",
            logger=self.logger,
            timeout=self.timeout
        )

    async def fetch_subscription_plan_details(self, plan_id: str) -> Optional[SubscriptionPlanDocument]:
        """Fetch subscription plan details from Firestore"""
        try:
            plan_data_dict = await self._subscription_plans_db_service.get_document(plan_id)
            if not plan_data_dict:
                self.logger.warning(f"Subscription plan with ID '{plan_id}' not found")
                return None

            # Add the plan_id to the dict if it's not already there
            plan_data_dict.setdefault('id', plan_id)
            plan_doc = SubscriptionPlanDocument(**plan_data_dict)
            self.logger.info(f"Successfully fetched subscription plan details for plan_id: {plan_id}")
            return plan_doc

        except ResourceNotFoundError:
            self.logger.warning(f"Subscription plan '{plan_id}' not found")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching subscription plan details for {plan_id}: {e}", exc_info=True)
            raise SubscriptionError(
                detail=f"Failed to fetch subscription plan: {str(e)}",
                plan_id=plan_id,
                operation="fetch_subscription_plan_details",
                original_error=e
            )

    async def apply_subscription_plan(
        self,
        user_uid: str,
        plan_id: str,
        source: str = "system_default_config"
    ) -> Subscription:
        """Apply a subscription plan to a user"""
        user_status = await self.user_account_ops.get_userstatus(user_uid)
        if not user_status:
            raise UserStatusError(
                detail=f"UserStatus not found for user_uid {user_uid}",
                user_uid=user_uid,
                operation="apply_subscription_plan"
            )

        plan_doc = await self.fetch_subscription_plan_details(plan_id)
        if not plan_doc:
            raise SubscriptionError(
                detail=f"Subscription plan {plan_id} not found",
                user_uid=user_uid,
                plan_id=plan_id,
                operation="apply_subscription_plan"
            )

        # Validate plan data
        plan_name_str = plan_doc.plan_name
        if not plan_name_str:
            raise SubscriptionError(
                detail="Plan name missing in plan details",
                user_uid=user_uid,
                plan_id=plan_id,
                operation="apply_subscription_plan"
            )

        try:
            plan_name_enum = SubscriptionPlan(plan_name_str)
        except ValueError as e:
            raise SubscriptionError(
                detail=f"Invalid plan name '{plan_name_str}': {str(e)}",
                user_uid=user_uid,
                plan_id=plan_id,
                operation="apply_subscription_plan",
                original_error=e
            )

        # Validate required fields
        plan_version = plan_doc.plan_version
        validity_length = plan_doc.plan_validity_cycle_length
        validity_unit = plan_doc.plan_validity_cycle_unit

        if not all([
            plan_version is not None and isinstance(plan_version, int),
            validity_length is not None and isinstance(validity_length, int),
            validity_unit is not None and isinstance(validity_unit, str)
        ]):
            raise SubscriptionError(
                detail="Missing or invalid subscription duration fields",
                user_uid=user_uid,
                plan_id=plan_id,
                operation="apply_subscription_plan"
            )

        # Create subscription
        start_date = datetime.now(timezone.utc)
        # At this point, we know validity_length and validity_unit are not None
        # Type assertions to satisfy type checker
        assert validity_length is not None and validity_unit is not None
        end_date = Subscription.calculate_cycle_end_date(start_date, validity_length, validity_unit)

        try:
            new_subscription = Subscription(
                plan_name=plan_name_enum,
                plan_version=int(plan_version),
                plan_id=plan_id,
                cycle_start_date=start_date,
                cycle_end_date=end_date,
                validity_time_length=validity_length,  # We already validated it's not None
                validity_time_unit=validity_unit,      # We already validated it's not None
                auto_renew=plan_doc.plan_auto_renewal if plan_doc.plan_auto_renewal is not None else False,
                status=SubscriptionStatus.ACTIVE,
                default_iam_domain_permissions=plan_doc.default_iam_domain_permissions or {},
                fallback_plan_id=plan_doc.fallback_plan_id_if_current_plan_expired,
                price_paid_usd=float(plan_doc.plan_per_cycle_price_usd if plan_doc.plan_per_cycle_price_usd is not None else 0.0),
                created_by=source,
                updated_by=source,
                subscription_based_insight_credits_per_update=int(plan_doc.subscription_based_insight_credits_per_update if plan_doc.subscription_based_insight_credits_per_update is not None else 0),
                subscription_based_insight_credits_update_freq_h=int(plan_doc.subscription_based_insight_credits_update_freq_h if plan_doc.subscription_based_insight_credits_update_freq_h is not None else 24),
                extra_insight_credits_per_cycle=int(plan_doc.extra_insight_credits_per_cycle if plan_doc.extra_insight_credits_per_cycle is not None else 0),
                voting_credits_per_update=int(plan_doc.voting_credits_per_update if plan_doc.voting_credits_per_update is not None else 0),
                voting_credits_update_freq_h=int(plan_doc.voting_credits_update_freq_h if plan_doc.voting_credits_update_freq_h is not None else 744),
            )
        except Exception as e:
            raise SubscriptionError(
                detail=f"Failed to create subscription object: {str(e)}",
                user_uid=user_uid,
                plan_id=plan_id,
                operation="apply_subscription_plan",
                original_error=e
            )

        # Apply subscription to user status
        try:
            user_status.apply_subscription(new_subscription)
            user_status.updated_at = datetime.now(timezone.utc)
            user_status.updated_by = f"SubscriptionManagement.apply_plan:{source}"

            await self.user_account_ops.update_userstatus(
                user_uid=user_uid,
                status_data=user_status.model_dump(exclude_none=True),
                updater_uid=f"SubscriptionManagement:{source}"
            )

            self.logger.info(f"Successfully applied subscription plan {plan_id} for user {user_uid}")
            return new_subscription

        except Exception as e:
            self.logger.error(f"Failed to apply subscription to user status: {e}", exc_info=True)
            raise SubscriptionError(
                detail=f"Failed to apply subscription to user: {str(e)}",
                user_uid=user_uid,
                plan_id=plan_id,
                operation="apply_subscription_plan",
                original_error=e
            )

    async def get_user_active_subscription(self, user_uid: str) -> Optional[Subscription]:
        """Get the user's currently active subscription"""
        user_status = await self.user_account_ops.get_userstatus(user_uid)
        if user_status and user_status.active_subscription and user_status.active_subscription.is_active():
            self.logger.info(f"Active subscription found for user {user_uid}: {user_status.active_subscription.plan_id}")
            return user_status.active_subscription

        self.logger.info(f"No active subscription found for user {user_uid}")
        return None

    async def change_user_subscription(
        self,
        user_uid: str,
        new_plan_id: str,
        source: Optional[str] = None
    ) -> Optional[Subscription]:
        """Change a user's subscription to a new plan"""
        self.logger.info(f"Attempting to change subscription for user {user_uid} to plan {new_plan_id}")

        user_status = await self.user_account_ops.get_userstatus(user_uid)
        if not user_status:
            raise UserStatusError(
                detail=f"UserStatus not found for user_uid {user_uid}",
                user_uid=user_uid,
                operation="change_user_subscription"
            )

        effective_source = source or f"user_initiated_change_uid_{user_uid}"

        # Archive current subscription if exists
        if user_status.active_subscription:
            self.logger.info(f"Archiving current active subscription {user_status.active_subscription.plan_id} for user {user_uid}")
            old_subscription = user_status.active_subscription

            try:
                old_subscription_dict = old_subscription.model_dump()
                old_subscription_dict['status'] = SubscriptionStatus.INACTIVE
                old_subscription_dict['updated_at'] = datetime.now(timezone.utc)
                old_subscription_dict['updated_by'] = f"superseded_by_{new_plan_id}_via_{effective_source}"

                modified_old_subscription = Subscription(**old_subscription_dict)

                if user_status.subscriptions_history is None:
                    user_status.subscriptions_history = {}
                user_status.subscriptions_history[modified_old_subscription.uuid] = modified_old_subscription

            except Exception as e:
                self.logger.error(f"Failed to archive old subscription: {e}", exc_info=True)
                raise SubscriptionError(
                    detail=f"Failed to archive old subscription: {str(e)}",
                    user_uid=user_uid,
                    plan_id=new_plan_id,
                    operation="change_user_subscription",
                    original_error=e
                )

        # Apply new subscription
        try:
            new_subscription_obj = await self.apply_subscription_plan(user_uid, new_plan_id, source=effective_source)
            self.logger.info(f"Successfully changed subscription for user {user_uid} to {new_plan_id}")
            return new_subscription_obj
        except Exception as e:
            self.logger.error(f"Error changing subscription for user {user_uid} to {new_plan_id}: {e}", exc_info=True)
            raise

    async def cancel_user_subscription(
        self,
        user_uid: str,
        reason: Optional[str] = None,
        cancelled_by: Optional[str] = None
    ) -> bool:
        """Cancel a user's active subscription"""
        self.logger.info(f"Attempting to cancel subscription for user {user_uid}. Reason: {reason}")

        user_status = await self.user_account_ops.get_userstatus(user_uid)
        if not user_status:
            raise UserStatusError(
                detail=f"UserStatus not found for user_uid {user_uid}",
                user_uid=user_uid,
                operation="cancel_user_subscription"
            )

        effective_canceller = cancelled_by or f"SubscriptionManagement.cancel:{reason or 'not_specified'}"

        if user_status.active_subscription and user_status.active_subscription.status == SubscriptionStatus.ACTIVE:
            try:
                active_sub_dict = user_status.active_subscription.model_dump()

                self.logger.info(f"Cancelling active subscription {active_sub_dict['plan_id']} for user {user_uid}")

                active_sub_dict['status'] = SubscriptionStatus.CANCELLED
                active_sub_dict['auto_renew'] = False
                active_sub_dict['updated_at'] = datetime.now(timezone.utc)
                active_sub_dict['updated_by'] = effective_canceller

                cancelled_subscription = Subscription(**active_sub_dict)

                if user_status.subscriptions_history is None:
                    user_status.subscriptions_history = {}
                user_status.subscriptions_history[cancelled_subscription.uuid] = cancelled_subscription

                user_status.revoke_subscription()
                user_status.updated_at = datetime.now(timezone.utc)
                user_status.updated_by = effective_canceller

                await self.user_account_ops.update_userstatus(
                    user_uid=user_uid,
                    status_data=user_status.model_dump(exclude_none=True),
                    updater_uid=effective_canceller
                )

                self.logger.info(f"Successfully cancelled subscription for user {user_uid}")
                return True

            except Exception as e:
                self.logger.error(f"Failed to cancel subscription: {e}", exc_info=True)
                raise SubscriptionError(
                    detail=f"Failed to cancel subscription: {str(e)}",
                    user_uid=user_uid,
                    operation="cancel_user_subscription",
                    original_error=e
                )
        else:
            self.logger.info(f"No active subscription to cancel for user {user_uid}")
            return False

    async def get_subscription_history(self, user_uid: str) -> Dict[str, Subscription]:
        """Get the user's subscription history"""
        user_status = await self.user_account_ops.get_userstatus(user_uid)
        if user_status and user_status.subscriptions_history:
            return user_status.subscriptions_history
        return {}

    async def get_all_subscription_plans(self) -> List[SubscriptionPlanDocument]:
        """Get all available subscription plans"""
        try:
            # This would require implementing a list_documents method in BaseFirestoreService
            # For now, we'll implement a basic version
            collection_ref = self.db.collection(self._subscription_plans_db_service.collection_name)
            docs = collection_ref.stream()

            plans = []
            for doc in docs:
                plan_data = doc.to_dict()
                plan_data['id'] = doc.id
                try:
                    plan = SubscriptionPlanDocument(**plan_data)
                    plans.append(plan)
                except Exception as e:
                    self.logger.warning(f"Failed to parse subscription plan {doc.id}: {e}")
                    continue

            return plans

        except Exception as e:
            self.logger.error(f"Error fetching subscription plans: {e}", exc_info=True)
            raise SubscriptionError(
                detail=f"Failed to fetch subscription plans: {str(e)}",
                operation="get_all_subscription_plans",
                original_error=e
            )

    async def validate_subscription_plan(self, plan_id: str) -> bool:
        """Validate if a subscription plan exists and is valid"""
        try:
            plan = await self.fetch_subscription_plan_details(plan_id)
            return plan is not None
        except Exception:
            return False
