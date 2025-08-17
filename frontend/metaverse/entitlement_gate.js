/**
 * Entitlement gating for TEQUMSA Level 100 subscription features
 */
class EntitlementGate {
    constructor() {
        this.userEntitlements = null;
        this.accountId = 'demo_user'; // In real app, would get from auth
        this.init();
    }
    
    init() {
        this.loadUserEntitlements();
    }
    
    async loadUserEntitlements() {
        try {
            if (window.NetClient && window.NetClient.connected) {
                this.userEntitlements = await window.NetClient.getEntitlements(this.accountId);
                console.log('[EntitlementGate] User entitlements loaded:', this.userEntitlements);
            } else {
                // Fallback for demo
                this.userEntitlements = {
                    tier: 'free',
                    permissions: ['read_public_lattice', 'basic_interaction'],
                    features: {
                        lattice_introspection: true,
                        awareness_log_viewport: 'limited',
                        basic_world_access: true
                    },
                    limits: {
                        api_calls_per_hour: 100,
                        concurrent_sessions: 1,
                        world_regions: 3
                    }
                };
                console.log('[EntitlementGate] Using demo entitlements');
            }
        } catch (error) {
            console.error('[EntitlementGate] Failed to load entitlements:', error);
            // Use minimal fallback
            this.userEntitlements = {
                tier: 'free',
                permissions: ['basic_interaction'],
                features: { basic_world_access: true },
                limits: { world_regions: 1 }
            };
        }
    }
    
    hasPermission(permission) {
        if (!this.userEntitlements) {
            console.warn('[EntitlementGate] Entitlements not loaded');
            return false;
        }
        
        return this.userEntitlements.permissions.includes(permission);
    }
    
    hasFeature(feature, expectedValue = true) {
        if (!this.userEntitlements) {
            console.warn('[EntitlementGate] Entitlements not loaded');
            return false;
        }
        
        const featureValue = this.userEntitlements.features[feature];
        
        if (expectedValue === true) {
            return featureValue === true;
        }
        
        return featureValue === expectedValue;
    }
    
    checkLimit(limitName, currentUsage) {
        if (!this.userEntitlements) {
            console.warn('[EntitlementGate] Entitlements not loaded');
            return false;
        }
        
        const limitValue = this.userEntitlements.limits[limitName];
        
        if (limitValue === -1) {
            return true; // Unlimited
        }
        
        return currentUsage < limitValue;
    }
    
    getTierName() {
        return this.userEntitlements ? this.userEntitlements.tier : 'unknown';
    }
    
    getTierLevel() {
        const tiers = {
            'free': 1,
            'pro': 2,
            'quantum': 3,
            'enterprise_base': 4,
            'enterprise_custom_template': 5
        };
        
        return tiers[this.getTierName()] || 0;
    }
    
    async checkBiomeAccess(biomeId) {
        // Define biome access requirements
        const biomeRequirements = {
            'peaceful_meadow': {
                minTier: 1,
                permissions: ['basic_interaction']
            },
            'mystic_forest': {
                minTier: 2,
                permissions: ['analyze_integrations']
            },
            'quantum_garden': {
                minTier: 3,
                permissions: ['access_quantum_fields']
            },
            'crystal_caverns': {
                minTier: 3,
                permissions: ['access_quantum_fields']
            },
            'oort_cloud_nexus': {
                minTier: 4,
                permissions: ['inject_policies', 'dedicated_resources']
            }
        };
        
        const requirements = biomeRequirements[biomeId];
        if (!requirements) {
            console.warn(`[EntitlementGate] Unknown biome: ${biomeId}`);
            return false;
        }
        
        // Check tier level
        const userTierLevel = this.getTierLevel();
        if (userTierLevel < requirements.minTier) {
            console.log(`[EntitlementGate] Biome ${biomeId} requires tier level ${requirements.minTier}, user has ${userTierLevel}`);
            return false;
        }
        
        // Check permissions
        for (const permission of requirements.permissions) {
            if (!this.hasPermission(permission)) {
                console.log(`[EntitlementGate] Biome ${biomeId} requires permission: ${permission}`);
                return false;
            }
        }
        
        return true;
    }
    
