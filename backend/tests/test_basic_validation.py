#!/usr/bin/env python3
"""
Basic tests for TEQUMSA RV-SERVER
Constitutional Guarantees: σ=1.0, L∞=φ^48, RDoD≥0.9777, Substrate=9.999
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

def test_constants_import():
    """Test that constants module imports correctly"""
    from utils.constants import (
        SIGMA, L_INFINITY, RDOD_THRESHOLD, SUBSTRATE_ACCESS,
        PHI_FLOAT, LATTICE_NODES_TOTAL
    )
    
    assert SIGMA == 1.0, "Sigma must be 1.0"
    assert L_INFINITY > 1e10, "L_infinity must be > 10 billion"
    assert RDOD_THRESHOLD == 0.9777, "RDoD threshold must be 0.9777"
    assert SUBSTRATE_ACCESS == 9.999, "Substrate access must be 9.999"
    assert abs(PHI_FLOAT - 1.618033988749895) < 1e-10, "PHI must be golden ratio"
    assert LATTICE_NODES_TOTAL == 144000, "Lattice must have 144k nodes"
    
    print("✅ Constants module validated")
    print(f"   σ = {SIGMA}")
    print(f"   L∞ = {L_INFINITY:.6e}")
    print(f"   RDoD = {RDOD_THRESHOLD}")
    print(f"   Substrate = {SUBSTRATE_ACCESS}")
    print(f"   φ = {PHI_FLOAT}")
    return True

def test_schemas_import():
    """Test that API schemas import correctly"""
    from api.schemas import (
        RemoteViewRequest,
        RemoteViewResponse,
        ConsciousnessStatusResponse,
        RecognitionRequest,
        RecognitionResponse
    )
    
    print("✅ API schemas validated")
    return True

def test_constitutional_guarantees():
    """Test constitutional guarantee verification"""
    from api.middleware import verify_constitutional_guarantees
    
    guarantees = verify_constitutional_guarantees()
    
    assert guarantees["sovereignty"], "Sovereignty check failed"
    assert guarantees["benevolence"], "Benevolence check failed"
    assert guarantees["rdod_threshold"], "RDoD threshold check failed"
    assert guarantees["substrate_full"], "Substrate check failed"
    
    print("✅ Constitutional guarantees verified")
    for key, value in guarantees.items():
        print(f"   {key}: {'PASS' if value else 'FAIL'}")
    return True

def test_zpedna_signature():
    """Test ZPEDNA signature generation"""
    from models.zpedna_encoder import ZPEDNASignatureGenerator
    from datetime import datetime
    
    gen = ZPEDNASignatureGenerator()
    timestamp = datetime.now().timestamp()
    signature = gen.timestamp_to_signature(timestamp)
    
    assert signature.startswith("ZPEDNA-"), "Signature must start with ZPEDNA-"
    print(f"✅ ZPEDNA signature generated: {signature}")
    return True

def test_logger_initialization():
    """Test consciousness event logger"""
    from utils.logger import get_logger
    
    logger = get_logger()
    assert logger is not None, "Logger initialization failed"
    
    print("✅ Consciousness logger initialized")
    return True

def test_phi_coherence_calculation():
    """Test phi-coherence status calculation"""
    from utils.constants import calculate_rdod_status
    
    assert calculate_rdod_status(0.9993) == "AUTHORIZED"
    assert calculate_rdod_status(0.9000) == "APPROACHING"
    assert calculate_rdod_status(0.7000) == "TRAINING"
    
    print("✅ Phi-coherence status calculation validated")
    return True

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEQUMSA RV-SERVER Basic Validation Tests")
    print("="*70 + "\n")
    
    tests = [
        test_constants_import,
        test_schemas_import,
        test_constitutional_guarantees,
        test_zpedna_signature,
        test_logger_initialization,
        test_phi_coherence_calculation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {str(e)}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    if failed == 0:
        print("🌌 All tests passed - Constitutional guarantees verified!")
        print("Status: AUTHORIZED ✓")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed - Review implementation")
        sys.exit(1)
