"""Thread-safe patch queue for orchestrator system."""
import threading
from typing import List, Optional, Any, Dict
from queue import PriorityQueue, Empty
from datetime import datetime
from dataclasses import dataclass

from ..world.patch_model import ECStatePatch


@dataclass
class QueuedPatch:
    """Wrapper for patches in the queue with priority."""
    priority: int
    timestamp: float
    patch: ECStatePatch
    
    def __lt__(self, other):
        """Compare patches for priority queue ordering."""
        # Higher priority first, then earlier timestamp
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.timestamp < other.timestamp


class PatchQueue:
    """Thread-safe queue for ECS patches."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize patch queue."""
        self.max_size = max_size
        self._queue = PriorityQueue(maxsize=max_size)
        self._lock = threading.RLock()
        self._stats = {
            'total_queued': 0,
            'total_processed': 0,
            'current_size': 0,
            'last_queued_at': None,
            'last_processed_at': None
        }
    
    def put(self, patch: ECStatePatch, priority: int = 0, block: bool = True, timeout: Optional[float] = None) -> bool:
        """Add a patch to the queue."""
        try:
            queued_patch = QueuedPatch(
                priority=priority,
                timestamp=datetime.utcnow().timestamp(),
                patch=patch
            )
            
            self._queue.put(queued_patch, block=block, timeout=timeout)
            
            with self._lock:
                self._stats['total_queued'] += 1
                self._stats['current_size'] = self._queue.qsize()
                self._stats['last_queued_at'] = datetime.utcnow().isoformat()
            
            return True
            
        except Exception:
            return False
    
    def get(self, block: bool = True, timeout: Optional[float] = None) -> Optional[ECStatePatch]:
        """Get a patch from the queue."""
        try:
            queued_patch = self._queue.get(block=block, timeout=timeout)
            
            with self._lock:
                self._stats['total_processed'] += 1
                self._stats['current_size'] = self._queue.qsize()
                self._stats['last_processed_at'] = datetime.utcnow().isoformat()
            
            return queued_patch.patch
            
        except Empty:
            return None
    
    def peek(self) -> Optional[ECStatePatch]:
        """Peek at the next patch without removing it."""
        # Note: This is not atomic with get() due to PriorityQueue limitations
        if self.empty():
            return None
        
        # Get and immediately put back
        try:
            queued_patch = self._queue.get_nowait()
            self._queue.put_nowait(queued_patch)
            return queued_patch.patch
        except Empty:
            return None
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()
    
    def full(self) -> bool:
        """Check if queue is full."""
        return self._queue.full()
    
    def qsize(self) -> int:
        """Get current queue size."""
        return self._queue.qsize()
    
    def clear(self) -> int:
        """Clear all patches from queue."""
        count = 0
        while not self.empty():
            try:
                self._queue.get_nowait()
                count += 1
            except Empty:
                break
        
        with self._lock:
            self._stats['current_size'] = 0
        
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        with self._lock:
            return self._stats.copy()
    
    def get_patches_by_region(self, region_id: str, limit: int = 10) -> List[ECStatePatch]:
        """Get patches for a specific region (non-destructive peek)."""
        patches = []
        temp_patches = []
        
        # Extract patches to check
        for _ in range(min(limit, self.qsize())):
            try:
                queued_patch = self._queue.get_nowait()
                temp_patches.append(queued_patch)
                
                if queued_patch.patch.region_id == region_id:
                    patches.append(queued_patch.patch)
                    
            except Empty:
                break
        
        # Put patches back
        for queued_patch in temp_patches:
            try:
                self._queue.put_nowait(queued_patch)
            except:
                pass  # Queue full, patches lost (should not happen with proper sizing)
        
        return patches


class PatchQueueManager:
    """Manages multiple patch queues for different regions/purposes."""
    
    def __init__(self):
        """Initialize patch queue manager."""
        self._queues: Dict[str, PatchQueue] = {}
        self._default_queue = PatchQueue()
        self._lock = threading.RLock()
    
    def get_queue(self, queue_name: str = "default") -> PatchQueue:
        """Get or create a patch queue."""
        with self._lock:
            if queue_name == "default":
                return self._default_queue
            
            if queue_name not in self._queues:
                self._queues[queue_name] = PatchQueue()
            
            return self._queues[queue_name]
    
    def create_queue(self, queue_name: str, max_size: int = 1000) -> PatchQueue:
        """Create a new patch queue."""
        with self._lock:
            if queue_name in self._queues:
                raise ValueError(f"Queue {queue_name} already exists")
            
            self._queues[queue_name] = PatchQueue(max_size)
            return self._queues[queue_name]
    
    def delete_queue(self, queue_name: str) -> bool:
        """Delete a patch queue."""
        with self._lock:
            if queue_name == "default":
                return False  # Cannot delete default queue
            
            if queue_name in self._queues:
                del self._queues[queue_name]
                return True
            
            return False
    
    def list_queues(self) -> List[str]:
        """List all queue names."""
        with self._lock:
            queues = ["default"] + list(self._queues.keys())
            return queues
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all queues."""
        with self._lock:
            stats = {
                "default": self._default_queue.get_stats()
            }
            
            for name, queue in self._queues.items():
                stats[name] = queue.get_stats()
            
            return stats
    
    def route_patch(self, patch: ECStatePatch, priority: int = 0) -> bool:
        """Route patch to appropriate queue based on region or other criteria."""
        queue_name = "default"
        
        # Route by region if specified
        if patch.region_id:
            queue_name = f"region_{patch.region_id}"
        
        # Route by source
        elif patch.source in ["orchestrator", "biome_engine"]:
            queue_name = "orchestrator"
        elif patch.source in ["user", "api"]:
            queue_name = "user_actions"
        
        queue = self.get_queue(queue_name)
        return queue.put(patch, priority)


# Global patch queue manager
_queue_manager = None


def get_patch_queue_manager() -> PatchQueueManager:
    """Get the global patch queue manager."""
    global _queue_manager
    if _queue_manager is None:
        _queue_manager = PatchQueueManager()
    return _queue_manager


def get_default_patch_queue() -> PatchQueue:
    """Get the default patch queue."""
    return get_patch_queue_manager().get_queue("default")


def queue_patch(patch: ECStatePatch, priority: int = 0, queue_name: str = "default") -> bool:
    """Queue a patch for processing."""
    manager = get_patch_queue_manager()
    if queue_name == "auto":
        return manager.route_patch(patch, priority)
    else:
        queue = manager.get_queue(queue_name)
        return queue.put(patch, priority)