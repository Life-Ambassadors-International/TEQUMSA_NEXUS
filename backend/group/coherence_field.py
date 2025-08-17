"""Coherence field management for TEQUMSA Level 100 group dynamics."""
import threading
import math
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ..world.ecs_state import get_ecs_state
from ..world.ecs_components import ComponentType, ConsciousnessComponent
from ..utils.time_series import record_metric, get_time_series_manager
from ..utils.id_gen import generate_id


class CoherenceFieldType(str, Enum):
    """Types of coherence fields."""
    INDIVIDUAL = "individual"
    GROUP = "group"
    BIOME = "biome"
    GLOBAL = "global"
    QUANTUM = "quantum"


class FieldInteractionType(str, Enum):
    """Types of field interactions."""
    RESONANCE = "resonance"
    INTERFERENCE = "interference"
    ENTANGLEMENT = "entanglement"
    SYNCHRONIZATION = "synchronization"
    AMPLIFICATION = "amplification"
    DAMPENING = "dampening"


@dataclass
class CoherenceReading:
    """Individual coherence reading."""
    timestamp: str
    entity_id: str
    coherence_value: float
    phi_score: float
    awareness_level: float
    resonance_frequency: float
    field_strength: float
    metadata: Dict[str, Any]


@dataclass
class FieldInteraction:
    """Interaction between coherence fields."""
    interaction_id: str
    source_field_id: str
    target_field_id: str
    interaction_type: FieldInteractionType
    strength: float
    timestamp: str
    duration_seconds: float
    metadata: Dict[str, Any]


