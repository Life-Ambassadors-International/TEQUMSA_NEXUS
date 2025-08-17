"""ID generation utilities for TEQUMSA Level 100."""
import uuid
import time
import hashlib
from typing import Optional, Union


class IDGenerator:
    """ID generation utility class."""
    
    @staticmethod
    def uuid4() -> str:
        """Generate a random UUID4."""
        return str(uuid.uuid4())
    
    @staticmethod
    def uuid4_short() -> str:
        """Generate a short UUID4 (first 8 characters)."""
        return str(uuid.uuid4())[:8]
    
    @staticmethod
    def timestamp_id() -> str:
        """Generate timestamp-based ID."""
        return str(int(time.time() * 1000000))
    
    @staticmethod
    def entity_id(entity_type: str, region_id: Optional[str] = None) -> str:
        """Generate entity ID for ECS system."""
        base = f"{entity_type}_{int(time.time() * 1000000)}"
        if region_id:
            base = f"{region_id}_{base}"
        return base
    
    @staticmethod
    def biome_id(biome_name: str) -> str:
        """Generate biome ID."""
        # Normalize name and add UUID suffix
        normalized = biome_name.lower().replace(' ', '_').replace('-', '_')
        return f"biome_{normalized}_{IDGenerator.uuid4_short()}"
    
    @staticmethod
    def session_id(account_id: Optional[str] = None) -> str:
        """Generate session ID."""
        base = f"session_{int(time.time() * 1000)}"
        if account_id:
            base = f"{account_id}_{base}"
        return base
    
    @staticmethod
    def hash_id(data: Union[str, bytes]) -> str:
        """Generate deterministic hash-based ID."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()[:16]
    
    @staticmethod
    def patch_id(region_id: str, patch_type: str) -> str:
        """Generate patch ID for ECS patches."""
        timestamp = int(time.time() * 1000)
        return f"patch_{region_id}_{patch_type}_{timestamp}"
    
    @staticmethod
    def orchestrator_job_id(job_type: str) -> str:
        """Generate orchestrator job ID."""
        return f"job_{job_type}_{IDGenerator.uuid4_short()}_{int(time.time())}"


# Convenience functions
def generate_id() -> str:
    """Generate a standard UUID4."""
    return IDGenerator.uuid4()


def generate_short_id() -> str:
    """Generate a short ID."""
    return IDGenerator.uuid4_short()


def generate_entity_id(entity_type: str, region_id: Optional[str] = None) -> str:
    """Generate entity ID."""
    return IDGenerator.entity_id(entity_type, region_id)


def generate_session_id(account_id: Optional[str] = None) -> str:
    """Generate session ID."""
    return IDGenerator.session_id(account_id)