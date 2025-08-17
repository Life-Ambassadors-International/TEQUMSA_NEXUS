"""ECS patch model for state updates in TEQUMSA Level 100."""
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

from .ecs_components import ComponentType, Component, deserialize_component
from ..utils.id_gen import IDGenerator


class PatchType(str, Enum):
    """Types of ECS patches."""
    ENTITY_CREATE = "entity_create"
    ENTITY_DELETE = "entity_delete"
    ENTITY_UPDATE = "entity_update"
    COMPONENT_ADD = "component_add"
    COMPONENT_UPDATE = "component_update"
    COMPONENT_REMOVE = "component_remove"
    BULK_UPDATE = "bulk_update"
    REGION_SYNC = "region_sync"


class PatchOperation(BaseModel):
    """Individual patch operation."""
    operation_id: str = Field(default_factory=lambda: IDGenerator.uuid4_short())
    patch_type: PatchType
    entity_id: Optional[str] = None
    component_type: Optional[ComponentType] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ECStatePatch(BaseModel):
    """ECS state patch for atomic updates."""
    patch_id: str = Field(default_factory=lambda: IDGenerator.patch_id("default", "update"))
    region_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    operations: List[PatchOperation] = Field(default_factory=list)
    source: str = "unknown"  # orchestrator, user, system, etc.
    priority: int = 0  # Higher priority patches applied first
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_operation(self, patch_type: PatchType, entity_id: Optional[str] = None,
                     component_type: Optional[ComponentType] = None,
                     data: Optional[Dict[str, Any]] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> PatchOperation:
        """Add an operation to this patch."""
        operation = PatchOperation(
            patch_type=patch_type,
            entity_id=entity_id,
            component_type=component_type,
            data=data or {},
            metadata=metadata or {}
        )
        self.operations.append(operation)
        return operation
    
    def add_entity_create(self, entity_id: str, entity_type: str, 
                         region_id: Optional[str] = None,
                         components: Optional[List[Component]] = None) -> PatchOperation:
        """Add entity creation operation."""
        data = {
            'entity_type': entity_type,
            'region_id': region_id
        }
        
        if components:
            data['components'] = [comp.serialize() for comp in components]
        
        return self.add_operation(
            patch_type=PatchType.ENTITY_CREATE,
            entity_id=entity_id,
            data=data
        )
    
    def add_entity_delete(self, entity_id: str) -> PatchOperation:
        """Add entity deletion operation."""
        return self.add_operation(
            patch_type=PatchType.ENTITY_DELETE,
            entity_id=entity_id
        )
    
    def add_component_update(self, entity_id: str, component: Component) -> PatchOperation:
        """Add component update operation."""
        return self.add_operation(
            patch_type=PatchType.COMPONENT_UPDATE,
            entity_id=entity_id,
            component_type=component.component_type,
            data=component.serialize()
        )
    
    def add_component_add(self, entity_id: str, component: Component) -> PatchOperation:
        """Add component addition operation."""
        return self.add_operation(
            patch_type=PatchType.COMPONENT_ADD,
            entity_id=entity_id,
            component_type=component.component_type,
            data=component.serialize()
        )
    
    def add_component_remove(self, entity_id: str, component_type: ComponentType) -> PatchOperation:
        """Add component removal operation."""
        return self.add_operation(
            patch_type=PatchType.COMPONENT_REMOVE,
            entity_id=entity_id,
            component_type=component_type
        )


class PatchResult(BaseModel):
    """Result of applying a patch."""
    patch_id: str
    success: bool
    operations_applied: int
    operations_failed: int
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    applied_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PatchApplier:
    """Applies patches to ECS state."""
    
    def __init__(self, ecs_state):
        """Initialize patch applier with ECS state."""
        self.ecs_state = ecs_state
    
    def apply_patch(self, patch: ECStatePatch) -> PatchResult:
        """Apply a patch to the ECS state."""
        result = PatchResult(
            patch_id=patch.patch_id,
            success=True,
            operations_applied=0,
            operations_failed=0
        )
        
        # Sort operations by priority (if any priority system needed)
        sorted_operations = sorted(patch.operations, 
                                 key=lambda op: op.metadata.get('priority', 0), 
                                 reverse=True)
        
        for operation in sorted_operations:
            try:
                self._apply_operation(operation)
                result.operations_applied += 1
            except Exception as e:
                result.operations_failed += 1
                result.errors.append(f"Operation {operation.operation_id}: {str(e)}")
                result.success = False
        
        return result
    
    def _apply_operation(self, operation: PatchOperation):
        """Apply a single patch operation."""
        if operation.patch_type == PatchType.ENTITY_CREATE:
            self._apply_entity_create(operation)
        elif operation.patch_type == PatchType.ENTITY_DELETE:
            self._apply_entity_delete(operation)
        elif operation.patch_type == PatchType.COMPONENT_ADD:
            self._apply_component_add(operation)
        elif operation.patch_type == PatchType.COMPONENT_UPDATE:
            self._apply_component_update(operation)
        elif operation.patch_type == PatchType.COMPONENT_REMOVE:
            self._apply_component_remove(operation)
        else:
            raise ValueError(f"Unknown patch type: {operation.patch_type}")
    
    def _apply_entity_create(self, operation: PatchOperation):
        """Apply entity creation operation."""
        entity_type = operation.data['entity_type']
        region_id = operation.data.get('region_id')
        
        entity = self.ecs_state.create_entity(
            entity_type=entity_type,
            region_id=region_id,
            entity_id=operation.entity_id
        )
        
        # Add components if provided
        components_data = operation.data.get('components', [])
        for comp_data in components_data:
            component = deserialize_component(comp_data)
            self.ecs_state.add_component(entity.entity_id, component)
    
    def _apply_entity_delete(self, operation: PatchOperation):
        """Apply entity deletion operation."""
        if not operation.entity_id:
            raise ValueError("Entity ID required for entity deletion")
        
        success = self.ecs_state.delete_entity(operation.entity_id)
        if not success:
            raise ValueError(f"Entity {operation.entity_id} not found")
    
    def _apply_component_add(self, operation: PatchOperation):
        """Apply component addition operation."""
        if not operation.entity_id or not operation.component_type:
            raise ValueError("Entity ID and component type required for component addition")
        
        component = deserialize_component(operation.data)
        self.ecs_state.add_component(operation.entity_id, component)
    
    def _apply_component_update(self, operation: PatchOperation):
        """Apply component update operation."""
        if not operation.entity_id or not operation.component_type:
            raise ValueError("Entity ID and component type required for component update")
        
        # Get existing component
        existing = self.ecs_state.get_component(operation.entity_id, operation.component_type)
        if not existing:
            raise ValueError(f"Component {operation.component_type} not found on entity {operation.entity_id}")
        
        # Update component with new data
        component = deserialize_component(operation.data)
        self.ecs_state.add_component(operation.entity_id, component)
    
    def _apply_component_remove(self, operation: PatchOperation):
        """Apply component removal operation."""
        if not operation.entity_id or not operation.component_type:
            raise ValueError("Entity ID and component type required for component removal")
        
        success = self.ecs_state.remove_component(operation.entity_id, operation.component_type)
        if not success:
            raise ValueError(f"Component {operation.component_type} not found on entity {operation.entity_id}")


class PatchBuilder:
    """Builder for creating patches."""
    
    def __init__(self, region_id: Optional[str] = None, source: str = "unknown"):
        """Initialize patch builder."""
        self.patch = ECStatePatch(region_id=region_id, source=source)
    
    def create_entity(self, entity_id: str, entity_type: str, 
                     region_id: Optional[str] = None,
                     components: Optional[List[Component]] = None) -> 'PatchBuilder':
        """Add entity creation to patch."""
        self.patch.add_entity_create(entity_id, entity_type, region_id, components)
        return self
    
    def delete_entity(self, entity_id: str) -> 'PatchBuilder':
        """Add entity deletion to patch."""
        self.patch.add_entity_delete(entity_id)
        return self
    
    def add_component(self, entity_id: str, component: Component) -> 'PatchBuilder':
        """Add component addition to patch."""
        self.patch.add_component_add(entity_id, component)
        return self
    
    def update_component(self, entity_id: str, component: Component) -> 'PatchBuilder':
        """Add component update to patch."""
        self.patch.add_component_update(entity_id, component)
        return self
    
    def remove_component(self, entity_id: str, component_type: ComponentType) -> 'PatchBuilder':
        """Add component removal to patch."""
        self.patch.add_component_remove(entity_id, component_type)
        return self
    
    def build(self) -> ECStatePatch:
        """Build and return the patch."""
        return self.patch


# Convenience functions
def create_patch(region_id: Optional[str] = None, source: str = "unknown") -> PatchBuilder:
    """Create a new patch builder."""
    return PatchBuilder(region_id=region_id, source=source)


def apply_patch_to_ecs(patch: ECStatePatch, ecs_state=None) -> PatchResult:
    """Apply a patch to the ECS state."""
    if ecs_state is None:
        from .ecs_state import get_ecs_state
        ecs_state = get_ecs_state()
    
    applier = PatchApplier(ecs_state)
    return applier.apply_patch(patch)