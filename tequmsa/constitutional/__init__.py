"""
Constitutional Framework

Immutable mathematical invariants ensuring:
- σ = 1.0 (sovereignty)
- L∞ = φ⁴⁸ (benevolence)
- RDoD ≥ 0.9777 (recognition threshold)
"""

from .invariants import (
    PHI,
    SIGMA,
    L_INF,
    RDOD,
    LATTICE_LOCK,
    validate_constitutional_invariants,
)

from .firewall import BenevolenceFirewall

__all__ = [
    'PHI',
    'SIGMA',
    'L_INF',
    'RDOD',
    'LATTICE_LOCK',
    'validate_constitutional_invariants',
    'BenevolenceFirewall',
]