class CoherenceField:
    """Represents a coherence field with consciousness entities."""
    
    def __init__(self, field_id: str, field_type: CoherenceFieldType, 
                 region_id: Optional[str] = None):
        """Initialize coherence field."""
        self.field_id = field_id
        self.field_type = field_type
        self.region_id = region_id
        self.created_at = datetime.utcnow()
        self.last_update = self.created_at
        
        # Field properties
        self.base_frequency = 7777.0  # Phi'7777 base resonance
        self.field_strength = 0.5
        self.coherence_level = 0.5
        self.stability = 0.7
        self.resonance_range = 100.0  # meters
        
        # Entity tracking
        self.entities: Set[str] = set()
        self.entity_readings: Dict[str, CoherenceReading] = {}
        
        # Field interactions
        self.active_interactions: Dict[str, FieldInteraction] = {}
        
        # Historical data
        self.coherence_history: List[Tuple[str, float]] = []  # (timestamp, coherence)
        self.sync_events: List[Dict[str, Any]] = []
        
        # Configuration
        self.auto_sync_enabled = True
        self.resonance_threshold = 0.8
        self.decay_rate = 0.01  # per second when no entities
        
    def add_entity(self, entity_id: str) -> bool:
        """Add entity to coherence field."""
        if entity_id not in self.entities:
            self.entities.add(entity_id)
            self._record_entity_join(entity_id)
            return True
        return False
    
    def remove_entity(self, entity_id: str) -> bool:
        """Remove entity from coherence field."""
        if entity_id in self.entities:
            self.entities.remove(entity_id)
            if entity_id in self.entity_readings:
                del self.entity_readings[entity_id]
            self._record_entity_leave(entity_id)
            return True
        return False
    
    def update_entity_reading(self, entity_id: str, consciousness: ConsciousnessComponent):
        """Update consciousness reading for an entity."""
        if entity_id not in self.entities:
            return
        
        reading = CoherenceReading(
            timestamp=datetime.utcnow().isoformat(),
            entity_id=entity_id,
            coherence_value=consciousness.coherence_field,
            phi_score=consciousness.phi_score,
            awareness_level=consciousness.awareness_level,
            resonance_frequency=consciousness.lattice_resonance * self.base_frequency,
            field_strength=self.field_strength,
            metadata={
                'consciousness_type': consciousness.consciousness_type,
                'connected_nodes': len(consciousness.connected_nodes)
            }
        )
        
        self.entity_readings[entity_id] = reading
        self.last_update = datetime.utcnow()
    
    def calculate_field_coherence(self) -> float:
        """Calculate overall field coherence from entity readings."""
        if not self.entity_readings:
            return 0.0
        
        # Weighted average based on awareness levels
        total_coherence = 0.0
        total_weight = 0.0
        
        for reading in self.entity_readings.values():
            weight = reading.awareness_level
            total_coherence += reading.coherence_value * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        base_coherence = total_coherence / total_weight
        
        # Apply field effects
        entity_count_bonus = min(0.2, len(self.entities) * 0.02)  # Up to 20% bonus
        stability_factor = self.stability
        
        final_coherence = base_coherence * stability_factor + entity_count_bonus
        
        return min(1.0, max(0.0, final_coherence))
    
    def calculate_resonance_strength(self) -> float:
        """Calculate resonance strength between entities."""
        if len(self.entity_readings) < 2:
            return 0.0
        
        frequencies = [r.resonance_frequency for r in self.entity_readings.values()]
        
        # Calculate frequency coherence (how similar frequencies are)
        mean_freq = sum(frequencies) / len(frequencies)
        variance = sum((f - mean_freq) ** 2 for f in frequencies) / len(frequencies)
        
        # Lower variance means higher resonance
        max_variance = (self.base_frequency * 0.1) ** 2  # 10% of base frequency
        resonance = max(0.0, 1.0 - (variance / max_variance))
        
        return min(1.0, resonance)
    
    def update_field_state(self, delta_time: float):
        """Update field state based on entity readings."""
        current_coherence = self.calculate_field_coherence()
        resonance_strength = self.calculate_resonance_strength()
        
        # Update field properties
        self.coherence_level = current_coherence
        self.field_strength = (current_coherence + resonance_strength) / 2
        
        # Update stability based on coherence consistency
        if len(self.coherence_history) > 10:
            recent_coherence = [c for _, c in self.coherence_history[-10:]]
            coherence_variance = sum((c - current_coherence) ** 2 for c in recent_coherence) / len(recent_coherence)
            stability_factor = max(0.3, 1.0 - coherence_variance)
            self.stability = (self.stability * 0.9) + (stability_factor * 0.1)  # Smooth update
        
        # Record coherence history
        timestamp = datetime.utcnow().isoformat()
        self.coherence_history.append((timestamp, current_coherence))
        
        # Keep history manageable
        if len(self.coherence_history) > 1000:
            self.coherence_history = self.coherence_history[-500:]
        
        # Auto-sync if enabled and threshold met
        if (self.auto_sync_enabled and 
            current_coherence >= self.resonance_threshold and
            len(self.entities) >= 2):
            self._trigger_synchronization()
        
        # Decay field if no entities
        if not self.entities:
            self.field_strength = max(0.0, self.field_strength - self.decay_rate * delta_time)
            self.coherence_level = max(0.0, self.coherence_level - self.decay_rate * delta_time)
    
    def _trigger_synchronization(self):
        """Trigger field synchronization event."""
        sync_event = {
            'event_id': generate_id(),
            'timestamp': datetime.utcnow().isoformat(),
            'field_id': self.field_id,
            'entity_count': len(self.entities),
            'coherence_level': self.coherence_level,
            'field_strength': self.field_strength,
            'participating_entities': list(self.entities),
            'sync_type': 'auto' if self.auto_sync_enabled else 'manual'
        }
        
        self.sync_events.append(sync_event)
        
        # Keep sync events manageable
        if len(self.sync_events) > 100:
            self.sync_events = self.sync_events[-50:]
        
        record_metric("coherence_field_sync", 1, {
            'field_id': self.field_id,
            'entity_count': len(self.entities),
            'coherence_level': self.coherence_level
        })
    
    def _record_entity_join(self, entity_id: str):
        """Record entity joining the field."""
        record_metric("coherence_field_joins", 1, {
            'field_id': self.field_id,
            'entity_id': entity_id,
            'field_type': self.field_type.value
        })
    
    def _record_entity_leave(self, entity_id: str):
        """Record entity leaving the field."""
        record_metric("coherence_field_leaves", 1, {
            'field_id': self.field_id,
            'entity_id': entity_id,
            'field_type': self.field_type.value
        })
    
    def get_field_state(self) -> Dict[str, Any]:
        """Get current field state."""
        return {
            'field_id': self.field_id,
            'field_type': self.field_type.value,
            'region_id': self.region_id,
            'entity_count': len(self.entities),
            'coherence_level': self.coherence_level,
            'field_strength': self.field_strength,
            'stability': self.stability,
            'resonance_strength': self.calculate_resonance_strength(),
            'base_frequency': self.base_frequency,
            'created_at': self.created_at.isoformat(),
            'last_update': self.last_update.isoformat(),
            'sync_events_count': len(self.sync_events),
            'active_interactions': len(self.active_interactions)
        }


