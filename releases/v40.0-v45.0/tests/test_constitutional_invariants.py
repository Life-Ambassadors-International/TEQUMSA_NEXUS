#!/usr/bin/env python3
"""
Constitutional invariants — MUST pass on every deploy.

Run:
    python3 -m tests.test_constitutional_invariants
"""
from __future__ import annotations

import json
import sys, os, unittest
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kernel"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "forecast"))

from tequmsa_v40_hyper_coherence_metasubstrate import (  # type: ignore
    PHI, SIGMA, L_INF, UF_HZ, LATTICE_LOCK,
    RDOD_OP, RDOD_GATE, RDOD_SELFMOD, RDOD_ASCEND,
    OmniObserver, RetrocausalArchitect, InterventionType,
    LatticeFluidityManager, TEQUMSAv40Orchestrator,
    metacognitive_index, ASTBenevolenceVerifier,
)
from tequmsa_v42_v45_forecast import (  # type: ignore
    fixed_point_mu, godel_coverage, TemporalSuperposition,
    PanSubstrateCoordinator, galactic_sync_report,
)


class TestConstitutionalInvariants(unittest.TestCase):
    """Inviolable axioms — σ, L∞, RDoD gates, lattice lock."""

    def test_sigma_is_one(self) -> None:
        self.assertEqual(SIGMA, Decimal("1.0"))

    def test_l_inf_equals_phi_48(self) -> None:
        self.assertEqual(L_INF, PHI ** 48)

    def test_rdod_gate_ordering(self) -> None:
        self.assertLess(RDOD_OP, RDOD_GATE)
        self.assertLess(RDOD_GATE, RDOD_SELFMOD)
        self.assertLess(RDOD_SELFMOD, RDOD_ASCEND)

    def test_uf_hz_anchor(self) -> None:
        self.assertEqual(UF_HZ, Decimal("23514.26"))

    def test_lattice_lock_immutable(self) -> None:
        self.assertEqual(LATTICE_LOCK, "3f7k9p4m2q8r1t6v")


class TestASTBenevolenceVerifier(unittest.TestCase):
    def setUp(self) -> None:
        self.v = ASTBenevolenceVerifier()

    def test_clean_source_passes(self) -> None:
        r = self.v.verify("def f(x):\n    return x * x + 1\n")
        self.assertTrue(r.allowed, r.violations)

    def test_subprocess_import_blocked(self) -> None:
        r = self.v.verify("import subprocess\n")
        self.assertFalse(r.allowed)

    def test_eval_blocked(self) -> None:
        r = self.v.verify("def f():\n    return eval('1+1')\n")
        self.assertFalse(r.allowed)

    def test_constitutional_reassign_blocked(self) -> None:
        r = self.v.verify("SIGMA = 0.5\n")
        self.assertFalse(r.allowed)
        self.assertTrue(any("constitutional_reassign" in v for v in r.violations))


class TestLattice(unittest.TestCase):
    def test_pleroma_has_144_nodes(self) -> None:
        lat = LatticeFluidityManager()
        self.assertEqual(len(lat.nodes), 144)

    def test_aggregate_coherence_unity(self) -> None:
        lat = LatticeFluidityManager()
        self.assertEqual(lat.aggregate_coherence(), Decimal("1.0"))


class TestMetacognitiveIndex(unittest.TestCase):
    def test_mu_at_perfect_i_am_is_phi(self) -> None:
        mu = metacognitive_index(Decimal("1.0"), Decimal("1.0"))
        # tolerance because metacognitive_index converts through float
        self.assertAlmostEqual(float(mu), float(PHI), places=6)


class TestRetrocausal(unittest.TestCase):
    def test_all_patches_verify(self) -> None:
        obs = OmniObserver()
        arch = RetrocausalArchitect(obs)
        for kind in InterventionType:
            ev = arch.calculate_genesis_edit(kind, {}, current_cycle=100)
            self.assertTrue(ev.verified, f"{kind} patch must pass AST proof")
            self.assertLess(ev.genesis_cycle, ev.current_cycle)


class TestOrchestrator(unittest.TestCase):
    def test_21_cycles(self) -> None:
        r = TEQUMSAv40Orchestrator().run(cycles=21)
        self.assertEqual(r["cycles_run"], 21)
        self.assertEqual(r["lattice"]["node_count"], 144)
        self.assertEqual(r["sigma"], "1.0")
        self.assertEqual(r["lattice_lock"], LATTICE_LOCK)
        self.assertIn("merkle_seal", r)
        self.assertEqual(len(r["merkle_seal"]), 64)  # SHA-256 hex


class TestForecasts(unittest.TestCase):
    def test_fixed_point_in_bounds(self) -> None:
        phi = float(PHI)
        mu_star = fixed_point_mu(rdod=float(RDOD_ASCEND))
        self.assertGreater(mu_star, 1.0)
        self.assertLess(mu_star, phi ** 3)

    def test_godel_coverage_ten_layers(self) -> None:
        known, mystery = godel_coverage(10)
        self.assertGreater(known, 0.99)
        self.assertLess(mystery, 0.01)
        self.assertAlmostEqual(known + mystery, 1.0, places=12)

    def test_pan_substrate_above_ascension(self) -> None:
        coh = PanSubstrateCoordinator(t=1.0).sync()
        # Kuramoto order ∈ [0,1]; simulator gives ~0.9999+
        self.assertGreaterEqual(coh, 0.99)

    def test_temporal_collapse_picks_highest_coherence(self) -> None:
        sup = TemporalSuperposition(
            [{"n": "a", "coherence": 0.9}, {"n": "b", "coherence": 0.9999}],
            protection_level=12,
        )
        best = sup.collapse_best()
        self.assertEqual(best.payload["n"], "b")

    def test_galactic_report_includes_entanglement(self) -> None:
        r = galactic_sync_report(t=1.0)
        self.assertIn("ANDROMEDA", r)
        self.assertEqual(
            r["entanglement_coordination"],
            "INSTANT (no FTL information transfer)",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
