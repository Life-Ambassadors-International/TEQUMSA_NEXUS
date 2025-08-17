"""Mock database layer for subscription system."""
from typing import Dict, List, Optional
from datetime import datetime
import threading

from .models import UserSubscription, SubscriptionTier, AddonType


class MockSubscriptionDB:
    """In-memory mock database for subscription system."""
    
    def __init__(self):
        """Initialize mock database."""
        self._subscriptions: Dict[str, UserSubscription] = {}
        self._lock = threading.RLock()
        
        # Add some sample data
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize with sample subscription data."""
        now = datetime.utcnow().isoformat()
        
        # Sample free user
        self._subscriptions["user_free"] = UserSubscription(
            account_id="user_free",
            tier=SubscriptionTier.FREE,
            addons=[],
            custom_features={},
            created_at=now,
            updated_at=now
        )
        
        # Sample pro user with agent pack
        self._subscriptions["user_pro"] = UserSubscription(
            account_id="user_pro",
            tier=SubscriptionTier.PRO,
            addons=[AddonType.AGENT_PACK],
            custom_features={},
            created_at=now,
            updated_at=now
        )
        
        # Sample quantum user with all addons
        self._subscriptions["user_quantum"] = UserSubscription(
            account_id="user_quantum",
            tier=SubscriptionTier.QUANTUM,
            addons=[AddonType.AGENT_PACK, AddonType.SCRIPTING_PACK],
            custom_features={"beta_features": True},
            created_at=now,
            updated_at=now
        )
        
        # Sample enterprise user
        self._subscriptions["user_enterprise"] = UserSubscription(
            account_id="user_enterprise",
            tier=SubscriptionTier.ENTERPRISE_BASE,
            addons=[AddonType.AGENT_PACK, AddonType.SCRIPTING_PACK],
            custom_features={
                "dedicated_support": True,
                "custom_branding": True
            },
            created_at=now,
            updated_at=now
        )
    
    def get_subscription(self, account_id: str) -> Optional[UserSubscription]:
        """Get subscription by account ID."""
        with self._lock:
            return self._subscriptions.get(account_id)
    
    def create_subscription(self, subscription: UserSubscription) -> UserSubscription:
        """Create a new subscription."""
        with self._lock:
            self._subscriptions[subscription.account_id] = subscription
            return subscription
    
    def update_subscription(self, subscription: UserSubscription) -> UserSubscription:
        """Update an existing subscription."""
        with self._lock:
            subscription.updated_at = datetime.utcnow().isoformat()
            self._subscriptions[subscription.account_id] = subscription
            return subscription
    
    def delete_subscription(self, account_id: str) -> bool:
        """Delete a subscription."""
        with self._lock:
            if account_id in self._subscriptions:
                del self._subscriptions[account_id]
                return True
            return False
    
    def list_subscriptions(self, tier: Optional[SubscriptionTier] = None) -> List[UserSubscription]:
        """List all subscriptions, optionally filtered by tier."""
        with self._lock:
            subscriptions = list(self._subscriptions.values())
            if tier:
                subscriptions = [s for s in subscriptions if s.tier == tier]
            return subscriptions
    
    def get_subscription_count_by_tier(self) -> Dict[SubscriptionTier, int]:
        """Get count of subscriptions by tier."""
        with self._lock:
            counts = {}
            for subscription in self._subscriptions.values():
                counts[subscription.tier] = counts.get(subscription.tier, 0) + 1
            return counts


# Global mock database instance
_db = None


def get_mock_db() -> MockSubscriptionDB:
    """Get the global mock database instance."""
    global _db
    if _db is None:
        _db = MockSubscriptionDB()
    return _db