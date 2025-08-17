"""Biome engine for TEQUMSA Level 100 metaverse."""
import yaml
import threading
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

from ..world.ecs_state import get_ecs_state, spawn_entity
from ..world.ecs_components import ComponentType, create_component
from ..world.patch_model import create_patch, ECStatePatch
from ..utils.time_series import record_metric
from .patch_queue import queue_patch


class BiomeDefinition:
    """Represents a biome definition loaded from YAML."""
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize biome definition from data."""
        self.biome_id = data['biome_id']
        self.name = data['name']
        self.description = data['description']
        self.environment = data.get('environment', {})
        self.lighting = data.get('lighting', {})
        self.physics = data.get('physics', {})
        self.consciousness_field = data.get('consciousness_field', {})
        self.spawnable_entities = data.get('spawnable_entities', [])
        self.biome_effects = data.get('biome_effects', [])
        self.access_requirements = data.get('access_requirements', {})
        self.transitions = data.get('transitions', [])
        self.resources = data.get('resources', [])
        self.weather_patterns = data.get('weather_patterns', [])
        self.natural_phenomena = data.get('natural_phenomena', [])
        self.metadata = data.get('metadata', {})
    
    def can_spawn_entity(self, entity_type: str, current_count: int) -> bool:
        """Check if entity can be spawned in this biome."""
        for spawnable in self.spawnable_entities:
            if spawnable['entity_type'] == entity_type:
                max_count = spawnable.get('max_count', float('inf'))
                return current_count < max_count
        return False
    
    def get_spawn_rate(self, entity_type: str) -> float:
        """Get spawn rate for entity type."""
        for spawnable in self.spawnable_entities:
            if spawnable['entity_type'] == entity_type:
                return spawnable.get('spawn_rate', 0.0)
        return 0.0
    
    def get_spawn_locations(self, entity_type: str) -> List[Dict[str, Any]]:
        """Get spawn locations for entity type."""
        for spawnable in self.spawnable_entities:
            if spawnable['entity_type'] == entity_type:
                return spawnable.get('spawn_locations', [])
        return []
    
    def check_access_requirements(self, user_entitlements: Dict[str, Any]) -> bool:
        """Check if user meets access requirements."""
        if not self.access_requirements:
            return True
        
        # Check tier requirement
        min_tier = self.access_requirements.get('min_tier')
        if min_tier and user_entitlements.get('tier') != min_tier:
            # Simple tier check - in reality would need tier hierarchy
            return False
        
        # Check permissions
        required_permissions = self.access_requirements.get('required_permissions', [])
        user_permissions = user_entitlements.get('permissions', [])
        
        for permission in required_permissions:
            if permission not in user_permissions:
                return False
        
        return True


class BiomeLoader:
    """Loads biome definitions from YAML files."""
    
    def __init__(self, biome_dir: Optional[str] = None):
        """Initialize biome loader."""
        if biome_dir is None:
            biome_dir = Path(__file__).parent.parent / "world" / "biome_defs"
        
        self.biome_dir = Path(biome_dir)
        self.biomes: Dict[str, BiomeDefinition] = {}
        self._lock = threading.RLock()
        self.load_biomes()
    
    def load_biomes(self):
        """Load all biome definitions from directory."""
        with self._lock:
            self.biomes.clear()
            
            if not self.biome_dir.exists():
                return
            
            for yaml_file in self.biome_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, 'r') as f:
                        data = yaml.safe_load(f)
                        biome = BiomeDefinition(data)
                        self.biomes[biome.biome_id] = biome
                except Exception as e:
                    print(f"Error loading biome {yaml_file}: {e}")
    
    def get_biome(self, biome_id: str) -> Optional[BiomeDefinition]:
        """Get biome definition by ID."""
        with self._lock:
            return self.biomes.get(biome_id)
    
    def list_biomes(self) -> List[str]:
        """List all biome IDs."""
        with self._lock:
            return list(self.biomes.keys())
    
    def reload(self):
        """Reload biome definitions."""
        self.load_biomes()


class BiomeEngine:
    """Engine for managing biome behaviors and entity spawning."""
    
    def __init__(self):
        """Initialize biome engine."""
        self.loader = BiomeLoader()
        self.ecs = get_ecs_state()
        self._active_biomes: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._last_update = datetime.utcnow()
    
    def activate_biome(self, biome_id: str, region_id: str) -> bool:
        """Activate a biome in a region."""
        biome = self.loader.get_biome(biome_id)
        if not biome:
            return False
        
        with self._lock:
            self._active_biomes[region_id] = {
                'biome_id': biome_id,
                'biome': biome,
                'activated_at': datetime.utcnow(),
                'last_spawn_check': datetime.utcnow(),
                'entity_counts': {},
                'active_effects': [],
                'weather_state': None,
                'resources': {}
            }
        
        # Initialize resources
        self._initialize_biome_resources(region_id, biome)
        
        record_metric(f"biome_activations", 1, {'biome_id': biome_id, 'region_id': region_id})
        return True
    
    def deactivate_biome(self, region_id: str) -> bool:
        """Deactivate biome in a region."""
        with self._lock:
            if region_id in self._active_biomes:
                del self._active_biomes[region_id]
                return True
            return False
    
    def update_biomes(self, delta_time: float):
        """Update all active biomes."""
        current_time = datetime.utcnow()
        
        with self._lock:
            for region_id, biome_state in self._active_biomes.items():
                self._update_biome(region_id, biome_state, delta_time, current_time)
        
        self._last_update = current_time
    
    def _update_biome(self, region_id: str, biome_state: Dict[str, Any], 
                     delta_time: float, current_time: datetime):
        """Update a single biome."""
        biome = biome_state['biome']
        
        # Update entity spawning
        self._update_entity_spawning(region_id, biome_state, delta_time)
        
        # Update weather patterns
        self._update_weather(region_id, biome_state, current_time)
        
        # Update resources
        self._update_resources(region_id, biome_state, delta_time)
        
        # Check for biome transitions
        self._check_biome_transitions(region_id, biome_state)
    
    def _update_entity_spawning(self, region_id: str, biome_state: Dict[str, Any], delta_time: float):
        """Update entity spawning for a biome."""
        biome = biome_state['biome']
        entity_counts = biome_state['entity_counts']
        
        for spawnable in biome.spawnable_entities:
            entity_type = spawnable['entity_type']
            spawn_rate = spawnable.get('spawn_rate', 0.0)  # per second
            max_count = spawnable.get('max_count', float('inf'))
            
            # Get current count
            current_count = entity_counts.get(entity_type, 0)
            actual_count = len(self.ecs.query_entities(
                entity_type=entity_type,
                region_id=region_id
            ))
            entity_counts[entity_type] = actual_count
            
            # Check if we should spawn
            if actual_count < max_count:
                spawn_probability = spawn_rate * delta_time
                if random.random() < spawn_probability:
                    self._spawn_biome_entity(region_id, entity_type, spawnable)
    
    def _spawn_biome_entity(self, region_id: str, entity_type: str, spawnable_config: Dict[str, Any]):
        """Spawn an entity in the biome."""
        try:
            # Create entity
            entity = spawn_entity(entity_type, region_id)
            
            # Add basic components based on spawn location
            spawn_locations = spawnable_config.get('spawn_locations', [])
            if spawn_locations:
                location_config = random.choice(spawn_locations)
                location_type = location_config.get('type', 'random_ground')
                
                # Generate position based on location type
                x, y, z = self._generate_spawn_position(location_type)
                
                transform = create_component(
                    ComponentType.TRANSFORM,
                    entity.entity_id,
                    x=x, y=y, z=z
                )
                self.ecs.add_component(entity.entity_id, transform)
            
            # Add consciousness component for consciousness-related entities
            if 'consciousness' in entity_type.lower():
                consciousness = create_component(
                    ComponentType.CONSCIOUSNESS,
                    entity.entity_id,
                    awareness_level=random.uniform(0.3, 0.8),
                    phi_score=random.uniform(1000, 10000)
                )
                self.ecs.add_component(entity.entity_id, consciousness)
            
            record_metric(f"entities_spawned_{entity_type}", 1, {
                'region_id': region_id,
                'entity_id': entity.entity_id
            })
            
        except Exception as e:
            print(f"Error spawning entity {entity_type} in {region_id}: {e}")
    
    def _generate_spawn_position(self, location_type: str) -> Tuple[float, float, float]:
        """Generate spawn position based on location type."""
        if location_type == "random_ground":
            return (
                random.uniform(-100, 100),
                0.0,
                random.uniform(-100, 100)
            )
        elif location_type == "hilltop":
            return (
                random.uniform(-50, 50),
                random.uniform(20, 50),
                random.uniform(-50, 50)
            )
        elif location_type == "crystal_formation":
            return (
                random.uniform(-20, 20),
                random.uniform(5, 15),
                random.uniform(-20, 20)
            )
        else:
            return (0.0, 0.0, 0.0)
    
    def _update_weather(self, region_id: str, biome_state: Dict[str, Any], current_time: datetime):
        """Update weather patterns for a biome."""
        # Simple weather system - could be much more complex
        if random.random() < 0.01:  # 1% chance per update
            biome = biome_state['biome']
            weather_patterns = biome.weather_patterns
            
            if weather_patterns:
                pattern = random.choice(weather_patterns)
                if random.random() < pattern.get('probability', 0.1):
                    biome_state['weather_state'] = {
                        'pattern': pattern,
                        'started_at': current_time,
                        'duration': random.randint(
                            pattern.get('duration_minutes', [30, 120])[0],
                            pattern.get('duration_minutes', [30, 120])[1]
                        )
                    }
    
    def _update_resources(self, region_id: str, biome_state: Dict[str, Any], delta_time: float):
        """Update resource generation for a biome."""
        biome = biome_state['biome']
        resources = biome_state['resources']
        
        for resource_config in biome.resources:
            resource_name = resource_config['name']
            generation_rate = resource_config.get('generation_rate', 0.0)  # per minute
            max_capacity = resource_config.get('max_capacity', 100)
            
            current_amount = resources.get(resource_name, 0)
            
            # Generate resources
            generated = generation_rate * (delta_time / 60.0)  # Convert to per-second
            new_amount = min(current_amount + generated, max_capacity)
            resources[resource_name] = new_amount
    
    def _check_biome_transitions(self, region_id: str, biome_state: Dict[str, Any]):
        """Check for possible biome transitions."""
        biome = biome_state['biome']
        
        for transition in biome.transitions:
            target_biome = transition['target_biome']
            conditions = transition.get('trigger_conditions', [])
            probability = transition.get('probability', 0.1)
            
            if self._check_transition_conditions(region_id, conditions):
                if random.random() < probability:
                    self._trigger_biome_transition(region_id, target_biome)
                    break
    
    def _check_transition_conditions(self, region_id: str, conditions: List[Dict[str, Any]]) -> bool:
        """Check if transition conditions are met."""
        for condition in conditions:
            condition_type = condition.get('type')
            
            if condition_type == 'consciousness_threshold':
                min_nodes = condition.get('min_nodes', 0)
                min_coherence = condition.get('min_coherence', 0.0)
                
                consciousness_entities = self.ecs.get_entities_with_component(ComponentType.CONSCIOUSNESS)
                region_consciousness = [
                    eid for eid in consciousness_entities
                    if self.ecs.get_entity(eid) and self.ecs.get_entity(eid).region_id == region_id
                ]
                
                if len(region_consciousness) < min_nodes:
                    return False
                
                # Check coherence (simplified)
                avg_coherence = 0.7  # Would calculate from actual consciousness components
                if avg_coherence < min_coherence:
                    return False
            
            # Add more condition types as needed
        
        return True
    
    def _trigger_biome_transition(self, region_id: str, new_biome_id: str):
        """Trigger a biome transition."""
        print(f"Transitioning region {region_id} to biome {new_biome_id}")
        
        # For now, just activate the new biome
        self.activate_biome(new_biome_id, region_id)
        
        record_metric("biome_transitions", 1, {
            'region_id': region_id,
            'new_biome': new_biome_id
        })
    
    def _initialize_biome_resources(self, region_id: str, biome: BiomeDefinition):
        """Initialize resources for a biome."""
        biome_state = self._active_biomes[region_id]
        
        for resource_config in biome.resources:
            resource_name = resource_config['name']
            # Start with some initial resources
            initial_amount = resource_config.get('max_capacity', 100) * 0.1
            biome_state['resources'][resource_name] = initial_amount
    
    def get_biome_state(self, region_id: str) -> Optional[Dict[str, Any]]:
        """Get current biome state for a region."""
        with self._lock:
            return self._active_biomes.get(region_id)
    
    def get_active_biomes(self) -> Dict[str, Dict[str, Any]]:
        """Get all active biome states."""
        with self._lock:
            return self._active_biomes.copy()


# Global biome engine instance
_biome_engine = None


def get_biome_engine() -> BiomeEngine:
    """Get the global biome engine instance."""
    global _biome_engine
    if _biome_engine is None:
        _biome_engine = BiomeEngine()
    return _biome_engine