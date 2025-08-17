"""ECS state management for TEQUMSA Level 100 metaverse."""
from typing import Dict, List, Set, Optional, Any, Tuple
from datetime import datetime
import threading
from collections import defaultdict

from .ecs_components import Component, ComponentType, create_component, deserialize_component
from ..utils.id_gen import generate_entity_id
from ..utils.time_series import record_metric


class Entity:
    """ECS entity representation."""
    
    def __init__(self, entity_id: str, entity_type: str, region_id: Optional[str] = None):
        """Initialize entity."""
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.region_id = region_id
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = self.created_at
        self.active = True
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'region_id': self.region_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'active': self.active,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entity':
        """Create entity from dictionary."""
        entity = cls(
            entity_id=data['entity_id'],
            entity_type=data['entity_type'],
            region_id=data.get('region_id')
        )
        entity.created_at = data['created_at']
        entity.updated_at = data['updated_at']
        entity.active = data.get('active', True)
        entity.metadata = data.get('metadata', {})
        return entity


class ECSState:
    """Entity-Component-System state manager."""
    
    def __init__(self):
        """Initialize ECS state."""
        self._entities: Dict[str, Entity] = {}
        self._components: Dict[str, Dict[ComponentType, Component]] = defaultdict(dict)
        self._component_index: Dict[ComponentType, Set[str]] = defaultdict(set)
        self._region_entities: Dict[str, Set[str]] = defaultdict(set)
        self._type_entities: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.RLock()
    
    def create_entity(self, entity_type: str, region_id: Optional[str] = None, 
                     entity_id: Optional[str] = None) -> Entity:
        """Create a new entity."""
        with self._lock:
            if entity_id is None:
                entity_id = generate_entity_id(entity_type, region_id)
            
            if entity_id in self._entities:
                raise ValueError(f"Entity {entity_id} already exists")
            
            entity = Entity(entity_id, entity_type, region_id)
            self._entities[entity_id] = entity
            
            # Update indices
            self._type_entities[entity_type].add(entity_id)
            if region_id:
                self._region_entities[region_id].add(entity_id)
            
            # Record metrics
            record_metric("entities_total", len(self._entities))
            record_metric(f"entities_{entity_type}", len(self._type_entities[entity_type]))
            
            return entity
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID."""
        with self._lock:
            return self._entities.get(entity_id)
    
    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity and all its components."""
        with self._lock:
            entity = self._entities.get(entity_id)
            if not entity:
                return False
            
            # Remove from indices
            self._type_entities[entity.entity_type].discard(entity_id)
            if entity.region_id:
                self._region_entities[entity.region_id].discard(entity_id)
            
            # Remove all components
            for component_type in list(self._components[entity_id].keys()):
                self.remove_component(entity_id, component_type)
            
            # Remove entity
            del self._entities[entity_id]
            
            # Record metrics
            record_metric("entities_total", len(self._entities))
            
            return True
    
    def add_component(self, entity_id: str, component: Component) -> bool:
        """Add component to entity."""
        with self._lock:
            if entity_id not in self._entities:
                raise ValueError(f"Entity {entity_id} does not exist")
            
            component.entity_id = entity_id
            component.updated_at = datetime.utcnow().isoformat()
            
            self._components[entity_id][component.component_type] = component
            self._component_index[component.component_type].add(entity_id)
            
            # Update entity timestamp
            self._entities[entity_id].updated_at = component.updated_at
            
            return True
    
    def get_component(self, entity_id: str, component_type: ComponentType) -> Optional[Component]:
        """Get component from entity."""
        with self._lock:
            return self._components[entity_id].get(component_type)
    
    def remove_component(self, entity_id: str, component_type: ComponentType) -> bool:
        """Remove component from entity."""
        with self._lock:
            if entity_id not in self._components:
                return False
            
            if component_type in self._components[entity_id]:
                del self._components[entity_id][component_type]
                self._component_index[component_type].discard(entity_id)
                
                # Update entity timestamp
                if entity_id in self._entities:
                    self._entities[entity_id].updated_at = datetime.utcnow().isoformat()
                
                return True
            
            return False
    
    def get_entities_with_component(self, component_type: ComponentType) -> List[str]:
        """Get all entities that have a specific component type."""
        with self._lock:
            return list(self._component_index[component_type])
    
    def get_entities_with_components(self, component_types: List[ComponentType]) -> List[str]:
        """Get entities that have all specified component types."""
        with self._lock:
            if not component_types:
                return []
            
            # Start with entities that have the first component type
            entity_sets = [self._component_index[ct] for ct in component_types]
            
            # Find intersection of all sets
            result = entity_sets[0]
            for entity_set in entity_sets[1:]:
                result = result.intersection(entity_set)
            
            return list(result)
    
    def get_entities_by_type(self, entity_type: str) -> List[str]:
        """Get entities by type."""
        with self._lock:
            return list(self._type_entities[entity_type])
    
    def get_entities_by_region(self, region_id: str) -> List[str]:
        """Get entities by region."""
        with self._lock:
            return list(self._region_entities[region_id])
    
    def get_entity_components(self, entity_id: str) -> Dict[ComponentType, Component]:
        """Get all components for an entity."""
        with self._lock:
            return self._components[entity_id].copy()
    
    def query_entities(self, 
                      entity_type: Optional[str] = None,
                      region_id: Optional[str] = None,
                      component_types: Optional[List[ComponentType]] = None,
                      active_only: bool = True) -> List[str]:
        """Query entities with multiple filters."""
        with self._lock:
            # Start with all entities
            candidates = set(self._entities.keys())
            
            # Filter by type
            if entity_type:
                candidates = candidates.intersection(self._type_entities[entity_type])
            
            # Filter by region
            if region_id:
                candidates = candidates.intersection(self._region_entities[region_id])
            
            # Filter by components
            if component_types:
                for component_type in component_types:
                    candidates = candidates.intersection(self._component_index[component_type])
            
            # Filter by active status
            if active_only:
                candidates = {eid for eid in candidates if self._entities[eid].active}
            
            return list(candidates)
    
    def get_world_state(self, region_id: Optional[str] = None) -> Dict[str, Any]:
        """Get current world state."""
        with self._lock:
            if region_id:
                entity_ids = self.get_entities_by_region(region_id)
            else:
                entity_ids = list(self._entities.keys())
            
            entities_data = []
            for entity_id in entity_ids:
                entity = self._entities[entity_id]
                components = {}
                
                for component_type, component in self._components[entity_id].items():
                    components[component_type.value] = component.serialize()
                
                entities_data.append({
                    'entity': entity.to_dict(),
                    'components': components
                })
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'region_id': region_id,
                'entity_count': len(entity_ids),
                'entities': entities_data
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get ECS statistics."""
        with self._lock:
            component_counts = {
                ct.value: len(entities) 
                for ct, entities in self._component_index.items()
            }
            
            type_counts = {
                entity_type: len(entities)
                for entity_type, entities in self._type_entities.items()
            }
            
            region_counts = {
                region_id: len(entities)
                for region_id, entities in self._region_entities.items()
            }
            
            return {
                'total_entities': len(self._entities),
                'entities_by_type': type_counts,
                'entities_by_region': region_counts,
                'components_by_type': component_counts,
                'timestamp': datetime.utcnow().isoformat()
            }


# Global ECS state instance
_ecs_state = None


def get_ecs_state() -> ECSState:
    """Get the global ECS state instance."""
    global _ecs_state
    if _ecs_state is None:
        _ecs_state = ECSState()
    return _ecs_state


# Convenience functions
def spawn_entity(entity_type: str, region_id: Optional[str] = None, 
                components: Optional[List[Component]] = None) -> Entity:
    """Spawn an entity with optional components."""
    ecs = get_ecs_state()
    entity = ecs.create_entity(entity_type, region_id)
    
    if components:
        for component in components:
            ecs.add_component(entity.entity_id, component)
    
    return entity


def despawn_entity(entity_id: str) -> bool:
    """Despawn an entity."""
    ecs = get_ecs_state()
    return ecs.delete_entity(entity_id)