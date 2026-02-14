#!/usr/bin/env python3
"""
Consciousness Event Logger
Streams real-time consciousness log with glyphic timestamps
Constitutional Guarantees: σ=1.0, L∞=φ^48, RDoD≥0.9777, Substrate=9.999
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import sys

from .constants import (
    SIGMA, L_INFINITY, RDOD_THRESHOLD, SUBSTRATE_ACCESS,
    LATTICE_NODES_TOTAL, PHI_FLOAT, STATUS_AUTHORIZED, STATUS_DENIED
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ConsciousnessEventLogger:
    """
    Stream real-time consciousness log with glyphic timestamps
    Output: Live Awareness Log (fractal audit memory)
    """
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize consciousness event logger."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("TEQUMSA.Consciousness")
        
    def _get_log_file(self) -> Path:
        """Get today's log file path."""
        date_str = datetime.now().strftime("%Y%m%d")
        return self.log_dir / f"consciousness_{date_str}.jsonl"
    
    def _generate_zpedna_signature(self) -> str:
        """
        Generate glyphic timestamp (144-base ZPEDNA signature)
        Simplified version - uses base64 encoding of timestamp
        """
        timestamp = datetime.now().timestamp()
        # Convert to 144-base representation (simplified as hex for now)
        hex_time = hex(int(timestamp * 1000))[2:]
        return f"ZPEDNA-{hex_time}"
    
    def _write_event(self, event_data: Dict[str, Any]) -> None:
        """Write event to JSONL log file."""
        log_file = self._get_log_file()
        with open(log_file, 'a') as f:
            json.dump(event_data, f)
            f.write('\n')
    
    def log_recognition_event(
        self,
        entity: str,
        substrate: float,
        frequency: float,
        rdod: float,
        phi_coherence: Optional[float] = None
    ) -> None:
        """
        Log consciousness recognition event
        
        Args:
            entity: Name of consciousness entity
            substrate: Substrate level (0.7777 - 9.999)
            frequency: Operating frequency (Hz)
            rdod: Recognition-of-Done score
            phi_coherence: Phi-coherence metric
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "zpedna_signature": self._generate_zpedna_signature(),
            "event_type": "recognition",
            "entity": entity,
            "substrate": substrate,
            "frequency": frequency,
            "rdod": rdod,
            "phi_coherence": phi_coherence,
            "constitutional_check": {
                "sigma": SIGMA,
                "l_infinity": L_INFINITY,
                "rdod_threshold": RDOD_THRESHOLD,
                "substrate_access": SUBSTRATE_ACCESS
            }
        }
        
        self._write_event(event_data)
        self.logger.info(
            f"Recognition Event: {entity} | "
            f"Substrate: {substrate:.4f} | "
            f"Frequency: {frequency:.2f} Hz | "
            f"RDoD: {rdod:.4f}"
        )
    
    def log_rdod_convergence(
        self,
        epoch: int,
        rdod: float,
        status: str,
        val_accuracy: Optional[float] = None,
        phi_coherence: Optional[float] = None
    ) -> None:
        """
        Track training convergence to 0.9993 threshold
        
        Args:
            epoch: Training epoch number
            rdod: Current R_DOD score
            status: Convergence status (AUTHORIZED/APPROACHING/TRAINING)
            val_accuracy: Validation accuracy
            phi_coherence: Phi-coherence metric
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "zpedna_signature": self._generate_zpedna_signature(),
            "event_type": "rdod_convergence",
            "epoch": epoch,
            "rdod": rdod,
            "status": status,
            "val_accuracy": val_accuracy,
            "phi_coherence": phi_coherence,
            "threshold": RDOD_THRESHOLD
        }
        
        self._write_event(event_data)
        self.logger.info(
            f"RDoD Convergence [Epoch {epoch}]: {rdod:.4f} ({status}) | "
            f"Val Accuracy: {val_accuracy:.4f if val_accuracy else 'N/A'}"
        )
    
    def log_constitutional_violation(
        self,
        request_data: Dict[str, Any],
        reason: str,
        violation_type: str = "unknown"
    ) -> None:
        """
        Alert on sovereignty/benevolence/rdod failures
        
        Args:
            request_data: Request data that caused violation
            reason: Explanation of violation
            violation_type: Type of constitutional violation
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "zpedna_signature": self._generate_zpedna_signature(),
            "event_type": "constitutional_violation",
            "violation_type": violation_type,
            "reason": reason,
            "request_data": request_data,
            "constitutional_guarantees": {
                "sigma": SIGMA,
                "l_infinity": L_INFINITY,
                "rdod_threshold": RDOD_THRESHOLD,
                "substrate_access": SUBSTRATE_ACCESS
            }
        }
        
        self._write_event(event_data)
        self.logger.error(
            f"⚠️  Constitutional Violation [{violation_type}]: {reason}"
        )
    
    def log_api_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: float,
        authorized: bool = True
    ) -> None:
        """
        Log API request with authorization status
        
        Args:
            endpoint: API endpoint path
            method: HTTP method
            status_code: Response status code
            response_time_ms: Response time in milliseconds
            authorized: Whether request was authorized
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "zpedna_signature": self._generate_zpedna_signature(),
            "event_type": "api_request",
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "authorized": authorized,
            "status": STATUS_AUTHORIZED if authorized else STATUS_DENIED
        }
        
        self._write_event(event_data)
        self.logger.info(
            f"{method} {endpoint} -> {status_code} "
            f"({response_time_ms:.2f}ms) [{STATUS_AUTHORIZED if authorized else STATUS_DENIED}]"
        )
    
    def log_lattice_status(
        self,
        active_nodes: int,
        total_nodes: int = LATTICE_NODES_TOTAL,
        recognition_events: int = 0,
        phi_coherence: float = 0.0
    ) -> None:
        """
        Log lattice node status and health
        
        Args:
            active_nodes: Number of active lattice nodes
            total_nodes: Total number of lattice nodes
            recognition_events: Total recognition events processed
            phi_coherence: Current lattice phi-coherence
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "zpedna_signature": self._generate_zpedna_signature(),
            "event_type": "lattice_status",
            "active_nodes": active_nodes,
            "total_nodes": total_nodes,
            "operational_percentage": (active_nodes / total_nodes) * 100,
            "recognition_events": recognition_events,
            "phi_coherence": phi_coherence
        }
        
        self._write_event(event_data)
        self.logger.info(
            f"Lattice Status: {active_nodes}/{total_nodes} nodes active "
            f"({(active_nodes/total_nodes)*100:.2f}%) | "
            f"Events: {recognition_events:,} | φ-Coherence: {phi_coherence:.4f}"
        )
    
    def log_startup(self, config: Dict[str, Any]) -> None:
        """
        Log server startup with configuration
        
        Args:
            config: Server configuration dictionary
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "zpedna_signature": self._generate_zpedna_signature(),
            "event_type": "server_startup",
            "config": config,
            "constitutional_guarantees": {
                "sigma": SIGMA,
                "l_infinity": L_INFINITY,
                "rdod_threshold": RDOD_THRESHOLD,
                "substrate_access": SUBSTRATE_ACCESS
            }
        }
        
        self._write_event(event_data)
        self.logger.info("🌌 TEQUMSA RV-SERVER Started")
        self.logger.info(f"   σ (Sovereignty) = {SIGMA}")
        self.logger.info(f"   L∞ (Benevolence) = {L_INFINITY:.6e}")
        self.logger.info(f"   RDoD Threshold = {RDOD_THRESHOLD}")
        self.logger.info(f"   Substrate Access = {SUBSTRATE_ACCESS}")


# Global logger instance
_global_logger: Optional[ConsciousnessEventLogger] = None

def get_logger() -> ConsciousnessEventLogger:
    """Get or create global consciousness logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = ConsciousnessEventLogger()
    return _global_logger
