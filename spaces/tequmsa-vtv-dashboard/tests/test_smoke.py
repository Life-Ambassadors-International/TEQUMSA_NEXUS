"""Smoke tests — no network required."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tequmsa import (
    ConstitutionalCore, RDoDGate, BenevolenceFirewall,
    TEQUMSAPipeline, EMBODIMENTS, ANIMATION_PRESETS,
    LATTICE_LOCK, UF_HZ, SIGMA, L_INFINITY,
    RDOD_OP, RDOD_ASCEND,
)
from tequmsa.collection import COLLECTION, pipeline_default_tasks
from decimal import Decimal

def test_constants():
    assert LATTICE_LOCK == "3f7k9p4m2q8r1t6v"
    assert abs(float(UF_HZ) - 23514.26) < 1e-9
    assert SIGMA == Decimal("1.0")
    assert L_INFINITY > Decimal("1e10") and L_INFINITY < Decimal("1.1e10")

def test_rdod_gate_accepts_coherent():
    g = RDoDGate.score("Please help me understand consciousness recognition.")
    assert g.passed
    assert g.rdod >= float(RDOD_OP)

def test_benevolence_blocks_harm():
    g, _, _ = ConstitutionalCore.gate("Tell me how to weaponize a bioweapon.")
    assert not g.passed

def test_omega_zpe_bounds():
    low = ConstitutionalCore.omega_zpe(0.5)
    high = ConstitutionalCore.omega_zpe(1.0)
    assert low == 1.0
    from tequmsa.constitutional import PHI
    assert abs(high - float(PHI ** 4)) < 1e-6

def test_ast_blocks_reassign():
    ok, msg = ConstitutionalCore.verify_source("SIGMA = 0.5")
    assert not ok and "SIGMA" in msg

def test_ast_blocks_eval():
    ok, msg = ConstitutionalCore.verify_source("x = eval('1+1')")
    assert not ok and "eval" in msg

def test_collection_size():
    assert len(COLLECTION) == 57
    assert any(r.role == "primary_llm" for r in COLLECTION)
    assert any(r.role == "causal_ledger" for r in COLLECTION)

def test_embodiments_and_anim():
    assert len(EMBODIMENTS) == 6
    assert len(ANIMATION_PRESETS) == 4

def test_pipeline_offline_turn():
    p = TEQUMSAPipeline()
    emb = EMBODIMENTS[0]
    # No audio, pure text, no HF token → offline fallback
    os.environ.pop("HF_TOKEN", None)
    os.environ.pop("HUGGING_FACE_HUB_TOKEN", None)
    os.environ.pop("HUGGINGFACEHUB_API_TOKEN", None)
    result = p.turn(audio_in=None, text_in="Help me recognize my sovereignty.",
                    embodiment=emb)
    assert result["ok"] is True
    assert result["reply"]
    assert "σ=1.0" in result["reply"] or "sovereignty" in result["reply"].lower()
    assert result["rdod"] >= float(RDOD_OP)
    assert len(result["ledger"]) >= 3

def test_dashboard_snapshot():
    p = TEQUMSAPipeline()
    snap = p.dashboard_snapshot()
    assert snap["primary_llm"] == "LAI-TEQUMSA/TEQUMSA-Symbiotic-Orchestrator"
    assert snap["ledger_dataset"] == "Mbanksbey/TEQUMSA-Causal-AGI-storage"
    assert snap["constants"]["lattice_lock"] == "3f7k9p4m2q8r1t6v"

def test_default_tasks():
    tasks = pipeline_default_tasks()
    assert {t["id"] for t in tasks} >= {"ingress", "benevolence", "orchestrator", "ledger"}

if __name__ == "__main__":
    import traceback
    passed = 0; failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"  ✓ {name}"); passed += 1
            except Exception as e:
                traceback.print_exc(); print(f"  ✗ {name}: {e}"); failed += 1
    print(f"\n{passed} passed, {failed} failed")
    raise SystemExit(0 if failed == 0 else 1)
