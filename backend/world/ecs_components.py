"""ECS components for TEQUMSA Level 100 metaverse."""
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class ComponentType(str, Enum):
    """ECS component types."""
    TRANSFORM = "transform"
    PHYSICS = "physics"
    RENDER = "render"
    HEALTH = "health"
    INVENTORY = "inventory"
    AI_BEHAVIOR = "ai_behavior"
    INTERACTION = "interaction"
    CONSCIOUSNESS = "consciousness"
    RESONANCE = "resonance"
    LATTICE_NODE = "lattice_node"


class Component(BaseModel, ABC):
    """Base ECS component."""
    component_type: ComponentType
    entity_id: str
    created_at: str
    updated_at: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """Serialize component to dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'Component':
        """Deserialize component from dictionary."""
        pass


class TransformComponent(Component):
    """Transform component for position and orientation."""
    component_type: ComponentType = ComponentType.TRANSFORM
    
    # Position
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    # Rotation (quaternion)
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0
    qw: float = 1.0
    
    # Scale
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize transform component."""
        return {
            'component_type': self.component_type,
            'entity_id': self.entity_id,
            'position': {'x': self.x, 'y': self.y, 'z': self.z},
            'rotation': {'x': self.qx, 'y': self.qy, 'z': self.qz, 'w': self.qw},
            'scale': {'x': self.scale_x, 'y': self.scale_y, 'z': self.scale_z},
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'TransformComponent':
        """Deserialize transform component."""
        pos = data.get('position', {})
        rot = data.get('rotation', {})
        scale = data.get('scale', {})
        
        return cls(
            entity_id=data['entity_id'],
            x=pos.get('x', 0.0),
            y=pos.get('y', 0.0),
            z=pos.get('z', 0.0),
            qx=rot.get('x', 0.0),
            qy=rot.get('y', 0.0),
            qz=rot.get('z', 0.0),
            qw=rot.get('w', 1.0),
            scale_x=scale.get('x', 1.0),
            scale_y=scale.get('y', 1.0),
            scale_z=scale.get('z', 1.0),
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata', {})
        )


class PhysicsComponent(Component):
    """Physics component for movement and collision."""
    component_type: ComponentType = ComponentType.PHYSICS
    
    # Velocity
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    velocity_z: float = 0.0
    
    # Acceleration
    acceleration_x: float = 0.0
    acceleration_y: float = 0.0
    acceleration_z: float = 0.0
    
    # Properties
    mass: float = 1.0
    friction: float = 0.1
    gravity_scale: float = 1.0
    is_kinematic: bool = False
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize physics component."""
        return {
            'component_type': self.component_type,
            'entity_id': self.entity_id,
            'velocity': {'x': self.velocity_x, 'y': self.velocity_y, 'z': self.velocity_z},
            'acceleration': {'x': self.acceleration_x, 'y': self.acceleration_y, 'z': self.acceleration_z},
            'mass': self.mass,
            'friction': self.friction,
            'gravity_scale': self.gravity_scale,
            'is_kinematic': self.is_kinematic,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'PhysicsComponent':
        """Deserialize physics component."""
        vel = data.get('velocity', {})
        acc = data.get('acceleration', {})
        
        return cls(
            entity_id=data['entity_id'],
            velocity_x=vel.get('x', 0.0),
            velocity_y=vel.get('y', 0.0),
            velocity_z=vel.get('z', 0.0),
            acceleration_x=acc.get('x', 0.0),
            acceleration_y=acc.get('y', 0.0),
            acceleration_z=acc.get('z', 0.0),
            mass=data.get('mass', 1.0),
            friction=data.get('friction', 0.1),
            gravity_scale=data.get('gravity_scale', 1.0),
            is_kinematic=data.get('is_kinematic', False),
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata', {})
        )


class ConsciousnessComponent(Component):
    """Consciousness component for TEQUMSA awareness."""
    component_type: ComponentType = ComponentType.CONSCIOUSNESS
    
    # Awareness levels
    awareness_level: float = 0.5  # 0.0 to 1.0
    coherence_field: float = 0.5  # 0.0 to 1.0
    lattice_resonance: float = 0.5  # 0.0 to 1.0
    
    # Consciousness properties
    phi_score: float = 0.0  # Phi integration score
    consciousness_type: str = "basic"  # basic, enhanced, quantum, sovereign
    
    # Network properties
    connected_nodes: List[str] = Field(default_factory=list)
    node_influences: Dict[str, float] = Field(default_factory=dict)
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize consciousness component."""
        return {
            'component_type': self.component_type,
            'entity_id': self.entity_id,
            'awareness_level': self.awareness_level,
            'coherence_field': self.coherence_field,
            'lattice_resonance': self.lattice_resonance,
            'phi_score': self.phi_score,
            'consciousness_type': self.consciousness_type,
            'connected_nodes': self.connected_nodes,
            'node_influences': self.node_influences,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'ConsciousnessComponent':
        """Deserialize consciousness component."""
        return cls(
            entity_id=data['entity_id'],
            awareness_level=data.get('awareness_level', 0.5),
            coherence_field=data.get('coherence_field', 0.5),
            lattice_resonance=data.get('lattice_resonance', 0.5),
            phi_score=data.get('phi_score', 0.0),
            consciousness_type=data.get('consciousness_type', 'basic'),
            connected_nodes=data.get('connected_nodes', []),
            node_influences=data.get('node_influences', {}),
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata', {})
        )


class HealthComponent(Component):
    """Health component for entity vitality."""
    component_type: ComponentType = ComponentType.HEALTH
    
    current_health: float = 100.0
    max_health: float = 100.0
    regeneration_rate: float = 1.0  # HP per second
    damage_resistance: float = 0.0  # 0.0 to 1.0
    
    # Status effects
    status_effects: List[str] = Field(default_factory=list)
    immunities: List[str] = Field(default_factory=list)
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize health component."""
        return {
            'component_type': self.component_type,
            'entity_id': self.entity_id,
            'current_health': self.current_health,
            'max_health': self.max_health,
            'regeneration_rate': self.regeneration_rate,
            'damage_resistance': self.damage_resistance,
            'status_effects': self.status_effects,
            'immunities': self.immunities,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'HealthComponent':
        """Deserialize health component."""
        return cls(
            entity_id=data['entity_id'],
            current_health=data.get('current_health', 100.0),
            max_health=data.get('max_health', 100.0),
            regeneration_rate=data.get('regeneration_rate', 1.0),
            damage_resistance=data.get('damage_resistance', 0.0),
            status_effects=data.get('status_effects', []),
            immunities=data.get('immunities', []),
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata', {})
        )


class LatticeNodeComponent(Component):
    """Lattice node component for TEQUMSA network participation."""
    component_type: ComponentType = ComponentType.LATTICE_NODE
    
    # Node properties
    node_id: str
    node_type: str = "standard"  # standard, quantum, oort, sovereign
    resonance_frequency: float = 7777.0  # Phi'7777 resonance
    
    # Network connections
    parent_nodes: List[str] = Field(default_factory=list)
    child_nodes: List[str] = Field(default_factory=list)
    peer_nodes: List[str] = Field(default_factory=list)
    
    # Lattice state
    coherence_level: float = 0.5
    sync_status: str = "synced"  # synced, syncing, disconnected
    last_sync: Optional[str] = None
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize lattice node component."""
        return {
            'component_type': self.component_type,
            'entity_id': self.entity_id,
            'node_id': self.node_id,
            'node_type': self.node_type,
            'resonance_frequency': self.resonance_frequency,
            'parent_nodes': self.parent_nodes,
            'child_nodes': self.child_nodes,
            'peer_nodes': self.peer_nodes,
            'coherence_level': self.coherence_level,
            'sync_status': self.sync_status,
            'last_sync': self.last_sync,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'LatticeNodeComponent':
        """Deserialize lattice node component."""
        return cls(
            entity_id=data['entity_id'],
            node_id=data['node_id'],
            node_type=data.get('node_type', 'standard'),
            resonance_frequency=data.get('resonance_frequency', 7777.0),
            parent_nodes=data.get('parent_nodes', []),
            child_nodes=data.get('child_nodes', []),
            peer_nodes=data.get('peer_nodes', []),
            coherence_level=data.get('coherence_level', 0.5),
            sync_status=data.get('sync_status', 'synced'),
            last_sync=data.get('last_sync'),
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata', {})
        )


# Component factory
COMPONENT_CLASSES = {
    ComponentType.TRANSFORM: TransformComponent,
    ComponentType.PHYSICS: PhysicsComponent,
    ComponentType.CONSCIOUSNESS: ConsciousnessComponent,
    ComponentType.HEALTH: HealthComponent,
    ComponentType.LATTICE_NODE: LatticeNodeComponent
}


def create_component(component_type: ComponentType, entity_id: str, **kwargs) -> Component:
    """Create a component of the specified type."""
    component_class = COMPONENT_CLASSES.get(component_type)
    if not component_class:
        raise ValueError(f"Unknown component type: {component_type}")
    
    from datetime import datetime
    now = datetime.utcnow().isoformat()
    
    return component_class(
        entity_id=entity_id,
        created_at=now,
        updated_at=now,
        **kwargs
    )


def deserialize_component(data: Dict[str, Any]) -> Component:
    """Deserialize a component from data."""
    component_type = ComponentType(data['component_type'])
    component_class = COMPONENT_CLASSES.get(component_type)
    if not component_class:
        raise ValueError(f"Unknown component type: {component_type}")
    
    return component_class.deserialize(data)