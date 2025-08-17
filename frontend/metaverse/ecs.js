/**
 * ECS client for TEQUMSA Level 100 entity management
 */
class ECSClient {
    constructor() {
        this.entities = new Map();
        this.components = new Map();
        this.systems = [];
        this.lastUpdate = Date.now();
    }
    
    // Entity management
    createEntity(entityType, regionId) {
        const entityId = `entity_${entityType}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        const entity = {
            id: entityId,
            type: entityType,
            regionId: regionId,
            components: new Set(),
            active: true,
            createdAt: Date.now()
        };
        
        this.entities.set(entityId, entity);
        
        console.log(`[ECSClient] Created entity: ${entityId} (${entityType})`);
        return entity;
    }
    
    destroyEntity(entityId) {
        const entity = this.entities.get(entityId);
        if (!entity) return false;
        
        // Remove all components
        entity.components.forEach(componentType => {
            this.removeComponent(entityId, componentType);
        });
        
        this.entities.delete(entityId);
        console.log(`[ECSClient] Destroyed entity: ${entityId}`);
        return true;
    }
    
    getEntity(entityId) {
        return this.entities.get(entityId);
    }
    
    // Component management
    addComponent(entityId, componentType, componentData) {
        const entity = this.entities.get(entityId);
        if (!entity) {
            console.error(`[ECSClient] Entity not found: ${entityId}`);
            return false;
        }
        
        const componentKey = `${entityId}_${componentType}`;
        
        const component = {
            entityId: entityId,
            type: componentType,
            data: componentData,
            createdAt: Date.now(),
            updatedAt: Date.now()
        };
        
        this.components.set(componentKey, component);
        entity.components.add(componentType);
        
        console.log(`[ECSClient] Added component ${componentType} to entity ${entityId}`);
        return true;
    }
    
    removeComponent(entityId, componentType) {
        const entity = this.entities.get(entityId);
        if (!entity) return false;
        
        const componentKey = `${entityId}_${componentType}`;
        
        this.components.delete(componentKey);
        entity.components.delete(componentType);
        
        console.log(`[ECSClient] Removed component ${componentType} from entity ${entityId}`);
        return true;
    }
    
    getComponent(entityId, componentType) {
        const componentKey = `${entityId}_${componentType}`;
        return this.components.get(componentKey);
    }
    
    updateComponent(entityId, componentType, newData) {
        const componentKey = `${entityId}_${componentType}`;
        const component = this.components.get(componentKey);
        
        if (!component) {
            console.error(`[ECSClient] Component not found: ${componentType} on entity ${entityId}`);
            return false;
        }
        
        component.data = { ...component.data, ...newData };
        component.updatedAt = Date.now();
        
        return true;
    }
    
    // Query methods
    getEntitiesWithComponent(componentType) {
        const entities = [];
        
        for (const [entityId, entity] of this.entities) {
            if (entity.components.has(componentType)) {
                entities.push(entity);
            }
        }
        
        return entities;
    }
    
    getEntitiesWithComponents(componentTypes) {
        const entities = [];
        
        for (const [entityId, entity] of this.entities) {
            const hasAllComponents = componentTypes.every(type => 
                entity.components.has(type)
            );
            
            if (hasAllComponents) {
                entities.push(entity);
            }
        }
        
        return entities;
    }
    
    getEntitiesByType(entityType) {
        const entities = [];
        
        for (const [entityId, entity] of this.entities) {
            if (entity.type === entityType) {
                entities.push(entity);
            }
        }
        
        return entities;
    }
    
    getEntitiesByRegion(regionId) {
        const entities = [];
        
        for (const [entityId, entity] of this.entities) {
            if (entity.regionId === regionId) {
                entities.push(entity);
            }
        }
        
        return entities;
    }
    
    // System management
    addSystem(system) {
        this.systems.push(system);
        console.log(`[ECSClient] Added system: ${system.name || 'unnamed'}`);
    }
    
    removeSystem(systemName) {
        const index = this.systems.findIndex(system => 
            system.name === systemName
        );
        
        if (index !== -1) {
            this.systems.splice(index, 1);
            console.log(`[ECSClient] Removed system: ${systemName}`);
            return true;
        }
        
        return false;
    }
    
    // Update loop
    update() {
        const now = Date.now();
        const deltaTime = (now - this.lastUpdate) / 1000; // Convert to seconds
        
        // Run all systems
        this.systems.forEach(system => {
            try {
                if (system.update && typeof system.update === 'function') {
                    system.update(deltaTime, this);
                }
            } catch (error) {
                console.error(`[ECSClient] Error in system ${system.name}:`, error);
            }
        });
        
        this.lastUpdate = now;
    }
    
    // Serialization
    serialize() {
        const entitiesData = [];
        
        for (const [entityId, entity] of this.entities) {
            const entityData = {
                id: entity.id,
                type: entity.type,
                regionId: entity.regionId,
                active: entity.active,
                components: {}
            };
            
            // Add all components
            entity.components.forEach(componentType => {
                const component = this.getComponent(entityId, componentType);
                if (component) {
                    entityData.components[componentType] = component.data;
                }
            });
            
            entitiesData.push(entityData);
        }
        
        return {
            entities: entitiesData,
            timestamp: Date.now()
        };
    }
    
    deserialize(data) {
        // Clear existing state
        this.entities.clear();
        this.components.clear();
        
        // Restore entities and components
        data.entities.forEach(entityData => {
            // Create entity
            const entity = {
                id: entityData.id,
                type: entityData.type,
                regionId: entityData.regionId,
                components: new Set(),
                active: entityData.active || true,
                createdAt: Date.now()
            };
            
            this.entities.set(entity.id, entity);
            
            // Add components
            Object.entries(entityData.components).forEach(([componentType, componentData]) => {
                this.addComponent(entity.id, componentType, componentData);
            });
        });
        
        console.log(`[ECSClient] Deserialized ${data.entities.length} entities`);
    }
    
    // Statistics
    getStats() {
        const componentCounts = {};
        const typeCounts = {};
        
        // Count components
        for (const component of this.components.values()) {
            componentCounts[component.type] = (componentCounts[component.type] || 0) + 1;
        }
        
        // Count entity types
        for (const entity of this.entities.values()) {
            typeCounts[entity.type] = (typeCounts[entity.type] || 0) + 1;
        }
        
        return {
            totalEntities: this.entities.size,
            totalComponents: this.components.size,
            totalSystems: this.systems.length,
            componentCounts,
            typeCounts
        };
    }
    
    // Sync with backend
    async syncWithBackend(regionId) {
        if (!window.NetClient || !window.NetClient.connected) {
            console.warn('[ECSClient] Cannot sync: not connected to backend');
            return false;
        }
        
        try {
            const worldState = await window.NetClient.getWorldState(regionId);
            
            if (worldState && worldState.entities) {
                // Update local state with backend data
                worldState.entities.forEach(entityData => {
                    const entity = entityData.entity;
                    const components = entityData.components;
                    
                    // Create or update entity
                    if (!this.entities.has(entity.entity_id)) {
                        this.createEntity(entity.entity_type, entity.region_id);
                        this.entities.get(entity.entity_id).id = entity.entity_id;
                    }
                    
                    // Update components
                    Object.entries(components).forEach(([componentType, componentData]) => {
                        this.addComponent(entity.entity_id, componentType, componentData);
                    });
                });
                
                console.log(`[ECSClient] Synced with backend: ${worldState.entity_count} entities`);
                return true;
            }
        } catch (error) {
            console.error('[ECSClient] Sync failed:', error);
        }
        
        return false;
    }
}

// Global instance
window.ECSClient = new ECSClient();

// Auto-sync when connected
document.addEventListener('DOMContentLoaded', () => {
    console.log('[ECSClient] Module loaded');
    
    // Start update loop
    setInterval(() => {
        window.ECSClient.update();
    }, 1000 / 60); // 60 FPS
});

// Example systems
const ConsciousnessSystem = {
    name: 'ConsciousnessSystem',
    update(deltaTime, ecs) {
        const consciousnessEntities = ecs.getEntitiesWithComponent('consciousness');
        
        consciousnessEntities.forEach(entity => {
            const consciousness = ecs.getComponent(entity.id, 'consciousness');
            if (consciousness) {
                // Update consciousness values
                const data = consciousness.data;
                data.phi_score += Math.random() * 10 - 5;
                data.awareness_level += (Math.random() - 0.5) * 0.01;
                data.awareness_level = Math.max(0, Math.min(1, data.awareness_level));
                
                ecs.updateComponent(entity.id, 'consciousness', data);
            }
        });
    }
};

// Add default systems
window.ECSClient.addSystem(ConsciousnessSystem);