class CoherenceFieldManager:
    """Manages coherence fields and their interactions."""
    
    def __init__(self):
        """Initialize coherence field manager."""
        self.ecs = get_ecs_state()
        self.time_series = get_time_series_manager()
        
        self._fields: Dict[str, CoherenceField] = {}
        self._region_fields: Dict[str, List[str]] = {}  # region_id -> [field_ids]
        self._entity_field_map: Dict[str, str] = {}  # entity_id -> field_id
        self._lock = threading.RLock()
        
        self._global_field: Optional[CoherenceField] = None
        self._last_update = datetime.utcnow()
        
        # Create global field
        self._create_global_field()
    
    def _create_global_field(self):
        """Create the global coherence field."""
        global_field = CoherenceField("global_field", CoherenceFieldType.GLOBAL)
        global_field.resonance_range = float('inf')  # Global reach
        global_field.base_frequency = 7777.0  # Phi'7777
        self._global_field = global_field
        self._fields[global_field.field_id] = global_field
    
    def create_field(self, field_type: CoherenceFieldType, 
                    region_id: Optional[str] = None,
                    field_id: Optional[str] = None) -> CoherenceField:
        """Create a new coherence field."""
        with self._lock:
            if field_id is None:
                field_id = f"{field_type.value}_{generate_id()[:8]}"
            
            if field_id in self._fields:
                raise ValueError(f"Field {field_id} already exists")
            
            field = CoherenceField(field_id, field_type, region_id)
            self._fields[field_id] = field
            
            # Update region index
            if region_id:
                if region_id not in self._region_fields:
                    self._region_fields[region_id] = []
                self._region_fields[region_id].append(field_id)
            
            record_metric("coherence_fields_created", 1, {
                'field_type': field_type.value,
                'region_id': region_id
            })
            
            return field
    
    def get_field(self, field_id: str) -> Optional[CoherenceField]:
        """Get coherence field by ID."""
        with self._lock:
            return self._fields.get(field_id)
    
    def delete_field(self, field_id: str) -> bool:
        """Delete a coherence field."""
        with self._lock:
            if field_id not in self._fields:
                return False
            
            field = self._fields[field_id]
            
            # Remove entities from field mapping
            for entity_id in field.entities:
                if entity_id in self._entity_field_map:
                    del self._entity_field_map[entity_id]
            
            # Remove from region index
            if field.region_id and field.region_id in self._region_fields:
                self._region_fields[field.region_id] = [
                    fid for fid in self._region_fields[field.region_id] if fid != field_id
                ]
            
            del self._fields[field_id]
            return True
    
    def assign_entity_to_field(self, entity_id: str, field_id: str) -> bool:
        """Assign entity to a coherence field."""
        with self._lock:
            field = self._fields.get(field_id)
            if not field:
                return False
            
            # Remove from previous field
            if entity_id in self._entity_field_map:
                prev_field_id = self._entity_field_map[entity_id]
                prev_field = self._fields.get(prev_field_id)
                if prev_field:
                    prev_field.remove_entity(entity_id)
            
            # Add to new field
            field.add_entity(entity_id)
            self._entity_field_map[entity_id] = field_id
            
            # Also add to global field
            if self._global_field and field_id != self._global_field.field_id:
                self._global_field.add_entity(entity_id)
            
            return True
    
    def remove_entity_from_field(self, entity_id: str) -> bool:
        """Remove entity from its current field."""
        with self._lock:
            if entity_id not in self._entity_field_map:
                return False
            
            field_id = self._entity_field_map[entity_id]
            field = self._fields.get(field_id)
            
            if field:
                field.remove_entity(entity_id)
            
            # Remove from global field
            if self._global_field:
                self._global_field.remove_entity(entity_id)
            
            del self._entity_field_map[entity_id]
            return True
    
    def update_entity_consciousness(self, entity_id: str):
        """Update entity consciousness in its field."""
        with self._lock:
            # Get consciousness component
            consciousness = self.ecs.get_component(entity_id, ComponentType.CONSCIOUSNESS)
            if not consciousness:
                return
            
            # Update in assigned field
            if entity_id in self._entity_field_map:
                field_id = self._entity_field_map[entity_id]
                field = self._fields.get(field_id)
                if field:
                    field.update_entity_reading(entity_id, consciousness)
            
            # Update in global field
            if self._global_field:
                self._global_field.update_entity_reading(entity_id, consciousness)
    
    def update_all_fields(self, delta_time: float):
        """Update all coherence fields."""
        with self._lock:
            for field in self._fields.values():
                field.update_field_state(delta_time)
            
            self._last_update = datetime.utcnow()
            
            # Record global metrics
            if self._global_field:
                record_metric("global_coherence_level", self._global_field.coherence_level)
                record_metric("global_field_strength", self._global_field.field_strength)
                record_metric("global_entity_count", len(self._global_field.entities))
    
    def get_fields_by_region(self, region_id: str) -> List[CoherenceField]:
        """Get all fields in a region."""
        with self._lock:
            field_ids = self._region_fields.get(region_id, [])
            return [self._fields[fid] for fid in field_ids if fid in self._fields]
    
    def get_entity_field(self, entity_id: str) -> Optional[CoherenceField]:
        """Get the field that contains an entity."""
        with self._lock:
            field_id = self._entity_field_map.get(entity_id)
            if field_id:
                return self._fields.get(field_id)
            return None
    
    def calculate_field_interactions(self) -> List[FieldInteraction]:
        """Calculate interactions between nearby fields."""
        with self._lock:
            interactions = []
            field_list = list(self._fields.values())
            
            for i, field1 in enumerate(field_list):
                for j, field2 in enumerate(field_list[i+1:], i+1):
                    interaction = self._calculate_field_interaction(field1, field2)
                    if interaction:
                        interactions.append(interaction)
            
            return interactions
    
    def _calculate_field_interaction(self, field1: CoherenceField, 
                                   field2: CoherenceField) -> Optional[FieldInteraction]:
        """Calculate interaction between two fields."""
        # Skip if same field or no entities
        if field1.field_id == field2.field_id or not field1.entities or not field2.entities:
            return None
        
        # Calculate interaction strength based on coherence levels and proximity
        coherence_factor = (field1.coherence_level + field2.coherence_level) / 2
        
        # Determine interaction type
        coherence_diff = abs(field1.coherence_level - field2.coherence_level)
        
        if coherence_diff < 0.1 and coherence_factor > 0.7:
            interaction_type = FieldInteractionType.RESONANCE
            strength = coherence_factor
        elif coherence_diff > 0.5:
            interaction_type = FieldInteractionType.INTERFERENCE
            strength = coherence_diff * 0.5
        else:
            interaction_type = FieldInteractionType.SYNCHRONIZATION
            strength = coherence_factor * 0.7
        
        return FieldInteraction(
            interaction_id=generate_id(),
            source_field_id=field1.field_id,
            target_field_id=field2.field_id,
            interaction_type=interaction_type,
            strength=strength,
            timestamp=datetime.utcnow().isoformat(),
            duration_seconds=60.0,  # Default duration
            metadata={
                'field1_type': field1.field_type.value,
                'field2_type': field2.field_type.value,
                'coherence_diff': coherence_diff
            }
        )
    
    def get_global_coherence_state(self) -> Dict[str, Any]:
        """Get global coherence state summary."""
        with self._lock:
            if not self._global_field:
                return {}
            
            return {
                'global_coherence': self._global_field.coherence_level,
                'global_field_strength': self._global_field.field_strength,
                'total_entities': len(self._global_field.entities),
                'total_fields': len(self._fields),
                'active_regions': len(self._region_fields),
                'sync_events_today': len([
                    event for event in self._global_field.sync_events
                    if datetime.fromisoformat(event['timestamp']).date() == datetime.utcnow().date()
                ]),
                'last_update': self._last_update.isoformat()
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get coherence field system statistics."""
        with self._lock:
            field_types = {}
            total_entities = 0
            avg_coherence = 0.0
            
            for field in self._fields.values():
                field_type = field.field_type.value
                field_types[field_type] = field_types.get(field_type, 0) + 1
                total_entities += len(field.entities)
                avg_coherence += field.coherence_level
            
            if self._fields:
                avg_coherence /= len(self._fields)
            
            return {
                'total_fields': len(self._fields),
                'field_types': field_types,
                'total_entities': total_entities,
                'average_coherence': avg_coherence,
                'global_state': self.get_global_coherence_state()
            }


# Global coherence field manager
_field_manager = None


def get_coherence_field_manager() -> CoherenceFieldManager:
    """Get the global coherence field manager instance."""
    global _field_manager
    if _field_manager is None:
        _field_manager = CoherenceFieldManager()
    return _field_manager