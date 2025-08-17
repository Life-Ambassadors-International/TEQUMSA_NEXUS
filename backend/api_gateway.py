"""FastAPI gateway for TEQUMSA Level 100 system."""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any, Optional
import logging

# Import routers and services
from subscription.api import router as subscription_router
from utils.config import get_config


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting TEQUMSA Level 100 API Gateway")
    
    # Start orchestrator service
    try:
        from orchestrator.orchestrator_service import get_orchestrator_service
        orchestrator = get_orchestrator_service()
        orchestrator.start()
        logger.info("Orchestrator service started")
    except Exception as e:
        logger.error(f"Failed to start orchestrator: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down TEQUMSA Level 100 API Gateway")
    
    # Stop orchestrator service
    try:
        from orchestrator.orchestrator_service import get_orchestrator_service
        orchestrator = get_orchestrator_service()
        orchestrator.stop()
        logger.info("Orchestrator service stopped")
    except Exception as e:
        logger.error(f"Failed to stop orchestrator: {e}")


# Create FastAPI app
app = FastAPI(
    title="TEQUMSA Level 100 API",
    description="API Gateway for TEQUMSA Level 100 Civilization System",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle global exceptions."""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "TEQUMSA Level 100 API Gateway",
        "version": "1.0.0"
    }


# World state endpoints
@app.get("/world/regions/{region_id}/state")
async def get_world_state(region_id: str):
    """Get world state for a region."""
    try:
        from world.ecs_state import get_ecs_state
        ecs = get_ecs_state()
        world_state = ecs.get_world_state(region_id)
        return world_state
    except Exception as e:
        logger.error(f"Error getting world state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/world/patches")
async def apply_patch(patch_data: Dict[str, Any]):
    """Apply a patch to the world state."""
    try:
        from world.patch_model import ECStatePatch, apply_patch_to_ecs
        from orchestrator.patch_queue import queue_patch
        
        # Create patch from data
        patch = ECStatePatch(**patch_data)
        
        # Queue for processing
        success = queue_patch(patch, priority=patch_data.get('priority', 0))
        
        if success:
            return {"status": "queued", "patch_id": patch.patch_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to queue patch")
            
    except Exception as e:
        logger.error(f"Error applying patch: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Group sync endpoint
@app.post("/group/sync")
async def group_sync(sync_data: Dict[str, Any]):
    """Synchronize group consciousness."""
    try:
        from group.coherence_field import get_coherence_field_manager
        
        field_manager = get_coherence_field_manager()
        account_id = sync_data.get('account_id')
        phi_score = sync_data.get('phi_score', 0.0)
        region_id = sync_data.get('region_id')
        
        # Update entity in coherence field
        if account_id:
            # Find or create entity field assignment
            entity_field = field_manager.get_entity_field(account_id)
            if not entity_field and region_id:
                # Create group field for region if not exists
                from group.coherence_field import CoherenceFieldType
                fields = field_manager.get_fields_by_region(region_id)
                if not fields:
                    field = field_manager.create_field(CoherenceFieldType.GROUP, region_id)
                    field_manager.assign_entity_to_field(account_id, field.field_id)
        
        return {"status": "synchronized", "phi_score": phi_score}
        
    except Exception as e:
        logger.error(f"Error in group sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Consent endpoints
@app.post("/consent/record")
async def record_consent_endpoint(consent_data: Dict[str, Any]):
    """Record user consent."""
    try:
        from consent.consent_ledger import get_consent_ledger, ConsentType, ConsentStatus
        
        ledger = get_consent_ledger()
        account_id = consent_data['account_id']
        consent_type = ConsentType(consent_data['consent_type'])
        granted = consent_data.get('granted', True)
        
        status = ConsentStatus.GRANTED if granted else ConsentStatus.DENIED
        consent = ledger.record_consent(
            account_id=account_id,
            consent_type=consent_type,
            status=status,
            details=consent_data.get('details', {}),
            expires_at=consent_data.get('expires_at')
        )
        
        return {
            "consent_id": consent.consent_id,
            "status": consent.status.value,
            "granted_at": consent.granted_at
        }
        
    except Exception as e:
        logger.error(f"Error recording consent: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/consent/{account_id}/check/{consent_type}")
async def check_consent_endpoint(account_id: str, consent_type: str):
    """Check if user has valid consent."""
    try:
        from consent.consent_ledger import check_consent, ConsentType
        
        consent_type_enum = ConsentType(consent_type)
        has_consent = check_consent(account_id, consent_type_enum)
        
        return {
            "account_id": account_id,
            "consent_type": consent_type,
            "has_consent": has_consent
        }
        
    except Exception as e:
        logger.error(f"Error checking consent: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Orchestrator endpoints
@app.get("/orchestrator/status")
async def get_orchestrator_status():
    """Get orchestrator service status."""
    try:
        from orchestrator.orchestrator_service import get_orchestrator_service
        orchestrator = get_orchestrator_service()
        return orchestrator.get_stats()
    except Exception as e:
        logger.error(f"Error getting orchestrator status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/orchestrator/jobs")
async def submit_orchestrator_job(job_data: Dict[str, Any]):
    """Submit a job to the orchestrator."""
    try:
        from orchestrator.orchestrator_service import get_orchestrator_service
        
        orchestrator = get_orchestrator_service()
        job_id = orchestrator.submit_job(
            job_type=job_data['job_type'],
            priority=job_data.get('priority', 0),
            **job_data.get('metadata', {})
        )
        
        return {"job_id": job_id, "status": "submitted"}
        
    except Exception as e:
        logger.error(f"Error submitting job: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Biome endpoints
@app.get("/biomes")
async def list_biomes():
    """List available biomes."""
    try:
        from orchestrator.biome_engine import get_biome_engine
        biome_engine = get_biome_engine()
        biomes = biome_engine.loader.list_biomes()
        return {"biomes": biomes}
    except Exception as e:
        logger.error(f"Error listing biomes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/biomes/{biome_id}")
async def get_biome_info(biome_id: str):
    """Get biome information."""
    try:
        from orchestrator.biome_engine import get_biome_engine
        biome_engine = get_biome_engine()
        biome = biome_engine.loader.get_biome(biome_id)
        
        if not biome:
            raise HTTPException(status_code=404, detail="Biome not found")
        
        return {
            "biome_id": biome.biome_id,
            "name": biome.name,
            "description": biome.description,
            "metadata": biome.metadata
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting biome info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/biomes/{biome_id}/activate")
async def activate_biome(biome_id: str, activation_data: Dict[str, Any]):
    """Activate a biome in a region."""
    try:
        from orchestrator.orchestrator_service import get_orchestrator_service
        
        orchestrator = get_orchestrator_service()
        region_id = activation_data['region_id']
        
        job_id = orchestrator.submit_job(
            job_type="biome_activation",
            priority=5,
            biome_id=biome_id,
            region_id=region_id
        )
        
        return {"job_id": job_id, "status": "activation_requested"}
        
    except Exception as e:
        logger.error(f"Error activating biome: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ECS endpoints
@app.get("/ecs/statistics")
async def get_ecs_statistics():
    """Get ECS system statistics."""
    try:
        from world.ecs_state import get_ecs_state
        ecs = get_ecs_state()
        return ecs.get_statistics()
    except Exception as e:
        logger.error(f"Error getting ECS statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Coherence field endpoints
@app.get("/coherence/global")
async def get_global_coherence():
    """Get global coherence state."""
    try:
        from group.coherence_field import get_coherence_field_manager
        field_manager = get_coherence_field_manager()
        return field_manager.get_global_coherence_state()
    except Exception as e:
        logger.error(f"Error getting global coherence: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Include subscription router
app.include_router(subscription_router)


# Run the application
if __name__ == "__main__":
    config = get_config()
    uvicorn.run(
        "api_gateway:app",
        host=config.api_host,
        port=config.api_port,
        reload=config.debug,
        log_level="info"
    )