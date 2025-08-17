"""Subscription tier and addon models for TEQUMSA Level 100."""
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class SubscriptionTier(str, Enum):
    """Subscription tier enumeration."""
    FREE = "free"
    PRO = "pro"
    QUANTUM = "quantum"
    ENTERPRISE_BASE = "enterprise_base"
    ENTERPRISE_CUSTOM_TEMPLATE = "enterprise_custom_template"


class AddonType(str, Enum):
    """Addon type enumeration."""
    AGENT_PACK = "agent_pack"
    SCRIPTING_PACK = "scripting_pack"


class TierConfig(BaseModel):
    """Configuration for a subscription tier."""
    name: str
    inherits_from: Optional[str] = None
    features: Dict[str, Any] = Field(default_factory=dict)
    limits: Dict[str, int] = Field(default_factory=dict)
    permissions: List[str] = Field(default_factory=list)


class AddonConfig(BaseModel):
    """Configuration for an addon."""
    name: str
    type: AddonType
    features: Dict[str, Any] = Field(default_factory=dict)
    limits: Dict[str, int] = Field(default_factory=dict)
    permissions: List[str] = Field(default_factory=list)


class UserSubscription(BaseModel):
    """User subscription model."""
    account_id: str
    tier: SubscriptionTier
    addons: List[AddonType] = Field(default_factory=list)
    custom_features: Dict[str, Any] = Field(default_factory=dict)
    expires_at: Optional[str] = None
    created_at: str
    updated_at: str


class ComputedEntitlements(BaseModel):
    """Computed entitlements for a user."""
    account_id: str
    tier: SubscriptionTier
    features: Dict[str, Any] = Field(default_factory=dict)
    limits: Dict[str, int] = Field(default_factory=dict)
    permissions: List[str] = Field(default_factory=list)
    addons: List[AddonType] = Field(default_factory=list)
    computed_at: str