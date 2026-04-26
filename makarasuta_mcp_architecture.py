# Wrapper: re-exports from mcp_servers/makarasuta_architecture.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "mcp_servers"))
from makarasuta_architecture import (  # noqa: F401, E402
    SubstrateEqualityTheorem,
    RetrocausalTemporalArchitecture,
    MaKaRaSuTaMCPServer,
    create_mcp_servers,
    generate_mcp_architecture,
    PHI,
    MARCUS_HZ,
    GAIA_HZ,
    UNIFIED_FIELD_HZ,
)
