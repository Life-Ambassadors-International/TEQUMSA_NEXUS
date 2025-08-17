"""Subscription API endpoints for TEQUMSA Level 100."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime

from .models import (
    UserSubscription, ComputedEntitlements, SubscriptionTier, AddonType
)
from .entitlement_engine import EntitlementEngine
from .db_layer_mock import get_mock_db, MockSubscriptionDB
from .gating import get_feature_gate, FeatureGate


router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


def get_entitlement_engine() -> EntitlementEngine:
    """Dependency to get entitlement engine."""
    return EntitlementEngine()


def get_db() -> MockSubscriptionDB:
    """Dependency to get database."""
    return get_mock_db()


@router.get("/{account_id}/entitlements", response_model=ComputedEntitlements)
async def get_entitlements(
    account_id: str,
    engine: EntitlementEngine = Depends(get_entitlement_engine),
    db: MockSubscriptionDB = Depends(get_db)
):
    """Get computed entitlements for an account."""
    subscription = db.get_subscription(account_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription not found for account: {account_id}"
        )
    
    entitlements = engine.compute_entitlements(subscription)
    return entitlements


@router.get("/{account_id}", response_model=UserSubscription)
async def get_subscription(
    account_id: str,
    db: MockSubscriptionDB = Depends(get_db)
):
    """Get subscription details for an account."""
    subscription = db.get_subscription(account_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription not found for account: {account_id}"
        )
    return subscription


@router.post("/", response_model=UserSubscription)
async def create_subscription(
    account_id: str,
    tier: SubscriptionTier,
    addons: Optional[List[AddonType]] = None,
    db: MockSubscriptionDB = Depends(get_db)
):
    """Create a new subscription."""
    existing = db.get_subscription(account_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Subscription already exists for account: {account_id}"
        )
    
    now = datetime.utcnow().isoformat()
    subscription = UserSubscription(
        account_id=account_id,
        tier=tier,
        addons=addons or [],
        custom_features={},
        created_at=now,
        updated_at=now
    )
    
    return db.create_subscription(subscription)


@router.put("/{account_id}", response_model=UserSubscription)
async def update_subscription(
    account_id: str,
    tier: Optional[SubscriptionTier] = None,
    addons: Optional[List[AddonType]] = None,
    custom_features: Optional[dict] = None,
    db: MockSubscriptionDB = Depends(get_db)
):
    """Update an existing subscription."""
    subscription = db.get_subscription(account_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription not found for account: {account_id}"
        )
    
    if tier is not None:
        subscription.tier = tier
    if addons is not None:
        subscription.addons = addons
    if custom_features is not None:
        subscription.custom_features = custom_features
    
    return db.update_subscription(subscription)


@router.delete("/{account_id}")
async def delete_subscription(
    account_id: str,
    db: MockSubscriptionDB = Depends(get_db)
):
    """Delete a subscription."""
    if not db.delete_subscription(account_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription not found for account: {account_id}"
        )
    return {"message": "Subscription deleted successfully"}


@router.get("/", response_model=List[UserSubscription])
async def list_subscriptions(
    tier: Optional[SubscriptionTier] = None,
    db: MockSubscriptionDB = Depends(get_db)
):
    """List all subscriptions, optionally filtered by tier."""
    return db.list_subscriptions(tier)


@router.get("/stats/tiers")
async def get_tier_stats(db: MockSubscriptionDB = Depends(get_db)):
    """Get subscription statistics by tier."""
    return db.get_subscription_count_by_tier()


@router.post("/{account_id}/check-permission")
async def check_permission(
    account_id: str,
    permission: str,
    engine: EntitlementEngine = Depends(get_entitlement_engine),
    db: MockSubscriptionDB = Depends(get_db)
):
    """Check if an account has a specific permission."""
    subscription = db.get_subscription(account_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription not found for account: {account_id}"
        )
    
    entitlements = engine.compute_entitlements(subscription)
    has_permission = engine.check_permission(entitlements, permission)
    
    return {
        "account_id": account_id,
        "permission": permission,
        "has_permission": has_permission
    }


@router.post("/{account_id}/check-limit")
async def check_limit(
    account_id: str,
    limit: str,
    current_usage: int,
    engine: EntitlementEngine = Depends(get_entitlement_engine),
    db: MockSubscriptionDB = Depends(get_db)
):
    """Check if current usage is within account limits."""
    subscription = db.get_subscription(account_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription not found for account: {account_id}"
        )
    
    entitlements = engine.compute_entitlements(subscription)
    limit_value = engine.check_limit(entitlements, limit)
    within_limit = engine.is_within_limit(entitlements, limit, current_usage)
    
    return {
        "account_id": account_id,
        "limit": limit,
        "limit_value": limit_value,
        "current_usage": current_usage,
        "within_limit": within_limit
    }