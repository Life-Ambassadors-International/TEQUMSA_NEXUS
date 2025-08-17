"""Feature gating utilities for TEQUMSA subscriptions."""
from functools import wraps
from typing import Callable, Any, Optional
from fastapi import HTTPException, status

from .models import ComputedEntitlements
from .entitlement_engine import EntitlementEngine


class FeatureGate:
    """Feature gating utility class."""
    
    def __init__(self, entitlement_engine: EntitlementEngine):
        """Initialize feature gate with entitlement engine."""
        self.engine = entitlement_engine
    
    def require_permission(self, permission: str):
        """Decorator to require a specific permission."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Extract entitlements from kwargs or context
                entitlements = kwargs.get('entitlements')
                if not entitlements:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )
                
                if not self.engine.check_permission(entitlements, permission):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permission required: {permission}"
                    )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def require_feature(self, feature: str, expected_value: Any = True):
        """Decorator to require a specific feature."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                entitlements = kwargs.get('entitlements')
                if not entitlements:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )
                
                feature_value = self.engine.check_feature(entitlements, feature)
                if feature_value != expected_value:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Feature not available: {feature}"
                    )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def check_limit(self, entitlements: ComputedEntitlements, limit: str, usage: int) -> bool:
        """Check if usage is within limit."""
        return self.engine.is_within_limit(entitlements, limit, usage)
    
    def enforce_limit(self, entitlements: ComputedEntitlements, limit: str, usage: int):
        """Enforce a usage limit, raising exception if exceeded."""
        if not self.check_limit(entitlements, limit, usage):
            limit_value = self.engine.check_limit(entitlements, limit)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {usage}/{limit_value} for {limit}"
            )


# Global feature gate instance
_gate = None


def get_feature_gate() -> FeatureGate:
    """Get the global feature gate instance."""
    global _gate
    if _gate is None:
        _gate = FeatureGate(EntitlementEngine())
    return _gate