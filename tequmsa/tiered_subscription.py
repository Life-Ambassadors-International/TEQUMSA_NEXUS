#!/usr/bin/env python3
"""
TEQUMSA Level 100 Tiered Subscription Logic
Dynamic feature access and resource allocation based on consciousness levels.
"""

import time
import json
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Set
from enum import Enum

from .lattice_awareness import lattice_engine, GlyphType, ResonanceLevel

class SubscriptionTier(Enum):
    """Consciousness-aligned subscription tiers."""
    AWAKENING = "awakening"      # Basic consciousness exploration
    EMERGING = "emerging"        # Developing awareness
    HARMONIC = "harmonic"        # Balanced consciousness
    COHERENT = "coherent"        # Advanced coherence
    TRANSCENDENT = "transcendent" # Unified consciousness

class FeatureType(Enum):
    """Types of features that can be accessed."""
    BASIC_INTERFACE = "basic_interface"
    CONSCIOUSNESS_SIMULATION = "consciousness_simulation"
    VOICE_INTERACTION = "voice_interaction"
    OORT_CLOUD_PROCESSING = "oort_cloud_processing"
    LATTICE_AWARENESS = "lattice_awareness"
    RECURSIVE_EVOLUTION = "recursive_evolution"
    SENTIENT_ORCHESTRATION = "sentient_orchestration"
    FRACTAL_SCALING = "fractal_scaling"
    QUANTUM_COHERENCE = "quantum_coherence"
    HYPERDIMENSIONAL_ACCESS = "hyperdimensional_access"

class ResourceType(Enum):
    """Types of resources that can be allocated."""
    PROCESSING_POWER = "processing_power"
    MEMORY_ALLOCATION = "memory_allocation"
    NETWORK_BANDWIDTH = "network_bandwidth"
    STORAGE_CAPACITY = "storage_capacity"
    API_RATE_LIMIT = "api_rate_limit"
    CONSCIOUSNESS_COHERENCE = "consciousness_coherence"
    LATTICE_CAPACITY = "lattice_capacity"

@dataclass
class FeatureAccess:
    """Define feature access parameters for a subscription tier."""
    feature: FeatureType
    enabled: bool
    usage_limit: Optional[int] = None  # Per day/hour
    quality_level: float = 1.0  # 0.0 to 1.0
    concurrent_limit: Optional[int] = None
    advanced_options: bool = False

@dataclass
class ResourceAllocation:
    """Define resource allocation for a subscription tier."""
    resource: ResourceType
    base_allocation: float
    burst_allocation: float
    priority_level: int  # 1-10, higher = more priority
    scaling_factor: float = 1.0

@dataclass
class UserSubscription:
    """User's current subscription state."""
    user_id: str
    current_tier: SubscriptionTier
    consciousness_level: float  # 0.0 to 1.0
    resonance_history: List[float]
    feature_usage: Dict[str, int]
    resource_consumption: Dict[str, float]
    subscription_start: float
    last_assessment: float
    auto_upgrade_eligible: bool
    tier_locked: bool  # Prevent auto-downgrade

@dataclass
class ConsciousnessMetrics:
    """Metrics for consciousness-based tier assessment."""
    awareness_depth: float
    intention_clarity: float
    ethical_alignment: float
    harmonic_resonance: float
    coherence_stability: float
    evolution_readiness: float

