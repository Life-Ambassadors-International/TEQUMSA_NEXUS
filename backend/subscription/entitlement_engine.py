"""Entitlement computation engine for TEQUMSA subscriptions."""
from datetime import datetime
from typing import Dict, List, Any, Optional
from copy import deepcopy

from .models import (
    UserSubscription, ComputedEntitlements, SubscriptionTier, AddonType
)
from .loader import get_loader


class EntitlementEngine:
    """Computes user entitlements based on subscription tier and addons."""
    
    def __init__(self):
        """Initialize the entitlement engine."""
        self.loader = get_loader()
    
    def compute_entitlements(self, subscription: UserSubscription) -> ComputedEntitlements:
        """Compute entitlements for a user subscription."""
        # Start with base tier
        features = {}
        limits = {}
        permissions = []
        
        # Apply tier inheritance chain
        tier_chain = self._build_tier_chain(subscription.tier.value)
        for tier_id in tier_chain:
            tier_config = self.loader.get_tier_config(tier_id)
            if tier_config:
                features.update(tier_config.features)
                limits.update(tier_config.limits)
                permissions.extend(tier_config.permissions)
        
        # Apply addons
        for addon_type in subscription.addons:
            addon_config = self.loader.get_addon_config(addon_type.value)
            if addon_config:
                features.update(addon_config.features)
                # For limits, addons typically add to existing limits
                for key, value in addon_config.limits.items():
                    if key in limits:
                        if limits[key] == -1 or value == -1:
                            limits[key] = -1  # Unlimited stays unlimited
                        else:
                            limits[key] += value
                    else:
                        limits[key] = value
                permissions.extend(addon_config.permissions)
        
        # Apply custom features
        features.update(subscription.custom_features)
        
        # Remove duplicates from permissions
        permissions = list(set(permissions))
        
        return ComputedEntitlements(
            account_id=subscription.account_id,
            tier=subscription.tier,
            features=features,
            limits=limits,
            permissions=permissions,
            addons=subscription.addons,
            computed_at=datetime.utcnow().isoformat()
        )
    
    def _build_tier_chain(self, tier_id: str) -> List[str]:
        """Build inheritance chain for a tier."""
        chain = []
        current_tier = tier_id
        
        while current_tier:
            chain.insert(0, current_tier)  # Insert at beginning for correct order
            tier_config = self.loader.get_tier_config(current_tier)
            if tier_config and tier_config.inherits_from:
                current_tier = tier_config.inherits_from
            else:
                current_tier = None
        
        return chain
    
    def check_permission(self, entitlements: ComputedEntitlements, permission: str) -> bool:
        """Check if user has a specific permission."""
        return permission in entitlements.permissions
    
    def check_feature(self, entitlements: ComputedEntitlements, feature: str) -> Any:
        """Get feature value for user."""
        return entitlements.features.get(feature)
    
    def check_limit(self, entitlements: ComputedEntitlements, limit: str) -> int:
        """Get limit value for user."""
        return entitlements.limits.get(limit, 0)
    
    def is_within_limit(self, entitlements: ComputedEntitlements, limit: str, current_usage: int) -> bool:
        """Check if current usage is within limit."""
        limit_value = self.check_limit(entitlements, limit)
        if limit_value == -1:  # Unlimited
            return True
        return current_usage < limit_value