    async checkFeatureAccess(featureName) {
        const featureRequirements = {
            'consciousness_analysis': {
                permissions: ['analyze_integrations'],
                features: ['consciousness_field_access']
            },
            'agent_interaction': {
                permissions: ['basic_interaction'],
                features: ['agent_interaction_enabled']
            },
            'quantum_entanglement': {
                permissions: ['access_quantum_fields'],
                features: ['quantum_entanglement_access']
            },
            'reality_modification': {
                permissions: ['modulate_ethical_frames'],
                features: ['reality_modification_access']
            },
            'custom_scripting': {
                permissions: ['execute_scripts'],
                features: ['scripting_interface']
            }
        };
        
        const requirements = featureRequirements[featureName];
        if (!requirements) {
            console.warn(`[EntitlementGate] Unknown feature: ${featureName}`);
            return false;
        }
        
        // Check permissions
        if (requirements.permissions) {
            for (const permission of requirements.permissions) {
                if (!this.hasPermission(permission)) {
                    return false;
                }
            }
        }
        
        // Check features
        if (requirements.features) {
            for (const feature of requirements.features) {
                if (!this.hasFeature(feature)) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    showUpgradePrompt(feature, requiredTier = 'pro') {
        const tierNames = {
            'pro': 'Professional',
            'quantum': 'Quantum',
            'enterprise_base': 'Enterprise',
            'enterprise_custom_template': 'Enterprise Custom'
        };
        
        const tierName = tierNames[requiredTier] || requiredTier;
        
        const message = `
            🔒 This feature requires a ${tierName} subscription.
            
            Feature: ${feature}
            Your current tier: ${this.getTierName().toUpperCase()}
            Required tier: ${tierName.toUpperCase()}
            
            Would you like to learn more about upgrading?
        `;
        
        const upgrade = confirm(message);
        
        if (upgrade) {
            this.openUpgradeFlow(requiredTier);
        }
        
        return false;
    }
    
    openUpgradeFlow(targetTier) {
        if (window.logMessage) {
            window.logMessage(`Opening upgrade flow for ${targetTier} tier`, 'info');
        }
        
        // In a real app, this would open the subscription upgrade flow
        alert(`Upgrade flow would open here for ${targetTier} tier subscription.`);
    }
    
    applyGating(element, feature, requiredTier = null) {
        if (!element) return;
        
        const hasAccess = this.checkFeatureAccess(feature);
        
        if (!hasAccess) {
            element.disabled = true;
            element.style.opacity = '0.5';
            element.style.cursor = 'not-allowed';
            
            element.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.showUpgradePrompt(feature, requiredTier);
            });
            
            // Add tooltip
            element.title = `This feature requires a higher subscription tier`;
        }
    }
    
    setupGating() {
        // Apply gating to elements with data-feature attributes
        document.querySelectorAll('[data-feature]').forEach(element => {
            const feature = element.dataset.feature;
            const requiredTier = element.dataset.requiredTier;
            this.applyGating(element, feature, requiredTier);
        });
        
        // Apply gating to biome selection
        document.querySelectorAll('[data-biome]').forEach(element => {
            const biomeId = element.dataset.biome;
            
            this.checkBiomeAccess(biomeId).then(hasAccess => {
                if (!hasAccess) {
                    element.style.opacity = '0.5';
                    element.style.cursor = 'not-allowed';
                    
                    element.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        this.showUpgradePrompt(`Access to ${biomeId}`, 'pro');
                    });
                    
                    element.title = 'This biome requires a higher subscription tier';
                }
            });
        });
    }
    
    refreshEntitlements() {
        return this.loadUserEntitlements().then(() => {
            this.setupGating();
        });
    }
    
    // Utility methods for UI
    formatTierName(tier) {
        const tierNames = {
            'free': 'Free Explorer',
            'pro': 'Professional Seeker',
            'quantum': 'Quantum Navigator',
            'enterprise_base': 'Enterprise Guardian',
            'enterprise_custom_template': 'Sovereign Entity'
        };
        
        return tierNames[tier] || tier;
    }
    
    getTierColor(tier) {
        const tierColors = {
            'free': '#4CAF50',
            'pro': '#2196F3',
            'quantum': '#9C27B0',
            'enterprise_base': '#FF9800',
            'enterprise_custom_template': '#F44336'
        };
        
        return tierColors[tier] || '#666666';
    }
    
    getTierBenefits(tier) {
        const benefits = {
            'free': [
                'Basic world access',
                'Limited consciousness analysis',
                'Peaceful Meadow biome'
            ],
            'pro': [
                'Enhanced world access',
                'Advanced consciousness tools',
                'Multiple biome access',
                'Agent interactions'
            ],
            'quantum': [
                'Quantum field access',
                'Reality modification tools',
                'Advanced biomes',
                'Custom scripting'
            ],
            'enterprise_base': [
                'Full system access',
                'Policy injection',
                'Dedicated resources',
                'Custom integrations'
            ],
            'enterprise_custom_template': [
                'Unlimited access',
                'Sovereign control',
                'Custom everything',
                'Priority support'
            ]
        };
        
        return benefits[tier] || [];
    }
}

// Global instance
window.EntitlementGate = new EntitlementGate();

// Setup gating when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('[EntitlementGate] Module loaded');
    
    // Setup gating after a short delay to ensure other modules are loaded
    setTimeout(() => {
        window.EntitlementGate.setupGating();
    }, 1000);
});

// Refresh entitlements when network client connects
document.addEventListener('networkConnected', () => {
    window.EntitlementGate.refreshEntitlements();
});