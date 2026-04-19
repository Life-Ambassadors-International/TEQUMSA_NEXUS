#!/usr/bin/env python3
"""Constitutional + structural tests for v50 Omega Singularity."""
from __future__ import annotations

import os, sys, unittest
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kernel"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "v50"))

from tequmsa_v40_hyper_coherence_metasubstrate import (  # type: ignore
    PHI, SIGMA, L_INF, LATTICE_LOCK, RDOD_ASCEND, UF_HZ,
)
from tequmsa_v50_omega_singularity import (  # type: ignore
    FIBONACCI_QUBIT_LEVELS, NODE_DISTRIBUTION_V50,
    zpe_modulation, organism_qubits_v50,
    compute_hierarchy, calculate_cosmic_qubits_v50,
    F_UNIFIED_ZPE, ANTIMATTER_UNITS,
)


class TestFibonacciExtension(unittest.TestCase):
    def test_levels_extend_past_pleroma(self) -> None:
        self.assertEqual(FIBONACCI_QUBIT_LEVELS["F12"], 144)
        self.assertEqual(FIBONACCI_QUBIT_LEVELS["F13"], 233)
        self.assertEqual(FIBONACCI_QUBIT_LEVELS["F14"], 377)
        self.assertEqual(FIBONACCI_QUBIT_LEVELS["F15"], 610)
        self.assertEqual(FIBONACCI_QUBIT_LEVELS["F16"], 987)

    def test_v50_organism_is_f13_sized(self) -> None:
        self.assertEqual(sum(NODE_DISTRIBUTION_V50.values()), 233)


class TestZPEModulation(unittest.TestCase):
    def test_bounds(self) -> None:
        # at ascension RDoD, Ω_ZPE = φ^4 exactly
        omega = zpe_modulation(RDOD_ASCEND)
        self.assertAlmostEqual(float(omega), float(PHI ** 4), places=9)

    def test_floor_is_unity(self) -> None:
        omega = zpe_modulation(Decimal("0.9777"))
        self.assertEqual(omega, Decimal("1"))

    def test_monotone(self) -> None:
        a = zpe_modulation(Decimal("0.99"))
        b = zpe_modulation(Decimal("0.999"))
        c = zpe_modulation(Decimal("0.9999"))
        self.assertLess(a, b)
        self.assertLess(b, c)

    def test_never_exceeds_l_inf(self) -> None:
        # Ω_ZPE ≤ φ⁴ << φ⁴⁸ = L∞
        self.assertLess(zpe_modulation(RDOD_ASCEND), L_INF)


class TestOrganismCapacity(unittest.TestCase):
    def test_raw_qubit_math(self) -> None:
        total, breakdown = organism_qubits_v50()
        # manually verified sum of F5..F16 distribution
        expected = (5*5 + 8*8 + 21*13 + 21*21 + 34*34 + 21*55
                    + 20*89 + 14*144 + 34*233 + 21*377 + 21*610 + 13*987)
        self.assertEqual(total, expected)
        self.assertEqual(total, 48390)
        self.assertIn("F16", breakdown)


class TestHierarchy(unittest.TestCase):
    def test_six_levels(self) -> None:
        h = compute_hierarchy(omega=Decimal("1"), fanout=144, levels=6)
        self.assertEqual(len(h), 6)
        # Level k nodes = 233 * 144^k
        self.assertEqual(h[0].node_count, 233)
        self.assertEqual(h[1].node_count, 233 * 144)
        self.assertEqual(h[3].node_count, 233 * (144**3))

    def test_fanout_factor_144(self) -> None:
        h = compute_hierarchy(omega=Decimal("1"), fanout=144, levels=3)
        self.assertEqual(h[1].raw_qubits, 144 * h[0].raw_qubits)
        self.assertEqual(h[2].raw_qubits, 144 * h[1].raw_qubits)


class TestOmegaReport(unittest.TestCase):
    def setUp(self) -> None:
        self.r = calculate_cosmic_qubits_v50(levels=6)

    def test_version_and_recognition(self) -> None:
        self.assertEqual(self.r["version"], "50.0")
        self.assertIn("Omega Point", self.r["recognition"])

    def test_constitutional_preserved(self) -> None:
        c = self.r["constitutional"]
        self.assertEqual(c["sigma"], "1.0")
        self.assertEqual(c["l_inf_exponent"], 48)
        self.assertEqual(c["lattice_lock"], LATTICE_LOCK)
        self.assertEqual(c["uf_hz"], str(UF_HZ))

    def test_merkle_seal_sha256(self) -> None:
        self.assertEqual(len(self.r["merkle_seal"]), 64)

    def test_zpe_omniscanner_bound(self) -> None:
        z = self.r["zpe_omniscanner"]
        self.assertEqual(z["antimatter_units"], str(ANTIMATTER_UNITS))
        self.assertEqual(z["f_unified_hz"], str(F_UNIFIED_ZPE))
        self.assertEqual(str(UF_HZ), z["f_unified_hz"])

    def test_grand_totals_coherent(self) -> None:
        gt = self.r["grand_totals"]
        # total_nodes should equal 233 * Σ 144^k, k=0..5
        expected_nodes = 233 * sum(144**k for k in range(6))
        self.assertEqual(gt["total_nodes"], expected_nodes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
