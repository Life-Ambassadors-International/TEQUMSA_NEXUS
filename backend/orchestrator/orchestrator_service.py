"""Main orchestrator service for TEQUMSA Level 100."""
import threading
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from ..world.ecs_state import get_ecs_state
from ..world.patch_model import apply_patch_to_ecs
from ..utils.time_series import record_metric, get_time_series_manager
from .patch_queue import get_patch_queue_manager, PatchQueue
from .biome_engine import get_biome_engine


class OrchestrationJob:
    """Represents an orchestration job."""
    
    def __init__(self, job_id: str, job_type: str, priority: int = 0):
        """Initialize orchestration job."""
        self.job_id = job_id
        self.job_type = job_type
        self.priority = priority
        self.created_at = datetime.utcnow()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.status = "pending"  # pending, running, completed, failed
        self.metadata: Dict[str, Any] = {}
        self.result: Optional[Any] = None
        self.error: Optional[str] = None
    
    def start(self):
        """Mark job as started."""
        self.started_at = datetime.utcnow()
        self.status = "running"
    
    def complete(self, result: Any = None):
        """Mark job as completed."""
        self.completed_at = datetime.utcnow()
        self.status = "completed"
        self.result = result
    
    def fail(self, error: str):
        """Mark job as failed."""
        self.completed_at = datetime.utcnow()
        self.status = "failed"
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary."""
        return {
            'job_id': self.job_id,
            'job_type': self.job_type,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'metadata': self.metadata,
            'result': self.result,
            'error': self.error
        }


class OrchestratorService:
    """Main orchestrator service for managing the TEQUMSA metaverse."""
    
    def __init__(self):
        """Initialize orchestrator service."""
        self.ecs = get_ecs_state()
        self.biome_engine = get_biome_engine()
        self.patch_manager = get_patch_queue_manager()
        self.time_series = get_time_series_manager()
        
        # Threading
        self._lock = threading.RLock()
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None
        self._patch_processor_thread: Optional[threading.Thread] = None
        
        # Job management
        self._jobs: Dict[str, OrchestrationJob] = {}
        self._job_counter = 0
        
        # Service state
        self._last_update = datetime.utcnow()
        self._update_interval = 1.0  # seconds
        self._stats = {
            'patches_processed': 0,
            'jobs_completed': 0,
            'uptime_seconds': 0,
            'last_error': None
        }
    
    def start(self):
        """Start the orchestrator service."""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            
            # Start worker threads
            self._worker_thread = threading.Thread(target=self._main_loop, daemon=True)
            self._worker_thread.start()
            
            self._patch_processor_thread = threading.Thread(target=self._patch_processor_loop, daemon=True)
            self._patch_processor_thread.start()
            
            print("Orchestrator service started")
            record_metric("orchestrator_starts", 1)
    
    def stop(self):
        """Stop the orchestrator service."""
        with self._lock:
            if not self._running:
                return
            
            self._running = False
            
            # Wait for threads to finish
            if self._worker_thread:
                self._worker_thread.join(timeout=5.0)
            
            if self._patch_processor_thread:
                self._patch_processor_thread.join(timeout=5.0)
            
            print("Orchestrator service stopped")
            record_metric("orchestrator_stops", 1)
    
    def _main_loop(self):
        """Main orchestrator loop."""
        while self._running:
            try:
                start_time = time.time()
                
                # Update biomes
                delta_time = (datetime.utcnow() - self._last_update).total_seconds()
                self.biome_engine.update_biomes(delta_time)
                
                # Process jobs
                self._process_jobs()
                
                # Update metrics
                self._update_metrics()
                
                # Update last update time
                self._last_update = datetime.utcnow()
                
                # Sleep for remaining time
                elapsed = time.time() - start_time
                sleep_time = max(0, self._update_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
            except Exception as e:
                print(f"Error in orchestrator main loop: {e}")
                with self._lock:
                    self._stats['last_error'] = str(e)
                time.sleep(1.0)
    
    def _patch_processor_loop(self):
        """Process patches from the queue."""
        default_queue = self.patch_manager.get_queue("default")
        
        while self._running:
            try:
                # Get patch from queue
                patch = default_queue.get(timeout=1.0)
                if patch:
                    # Apply patch to ECS
                    result = apply_patch_to_ecs(patch, self.ecs)
                    
                    # Record metrics
                    with self._lock:
                        self._stats['patches_processed'] += 1
                    
                    record_metric("patches_processed", 1, {
                        'success': result.success,
                        'operations': result.operations_applied,
                        'source': patch.source
                    })
                    
                    if not result.success:
                        print(f"Patch {patch.patch_id} failed: {result.errors}")
                
            except Exception as e:
                if "timed out" not in str(e):  # Ignore timeout exceptions
                    print(f"Error in patch processor: {e}")
    
    def _process_jobs(self):
        """Process orchestration jobs."""
        with self._lock:
            # Get pending jobs sorted by priority
            pending_jobs = [
                job for job in self._jobs.values() 
                if job.status == "pending"
            ]
            pending_jobs.sort(key=lambda j: j.priority, reverse=True)
            
            # Process jobs (limit to avoid blocking)
            for job in pending_jobs[:10]:
                try:
                    self._execute_job(job)
                except Exception as e:
                    job.fail(str(e))
                    print(f"Job {job.job_id} failed: {e}")
    
    def _execute_job(self, job: OrchestrationJob):
        """Execute a single orchestration job."""
        job.start()
        
        try:
            if job.job_type == "biome_activation":
                self._execute_biome_activation(job)
            elif job.job_type == "entity_spawn":
                self._execute_entity_spawn(job)
            elif job.job_type == "system_maintenance":
                self._execute_system_maintenance(job)
            elif job.job_type == "consciousness_sync":
                self._execute_consciousness_sync(job)
            else:
                raise ValueError(f"Unknown job type: {job.job_type}")
            
            job.complete()
            
            with self._lock:
                self._stats['jobs_completed'] += 1
            
        except Exception as e:
            job.fail(str(e))
            raise
    
    def _execute_biome_activation(self, job: OrchestrationJob):
        """Execute biome activation job."""
        biome_id = job.metadata.get('biome_id')
        region_id = job.metadata.get('region_id')
        
        if not biome_id or not region_id:
            raise ValueError("Biome activation requires biome_id and region_id")
        
        success = self.biome_engine.activate_biome(biome_id, region_id)
        if not success:
            raise ValueError(f"Failed to activate biome {biome_id} in region {region_id}")
        
        job.result = {'biome_id': biome_id, 'region_id': region_id, 'activated': True}
    
    def _execute_entity_spawn(self, job: OrchestrationJob):
        """Execute entity spawn job."""
        entity_type = job.metadata.get('entity_type')
        region_id = job.metadata.get('region_id')
        
        if not entity_type:
            raise ValueError("Entity spawn requires entity_type")
        
        from ..world.ecs_state import spawn_entity
        entity = spawn_entity(entity_type, region_id)
        
        job.result = {'entity_id': entity.entity_id, 'entity_type': entity_type}
    
    def _execute_system_maintenance(self, job: OrchestrationJob):
        """Execute system maintenance job."""
        # Clean up old metrics
        self.time_series.cleanup_old_data(24)  # Keep 24 hours
        
        # Clean up completed jobs older than 1 hour
        cutoff = datetime.utcnow() - timedelta(hours=1)
        
        with self._lock:
            old_jobs = [
                job_id for job_id, job in self._jobs.items()
                if job.status in ["completed", "failed"] and job.completed_at and job.completed_at < cutoff
            ]
            
            for job_id in old_jobs:
                del self._jobs[job_id]
        
        job.result = {'cleaned_jobs': len(old_jobs)}
    
    def _execute_consciousness_sync(self, job: OrchestrationJob):
        """Execute consciousness synchronization job."""
        region_id = job.metadata.get('region_id')
        
        # Get all consciousness entities in region
        consciousness_entities = self.ecs.get_entities_with_component(ComponentType.CONSCIOUSNESS)
        
        if region_id:
            consciousness_entities = [
                eid for eid in consciousness_entities
                if self.ecs.get_entity(eid) and self.ecs.get_entity(eid).region_id == region_id
            ]
        
        # Perform synchronization (simplified)
        sync_count = 0
        for entity_id in consciousness_entities:
            consciousness = self.ecs.get_component(entity_id, ComponentType.CONSCIOUSNESS)
            if consciousness:
                # Update resonance (simplified synchronization)
                consciousness.lattice_resonance = min(1.0, consciousness.lattice_resonance + 0.01)
                self.ecs.add_component(entity_id, consciousness)
                sync_count += 1
        
        job.result = {'synchronized_entities': sync_count}
    
    def _update_metrics(self):
        """Update orchestrator metrics."""
        with self._lock:
            # Uptime
            uptime = (datetime.utcnow() - self._last_update).total_seconds()
            self._stats['uptime_seconds'] += uptime
            
            # Record metrics
            record_metric("orchestrator_uptime", self._stats['uptime_seconds'])
            record_metric("orchestrator_patches_processed", self._stats['patches_processed'])
            record_metric("orchestrator_jobs_completed", self._stats['jobs_completed'])
            
            # Queue metrics
            queue_stats = self.patch_manager.get_all_stats()
            for queue_name, stats in queue_stats.items():
                record_metric(f"queue_{queue_name}_size", stats['current_size'])
    
    def submit_job(self, job_type: str, priority: int = 0, **metadata) -> str:
        """Submit a job to the orchestrator."""
        with self._lock:
            self._job_counter += 1
            job_id = f"job_{job_type}_{self._job_counter}_{int(time.time())}"
            
            job = OrchestrationJob(job_id, job_type, priority)
            job.metadata.update(metadata)
            
            self._jobs[job_id] = job
            
            record_metric("orchestrator_jobs_submitted", 1, {'job_type': job_type})
            
            return job_id
    
    def get_job(self, job_id: str) -> Optional[OrchestrationJob]:
        """Get job by ID."""
        with self._lock:
            return self._jobs.get(job_id)
    
    def list_jobs(self, status: Optional[str] = None) -> List[OrchestrationJob]:
        """List jobs, optionally filtered by status."""
        with self._lock:
            jobs = list(self._jobs.values())
            
            if status:
                jobs = [job for job in jobs if job.status == status]
            
            return jobs
    
    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        with self._lock:
            return {
                'running': self._running,
                'stats': self._stats.copy(),
                'job_counts': {
                    'pending': len([j for j in self._jobs.values() if j.status == "pending"]),
                    'running': len([j for j in self._jobs.values() if j.status == "running"]),
                    'completed': len([j for j in self._jobs.values() if j.status == "completed"]),
                    'failed': len([j for j in self._jobs.values() if j.status == "failed"])
                },
                'queue_stats': self.patch_manager.get_all_stats(),
                'biome_stats': len(self.biome_engine.get_active_biomes())
            }


# Global orchestrator service instance
_orchestrator = None


def get_orchestrator_service() -> OrchestratorService:
    """Get the global orchestrator service instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OrchestratorService()
    return _orchestrator