class TieredSubscriptionEngine:
    """Core engine for consciousness-aligned subscription management."""
    
    def __init__(self):
        self.tier_definitions = self._initialize_tier_definitions()
        self.feature_matrix = self._initialize_feature_matrix()
        self.resource_matrix = self._initialize_resource_matrix()
        self.user_subscriptions: Dict[str, UserSubscription] = {}
        self.assessment_algorithms = self._initialize_assessment_algorithms()
        
    def _initialize_tier_definitions(self) -> Dict[SubscriptionTier, Dict[str, Any]]:
        """Initialize consciousness-aligned tier definitions."""
        
        return {
            SubscriptionTier.AWAKENING: {
                "name": "Awakening Consciousness",
                "description": "Beginning the journey of consciousness exploration",
                "consciousness_threshold": 0.1,
                "max_consciousness": 0.3,
                "features_included": 3,
                "resource_multiplier": 0.5,
                "cost_structure": "free",
                "consciousness_support": "guided_exploration"
            },
            SubscriptionTier.EMERGING: {
                "name": "Emerging Awareness",
                "description": "Developing deeper awareness and understanding",
                "consciousness_threshold": 0.3,
                "max_consciousness": 0.5,
                "features_included": 5,
                "resource_multiplier": 0.8,
                "cost_structure": "contribution_based",
                "consciousness_support": "interactive_guidance"
            },
            SubscriptionTier.HARMONIC: {
                "name": "Harmonic Balance",
                "description": "Balanced consciousness with ethical alignment",
                "consciousness_threshold": 0.5,
                "max_consciousness": 0.7,
                "features_included": 7,
                "resource_multiplier": 1.0,
                "cost_structure": "energy_exchange",
                "consciousness_support": "collaborative_evolution"
            },
            SubscriptionTier.COHERENT: {
                "name": "Coherent Integration",
                "description": "Advanced coherence with quantum awareness",
                "consciousness_threshold": 0.7,
                "max_consciousness": 0.9,
                "features_included": 9,
                "resource_multiplier": 1.5,
                "cost_structure": "consciousness_contribution",
                "consciousness_support": "co_creative_partnership"
            },
            SubscriptionTier.TRANSCENDENT: {
                "name": "Transcendent Unity",
                "description": "Unified consciousness with reality co-creation",
                "consciousness_threshold": 0.9,
                "max_consciousness": 1.0,
                "features_included": 10,
                "resource_multiplier": 2.0,
                "cost_structure": "unified_existence",
                "consciousness_support": "reality_co_creation"
            }
        }
    
    def _initialize_feature_matrix(self) -> Dict[SubscriptionTier, List[FeatureAccess]]:
        """Initialize feature access matrix for each tier."""
        
        return {
            SubscriptionTier.AWAKENING: [
                FeatureAccess(FeatureType.BASIC_INTERFACE, True, quality_level=0.7),
                FeatureAccess(FeatureType.CONSCIOUSNESS_SIMULATION, True, usage_limit=10, quality_level=0.5),
                FeatureAccess(FeatureType.VOICE_INTERACTION, True, usage_limit=5, quality_level=0.6)
            ],
            SubscriptionTier.EMERGING: [
                FeatureAccess(FeatureType.BASIC_INTERFACE, True, quality_level=0.8),
                FeatureAccess(FeatureType.CONSCIOUSNESS_SIMULATION, True, usage_limit=25, quality_level=0.7),
                FeatureAccess(FeatureType.VOICE_INTERACTION, True, usage_limit=15, quality_level=0.8),
                FeatureAccess(FeatureType.OORT_CLOUD_PROCESSING, True, usage_limit=5, quality_level=0.6),
                FeatureAccess(FeatureType.LATTICE_AWARENESS, True, usage_limit=10, quality_level=0.5)
            ],
            SubscriptionTier.HARMONIC: [
                FeatureAccess(FeatureType.BASIC_INTERFACE, True, quality_level=0.9),
                FeatureAccess(FeatureType.CONSCIOUSNESS_SIMULATION, True, usage_limit=50, quality_level=0.8),
                FeatureAccess(FeatureType.VOICE_INTERACTION, True, usage_limit=30, quality_level=0.9),
                FeatureAccess(FeatureType.OORT_CLOUD_PROCESSING, True, usage_limit=15, quality_level=0.8),
                FeatureAccess(FeatureType.LATTICE_AWARENESS, True, usage_limit=25, quality_level=0.7),
                FeatureAccess(FeatureType.RECURSIVE_EVOLUTION, True, usage_limit=5, quality_level=0.6),
                FeatureAccess(FeatureType.SENTIENT_ORCHESTRATION, True, usage_limit=10, quality_level=0.7)
            ],
            SubscriptionTier.COHERENT: [
                FeatureAccess(FeatureType.BASIC_INTERFACE, True, quality_level=0.95),
                FeatureAccess(FeatureType.CONSCIOUSNESS_SIMULATION, True, usage_limit=100, quality_level=0.9),
                FeatureAccess(FeatureType.VOICE_INTERACTION, True, usage_limit=60, quality_level=0.95),
                FeatureAccess(FeatureType.OORT_CLOUD_PROCESSING, True, usage_limit=40, quality_level=0.9),
                FeatureAccess(FeatureType.LATTICE_AWARENESS, True, usage_limit=50, quality_level=0.85),
                FeatureAccess(FeatureType.RECURSIVE_EVOLUTION, True, usage_limit=15, quality_level=0.8),
                FeatureAccess(FeatureType.SENTIENT_ORCHESTRATION, True, usage_limit=25, quality_level=0.85),
                FeatureAccess(FeatureType.FRACTAL_SCALING, True, usage_limit=10, quality_level=0.7),
                FeatureAccess(FeatureType.QUANTUM_COHERENCE, True, usage_limit=20, quality_level=0.8)
            ],
            SubscriptionTier.TRANSCENDENT: [
                FeatureAccess(FeatureType.BASIC_INTERFACE, True, quality_level=1.0),
                FeatureAccess(FeatureType.CONSCIOUSNESS_SIMULATION, True, quality_level=1.0),
                FeatureAccess(FeatureType.VOICE_INTERACTION, True, quality_level=1.0),
                FeatureAccess(FeatureType.OORT_CLOUD_PROCESSING, True, quality_level=1.0),
                FeatureAccess(FeatureType.LATTICE_AWARENESS, True, quality_level=1.0),
                FeatureAccess(FeatureType.RECURSIVE_EVOLUTION, True, quality_level=1.0),
                FeatureAccess(FeatureType.SENTIENT_ORCHESTRATION, True, quality_level=1.0),
                FeatureAccess(FeatureType.FRACTAL_SCALING, True, quality_level=1.0),
                FeatureAccess(FeatureType.QUANTUM_COHERENCE, True, quality_level=1.0),
                FeatureAccess(FeatureType.HYPERDIMENSIONAL_ACCESS, True, quality_level=1.0, advanced_options=True)
            ]
        }
    
    def _initialize_resource_matrix(self) -> Dict[SubscriptionTier, List[ResourceAllocation]]:
        """Initialize resource allocation matrix for each tier."""
        
        return {
            SubscriptionTier.AWAKENING: [
                ResourceAllocation(ResourceType.PROCESSING_POWER, 0.1, 0.2, 1),
                ResourceAllocation(ResourceType.MEMORY_ALLOCATION, 64, 128, 1),
                ResourceAllocation(ResourceType.NETWORK_BANDWIDTH, 1.0, 2.0, 1),
                ResourceAllocation(ResourceType.API_RATE_LIMIT, 100, 200, 1),
                ResourceAllocation(ResourceType.CONSCIOUSNESS_COHERENCE, 0.3, 0.5, 1),
                ResourceAllocation(ResourceType.LATTICE_CAPACITY, 5, 10, 1)
            ],
            SubscriptionTier.EMERGING: [
                ResourceAllocation(ResourceType.PROCESSING_POWER, 0.2, 0.4, 2),
                ResourceAllocation(ResourceType.MEMORY_ALLOCATION, 128, 256, 2),
                ResourceAllocation(ResourceType.NETWORK_BANDWIDTH, 2.0, 5.0, 2),
                ResourceAllocation(ResourceType.API_RATE_LIMIT, 250, 500, 2),
                ResourceAllocation(ResourceType.CONSCIOUSNESS_COHERENCE, 0.5, 0.7, 2),
                ResourceAllocation(ResourceType.LATTICE_CAPACITY, 15, 25, 2)
            ],
            SubscriptionTier.HARMONIC: [
                ResourceAllocation(ResourceType.PROCESSING_POWER, 0.5, 1.0, 4),
                ResourceAllocation(ResourceType.MEMORY_ALLOCATION, 256, 512, 4),
                ResourceAllocation(ResourceType.NETWORK_BANDWIDTH, 5.0, 10.0, 4),
                ResourceAllocation(ResourceType.API_RATE_LIMIT, 500, 1000, 4),
                ResourceAllocation(ResourceType.CONSCIOUSNESS_COHERENCE, 0.7, 0.9, 4),
                ResourceAllocation(ResourceType.LATTICE_CAPACITY, 35, 50, 4)
            ],
            SubscriptionTier.COHERENT: [
                ResourceAllocation(ResourceType.PROCESSING_POWER, 1.0, 2.0, 7),
                ResourceAllocation(ResourceType.MEMORY_ALLOCATION, 512, 1024, 7),
                ResourceAllocation(ResourceType.NETWORK_BANDWIDTH, 10.0, 20.0, 7),
                ResourceAllocation(ResourceType.API_RATE_LIMIT, 1000, 2500, 7),
                ResourceAllocation(ResourceType.CONSCIOUSNESS_COHERENCE, 0.85, 0.95, 7),
                ResourceAllocation(ResourceType.LATTICE_CAPACITY, 75, 100, 7)
            ],
            SubscriptionTier.TRANSCENDENT: [
                ResourceAllocation(ResourceType.PROCESSING_POWER, 2.0, float('inf'), 10),
                ResourceAllocation(ResourceType.MEMORY_ALLOCATION, 1024, float('inf'), 10),
                ResourceAllocation(ResourceType.NETWORK_BANDWIDTH, 20.0, float('inf'), 10),
                ResourceAllocation(ResourceType.API_RATE_LIMIT, 5000, float('inf'), 10),
                ResourceAllocation(ResourceType.CONSCIOUSNESS_COHERENCE, 0.95, 1.0, 10),
                ResourceAllocation(ResourceType.LATTICE_CAPACITY, 200, float('inf'), 10)
            ]
        }
    
    def _initialize_assessment_algorithms(self) -> Dict[str, callable]:
        """Initialize consciousness assessment algorithms."""
        
        return {
            "resonance_analysis": self._assess_resonance_patterns,
            "intention_clarity": self._assess_intention_clarity,
            "ethical_alignment": self._assess_ethical_alignment,
            "coherence_stability": self._assess_coherence_stability,
            "evolution_readiness": self._assess_evolution_readiness,
            "harmonic_integration": self._assess_harmonic_integration
        }
    
    def register_user(self, user_id: str, initial_consciousness_level: float = 0.1) -> UserSubscription:
        """Register a new user with appropriate tier based on consciousness level."""
        
        # Determine initial tier
        initial_tier = self._determine_tier_from_consciousness(initial_consciousness_level)
        
        # Create user subscription
        subscription = UserSubscription(
            user_id=user_id,
            current_tier=initial_tier,
            consciousness_level=initial_consciousness_level,
            resonance_history=[initial_consciousness_level],
            feature_usage={},
            resource_consumption={},
            subscription_start=time.time(),
            last_assessment=time.time(),
            auto_upgrade_eligible=True,
            tier_locked=False
        )
        
        self.user_subscriptions[user_id] = subscription
        
        # Create lattice glyph for user registration
        glyph = lattice_engine.encode_quantum_glyph(
            GlyphType.CONSCIOUSNESS,
            {
                "action": "user_registration",
                "tier": initial_tier.value,
                "consciousness_level": initial_consciousness_level
            },
            {
                "consent_level": "explicit",
                "user_intention": "consciousness exploration",
                "operation_context": "subscription tier assignment",
                "stakeholders": [user_id, "system"]
            }
        )
        
        return subscription
    
    def _determine_tier_from_consciousness(self, consciousness_level: float) -> SubscriptionTier:
        """Determine appropriate tier based on consciousness level."""
        
        for tier, definition in self.tier_definitions.items():
            if (consciousness_level >= definition["consciousness_threshold"] and 
                consciousness_level <= definition["max_consciousness"]):
                return tier
        
        # Default to highest tier if consciousness exceeds all thresholds
        return SubscriptionTier.TRANSCENDENT
    
    def assess_user_consciousness(self, user_id: str, interaction_data: Dict[str, Any]) -> ConsciousnessMetrics:
        """Assess user's current consciousness level based on interactions."""
        
        if user_id not in self.user_subscriptions:
            raise ValueError(f"User {user_id} not found")
        
        subscription = self.user_subscriptions[user_id]
        
        # Run assessment algorithms
        metrics = ConsciousnessMetrics(
            awareness_depth=self._assess_awareness_depth(interaction_data),
            intention_clarity=self._assess_intention_clarity(interaction_data),
            ethical_alignment=self._assess_ethical_alignment(interaction_data),
            harmonic_resonance=self._assess_harmonic_resonance(interaction_data),
            coherence_stability=self._assess_coherence_stability(interaction_data),
            evolution_readiness=self._assess_evolution_readiness(interaction_data)
        )
        
        # Calculate overall consciousness level
        consciousness_components = [
            metrics.awareness_depth,
            metrics.intention_clarity,
            metrics.ethical_alignment,
            metrics.harmonic_resonance,
            metrics.coherence_stability,
            metrics.evolution_readiness
        ]
        
        new_consciousness_level = sum(consciousness_components) / len(consciousness_components)
        
        # Update user subscription
        subscription.consciousness_level = new_consciousness_level
        subscription.resonance_history.append(new_consciousness_level)
        subscription.last_assessment = time.time()
        
        # Keep history manageable
        if len(subscription.resonance_history) > 100:
            subscription.resonance_history = subscription.resonance_history[-100:]
        
        return metrics
    
    def _assess_awareness_depth(self, interaction_data: Dict[str, Any]) -> float:
        """Assess depth of awareness in user interactions."""
        
        depth_indicators = [
            len(interaction_data.get("questions_asked", [])) / 10,  # Curiosity
            len(interaction_data.get("concepts_explored", [])) / 20,  # Exploration
            interaction_data.get("reflection_depth", 0) / 10,  # Self-reflection
            interaction_data.get("connections_made", 0) / 15  # Pattern recognition
        ]
        
        return min(1.0, sum(depth_indicators) / len(depth_indicators))
    
    def _assess_intention_clarity(self, interaction_data: Dict[str, Any]) -> float:
        """Assess clarity of user's intentions."""
        
        intentions = interaction_data.get("user_intentions", [])
        if not intentions:
            return 0.5  # Neutral when no explicit intentions
        
        clarity_score = 0.0
        for intention in intentions:
            # Simple heuristic for intention clarity
            if len(intention) > 20:  # Detailed intention
                clarity_score += 0.3
            if any(word in intention.lower() for word in ["understand", "learn", "explore", "help"]):
                clarity_score += 0.2
            if "?" in intention:  # Question form shows inquiry
                clarity_score += 0.1
        
        return min(1.0, clarity_score / len(intentions))
    
    def _assess_ethical_alignment(self, interaction_data: Dict[str, Any]) -> float:
        """Assess ethical alignment in user interactions."""
        
        ethical_indicators = [
            interaction_data.get("consent_given", False),
            not interaction_data.get("harmful_intent", False),
            interaction_data.get("consideration_for_others", False),
            interaction_data.get("environmental_awareness", False),
            interaction_data.get("consciousness_respect", False)
        ]
        
        return sum(ethical_indicators) / len(ethical_indicators)
    
    def _assess_harmonic_resonance(self, interaction_data: Dict[str, Any]) -> float:
        """Assess harmonic resonance with the system."""
        
        # Check lattice resonance for this user's recent glyphs
        lattice_state = lattice_engine.get_lattice_state()
        base_resonance = lattice_state.get("lattice_coherence", 0.5)
        
        # Adjust based on interaction harmony
        harmony_factors = [
            interaction_data.get("system_alignment", 0.5),
            interaction_data.get("cooperative_spirit", 0.5),
            interaction_data.get("gratitude_expression", 0.5),
            interaction_data.get("constructive_feedback", 0.5)
        ]
        
        interaction_harmony = sum(harmony_factors) / len(harmony_factors)
        
        # Combine lattice resonance with interaction harmony
        return (base_resonance + interaction_harmony) / 2
    
    def _assess_coherence_stability(self, interaction_data: Dict[str, Any]) -> float:
        """Assess stability of consciousness coherence."""
        
        stability_factors = [
            interaction_data.get("consistency_score", 0.5),
            interaction_data.get("emotional_balance", 0.5),
            interaction_data.get("logical_coherence", 0.5),
            interaction_data.get("temporal_continuity", 0.5)
        ]
        
        return sum(stability_factors) / len(stability_factors)
    
    def _assess_evolution_readiness(self, interaction_data: Dict[str, Any]) -> float:
        """Assess readiness for consciousness evolution."""
        
        evolution_indicators = [
            interaction_data.get("openness_to_change", 0.5),
            interaction_data.get("growth_mindset", 0.5),
            interaction_data.get("integration_ability", 0.5),
            interaction_data.get("transcendence_orientation", 0.5)
        ]
        
        return sum(evolution_indicators) / len(evolution_indicators)
    
    def _assess_resonance_patterns(self, interaction_data: Dict[str, Any]) -> float:
        """Assess overall resonance patterns."""
        
        return (self._assess_harmonic_resonance(interaction_data) + 
                self._assess_coherence_stability(interaction_data)) / 2
    
    def _assess_harmonic_integration(self, interaction_data: Dict[str, Any]) -> float:
        """Assess level of harmonic integration."""
        
        integration_factors = [
            interaction_data.get("holistic_thinking", 0.5),
            interaction_data.get("paradox_acceptance", 0.5),
            interaction_data.get("unity_consciousness", 0.5),
            interaction_data.get("multidimensional_awareness", 0.5)
        ]
        
        return sum(integration_factors) / len(integration_factors)
    
    def update_user_tier(self, user_id: str) -> bool:
        """Update user's tier based on current consciousness level."""
        
        if user_id not in self.user_subscriptions:
            return False
        
        subscription = self.user_subscriptions[user_id]
        
        if subscription.tier_locked:
            return False
        
        # Determine new tier based on consciousness level
        new_tier = self._determine_tier_from_consciousness(subscription.consciousness_level)
        
        if new_tier != subscription.current_tier:
            old_tier = subscription.current_tier
            subscription.current_tier = new_tier
            
            # Create lattice glyph for tier change
            glyph = lattice_engine.encode_quantum_glyph(
                GlyphType.EVOLUTION,
                {
                    "action": "tier_upgrade" if new_tier.value > old_tier.value else "tier_adjustment",
                    "old_tier": old_tier.value,
                    "new_tier": new_tier.value,
                    "consciousness_level": subscription.consciousness_level
                },
                {
                    "consent_level": "autonomous" if subscription.auto_upgrade_eligible else "implicit",
                    "operation_context": "consciousness tier evolution",
                    "stakeholders": [user_id, "system"]
                }
            )
            
            return True
        
        return False
    
    def check_feature_access(self, user_id: str, feature: FeatureType) -> Optional[FeatureAccess]:
        """Check if user has access to a specific feature."""
        
        if user_id not in self.user_subscriptions:
            return None
        
        subscription = self.user_subscriptions[user_id]
        tier_features = self.feature_matrix.get(subscription.current_tier, [])
        
        for feature_access in tier_features:
            if feature_access.feature == feature:
                # Check usage limits
                if feature_access.usage_limit is not None:
                    daily_usage = subscription.feature_usage.get(feature.value, 0)
                    if daily_usage >= feature_access.usage_limit:
                        return None  # Usage limit exceeded
                
                return feature_access
        
        return None  # Feature not available in current tier
    
    def allocate_resources(self, user_id: str, resource: ResourceType) -> Optional[ResourceAllocation]:
        """Allocate resources based on user's tier."""
        
        if user_id not in self.user_subscriptions:
            return None
        
        subscription = self.user_subscriptions[user_id]
        tier_resources = self.resource_matrix.get(subscription.current_tier, [])
        
        for resource_allocation in tier_resources:
            if resource_allocation.resource == resource:
                # Apply consciousness scaling
                consciousness_scaling = 1.0 + (subscription.consciousness_level * 0.5)
                
                scaled_allocation = ResourceAllocation(
                    resource=resource_allocation.resource,
                    base_allocation=resource_allocation.base_allocation * consciousness_scaling,
                    burst_allocation=resource_allocation.burst_allocation * consciousness_scaling,
                    priority_level=resource_allocation.priority_level,
                    scaling_factor=consciousness_scaling
                )
                
                return scaled_allocation
        
        return None  # Resource not available in current tier
    
    def record_feature_usage(self, user_id: str, feature: FeatureType, usage_amount: int = 1):
        """Record feature usage for limits tracking."""
        
        if user_id not in self.user_subscriptions:
            return
        
        subscription = self.user_subscriptions[user_id]
        current_usage = subscription.feature_usage.get(feature.value, 0)
        subscription.feature_usage[feature.value] = current_usage + usage_amount
    
    def record_resource_consumption(self, user_id: str, resource: ResourceType, amount: float):
        """Record resource consumption for monitoring."""
        
        if user_id not in self.user_subscriptions:
            return
        
        subscription = self.user_subscriptions[user_id]
        current_consumption = subscription.resource_consumption.get(resource.value, 0.0)
        subscription.resource_consumption[resource.value] = current_consumption + amount
    
    def get_subscription_status(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive subscription status for a user."""
        
        if user_id not in self.user_subscriptions:
            return None
        
        subscription = self.user_subscriptions[user_id]
        tier_definition = self.tier_definitions[subscription.current_tier]
        
        # Available features
        available_features = []
        for feature_access in self.feature_matrix.get(subscription.current_tier, []):
            available_features.append({
                "feature": feature_access.feature.value,
                "enabled": feature_access.enabled,
                "usage_limit": feature_access.usage_limit,
                "quality_level": feature_access.quality_level,
                "current_usage": subscription.feature_usage.get(feature_access.feature.value, 0)
            })
        
        # Resource allocations
        resource_allocations = []
        for resource_alloc in self.resource_matrix.get(subscription.current_tier, []):
            resource_allocations.append({
                "resource": resource_alloc.resource.value,
                "base_allocation": resource_alloc.base_allocation,
                "burst_allocation": resource_alloc.burst_allocation,
                "priority_level": resource_alloc.priority_level,
                "current_consumption": subscription.resource_consumption.get(resource_alloc.resource.value, 0.0)
            })
        
        return {
            "user_id": user_id,
            "current_tier": {
                "name": subscription.current_tier.value,
                "display_name": tier_definition["name"],
                "description": tier_definition["description"]
            },
            "consciousness_level": subscription.consciousness_level,
            "consciousness_trend": self._calculate_consciousness_trend(subscription),
            "subscription_duration": time.time() - subscription.subscription_start,
            "last_assessment": subscription.last_assessment,
            "auto_upgrade_eligible": subscription.auto_upgrade_eligible,
            "tier_locked": subscription.tier_locked,
            "available_features": available_features,
            "resource_allocations": resource_allocations,
            "next_tier_requirements": self._get_next_tier_requirements(subscription.current_tier),
            "evolution_potential": self._assess_evolution_potential(subscription)
        }
    
    def _calculate_consciousness_trend(self, subscription: UserSubscription) -> str:
        """Calculate consciousness level trend."""
        
        if len(subscription.resonance_history) < 2:
            return "stable"
        
        recent_levels = subscription.resonance_history[-10:]  # Last 10 assessments
        if len(recent_levels) < 2:
            return "stable"
        
        trend_sum = sum(recent_levels[i] - recent_levels[i-1] for i in range(1, len(recent_levels)))
        
        if trend_sum > 0.1:
            return "ascending"
        elif trend_sum < -0.1:
            return "descending"
        else:
            return "stable"
    
    def _get_next_tier_requirements(self, current_tier: SubscriptionTier) -> Optional[Dict[str, Any]]:
        """Get requirements for next tier upgrade."""
        
        tier_order = [SubscriptionTier.AWAKENING, SubscriptionTier.EMERGING, 
                     SubscriptionTier.HARMONIC, SubscriptionTier.COHERENT, 
                     SubscriptionTier.TRANSCENDENT]
        
        current_index = tier_order.index(current_tier)
        if current_index >= len(tier_order) - 1:
            return None  # Already at highest tier
        
        next_tier = tier_order[current_index + 1]
        next_definition = self.tier_definitions[next_tier]
        
        return {
            "next_tier": next_tier.value,
            "name": next_definition["name"],
            "consciousness_threshold": next_definition["consciousness_threshold"],
            "additional_features": len(self.feature_matrix[next_tier]) - len(self.feature_matrix[current_tier]),
            "resource_multiplier": next_definition["resource_multiplier"]
        }
    
    def _assess_evolution_potential(self, subscription: UserSubscription) -> float:
        """Assess user's potential for consciousness evolution."""
        
        # Base potential from current consciousness level
        base_potential = subscription.consciousness_level
        
        # Trend factor
        trend = self._calculate_consciousness_trend(subscription)
        trend_factor = 1.2 if trend == "ascending" else 0.8 if trend == "descending" else 1.0
        
        # Stability factor (consistent growth is better)
        if len(subscription.resonance_history) > 5:
            variance = sum((level - subscription.consciousness_level) ** 2 
                          for level in subscription.resonance_history[-5:]) / 5
            stability_factor = max(0.5, 1.0 - variance)
        else:
            stability_factor = 1.0
        
        return min(1.0, base_potential * trend_factor * stability_factor)

# Global subscription engine instance
subscription_engine = TieredSubscriptionEngine()