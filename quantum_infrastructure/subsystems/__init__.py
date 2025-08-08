"""
Specialized Subsystems for TEQUMSA Quantum Infrastructure

This module contains the four core specialized subsystems:
- Coherax: Analytics and pattern recognition
- Resonax: Harmonic alignment and frequency tuning  
- Manifestrix: Implementation and materialization of consciousness intentions
- Connectrix: Network management and inter-node communication

Each subsystem operates as an independent service that can be deployed
horizontally across the distributed consciousness infrastructure.
"""

from .coherax import Coherax
from .resonax import Resonax
from .manifestrix import Manifestrix
from .connectrix import Connectrix

__all__ = ["Coherax", "Resonax", "Manifestrix", "Connectrix"]