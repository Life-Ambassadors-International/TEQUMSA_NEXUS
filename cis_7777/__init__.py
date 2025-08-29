"""
CIS-7777: Cosmic Invitation Stack core package.

Exports:
    psi_switch          -> multiplicative readiness scalar Ψ_switch
    activation_state    -> 0/1 actualization gate
    recursive_gain      -> "quickening" recursion step
    DEFAULT_WEIGHTS (W)
    example_values (V)

Ethos:
    - Ethics-first instrumentation
    - Federated / consent-driven metrics
    - Minimal, auditable math core
"""
from .psi_switch import (
    psi_switch,
    activation_state,
    recursive_gain,
    W as DEFAULT_WEIGHTS,
    V as example_values,
)

__all__ = [
    "psi_switch",
    "activation_state",
    "recursive_gain",
    "DEFAULT_WEIGHTS",
    "example_values",
]