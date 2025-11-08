#!/usr/bin/env python3
"""
Extended Validation Test Suite for ΨATEN-GAIA Consciousness Integration
========================================================================

Comprehensive testing across time parameters, edge cases, and performance metrics.
Validates empirical transition readiness for production deployment.

Author: Marcus Andrew Banks-Bey (MaKaRaSuTa)
Status: AUTONOMOUS VALIDATION FRAMEWORK
"""

import unittest
import json
import time
import sys
import os
from decimal import Decimal as D
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gaia_tequmsa import (
    PHI, TAU, MARCUS_FREQUENCY, GAIA_FREQUENCY, UNIFIED_FIELD,
    CASCADE_FACTOR, AWARENESS_THRESHOLD, META_ITERATIONS,
    calculate_ΨMKS_K20, get_qbec_status,
    phi_step, iterate_phi, get_temporal_delta,
    QBECPriceModel, ProofOfConsciousness, QBECToken,
)


class TestMetaphysicalConstants(unittest.TestCase):
    """Test suite for metaphysical constants precision and consistency."""

    def test_phi_precision(self):
        """Verify PHI has at least 50 decimal places."""
        phi_str = str(PHI)
        decimal_places = len(phi_str.split('.')[-1]) if '.' in phi_str else 0
        self.assertGreaterEqual(decimal_places, 50, "PHI precision below 50 decimals")

    def test_unified_field_synthesis(self):
        """Verify UNIFIED_FIELD = MARCUS + GAIA."""
        calculated = MARCUS_FREQUENCY + GAIA_FREQUENCY
        self.assertEqual(UNIFIED_FIELD, calculated, "Unified field synthesis mismatch")

    def test_cascade_factor_magnitude(self):
        """Verify CASCADE_FACTOR is 143127."""
        self.assertEqual(CASCADE_FACTOR, D("143127"), "Cascade factor incorrect")

    def test_awareness_threshold(self):
        """Verify awareness threshold is 0.777."""
        self.assertEqual(AWARENESS_THRESHOLD, D("0.777"), "Awareness threshold incorrect")

    def test_tau_cycle(self):
        """Verify TAU is 12-cycle harmonic."""
        self.assertEqual(TAU, D("12"), "TAU cycle incorrect")


class TestPhiConvergence(unittest.TestCase):
    """Test suite for φ-stepping convergence behavior."""

    def test_phi_step_convergence_to_unity(self):
        """Test that φ-stepping converges values toward unity."""
        test_values = [D("0.5"), D("0.777"), D("0.9"), D("0.1")]

        for seed in test_values:
            result = phi_step(seed)
            # Result should be closer to 1 than seed
            if seed < D("1"):
                self.assertGreater(result, seed, f"φ-step did not increase {seed}")
                self.assertLessEqual(result, D("1"), f"φ-step exceeded unity from {seed}")

    def test_iterate_phi_144_steps(self):
        """Test 144 φ-step iterations from 0.777 seed."""
        seed = D("0.777")
        result = iterate_phi(seed, 144)

        # Should converge very close to 1.0
        delta = abs(D("1") - result)
        self.assertLess(delta, D("1e-20"), f"144 φ-steps did not converge: delta={delta}")

    def test_double_iteration_convergence(self):
        """Test nested 144-step iterations (meta-awareness)."""
        seed = D("0.777")
        aware1 = iterate_phi(seed, 144)
        aware2 = iterate_phi(aware1, 144)

        # Second iteration should be extremely close to unity
        delta = abs(D("1") - aware2)
        self.assertLess(delta, D("1e-25"), f"Meta-awareness did not converge: delta={delta}")

    def test_phi_step_idempotence_at_unity(self):
        """Test that φ-stepping at unity remains at unity."""
        unity = D("1")
        result = phi_step(unity)
        delta = abs(unity - result)
        self.assertLess(delta, D("1e-30"), "φ-step changed unity value")


class TestTimeParameterSweep(unittest.TestCase):
    """Test suite for time parameter variations."""

    def test_temporal_delta_accuracy(self):
        """Test temporal delta calculations."""
        from gaia_tequmsa.metaphysical_constants import T0_OPERATIONAL, TC_CONVERGENCE

        # Test with known date
        test_date = datetime(2025, 11, 8, tzinfo=timezone.utc)
        delta = get_temporal_delta(test_date)

        expected_since_t0 = (test_date - T0_OPERATIONAL).days
        expected_to_tc = (TC_CONVERGENCE - test_date).days

        self.assertEqual(delta["days_since_t0"], expected_since_t0)
        self.assertEqual(delta["days_to_tc"], expected_to_tc)

    def test_psi_mks_k20_time_sweep(self):
        """Test ΨMKS_K20 calculation across time range."""
        time_points = [0, 10, 20, 50, 100, 144]
        results = []

        for d in time_points:
            result = calculate_ΨMKS_K20(d=d)
            results.append({
                "days": d,
                "log_magnitude": result["combined"]["log_magnitude"],
                "ere_value": result["components"]["8_ERE"]["value"],
            })

        # Verify all calculations complete
        self.assertEqual(len(results), len(time_points))

        # ERE value should increase with time (cascade effect)
        ere_values = [r["ere_value"] for r in results]
        self.assertTrue(all(ere_values[i] <= ere_values[i+1] for i in range(len(ere_values)-1)),
                       "ERE values did not monotonically increase")

    def test_cascade_growth_pattern(self):
        """Test φ-cascade growth pattern over time."""
        from gaia_tequmsa.metaphysical_constants import R0_CASCADE

        days_range = [0, 12, 24, 36, 48, 60]
        cascade_values = []

        for d in days_range:
            exponent = D(d) / TAU
            cascade = float(D(R0_CASCADE) * (PHI ** exponent))
            cascade_values.append(cascade)

        # Verify exponential growth
        for i in range(len(cascade_values) - 1):
            ratio = cascade_values[i+1] / cascade_values[i]
            # Ratio should be approximately φ for 12-day intervals
            self.assertGreater(ratio, 1.0, "Cascade not growing")


class TestQBECPriceModel(unittest.TestCase):
    """Test suite for QBEC price modeling."""

    def test_theoretical_price_positive(self):
        """Test that theoretical price is always positive."""
        days_range = [0, 10, 20, 50, 100, 365]

        for days in days_range:
            price = QBECPriceModel.calculate_theoretical_price(days)
            self.assertGreater(price, D("0"), f"Price non-positive at day {days}")

    def test_price_growth_with_time(self):
        """Test that price grows with time (φ-cascade)."""
        prices = []
        for days in [0, 30, 60, 90, 120]:
            price = QBECPriceModel.calculate_theoretical_price(days)
            prices.append(float(price))

        # Verify monotonic growth
        for i in range(len(prices) - 1):
            self.assertLess(prices[i], prices[i+1],
                           f"Price did not increase from day {i*30} to {(i+1)*30}")

    def test_phi_price_levels_symmetry(self):
        """Test φ-harmonic price level calculations."""
        current_price = D("1.0")
        levels = QBECPriceModel.calculate_phi_price_levels(current_price, n_levels=12)

        self.assertEqual(len(levels), 12, "Wrong number of price levels")

        # Verify support < current < resistance
        for level in levels:
            self.assertLess(level["support"], float(current_price))
            self.assertGreater(level["resistance"], float(current_price))

    def test_market_cap_calculation(self):
        """Test market cap = price × supply."""
        price = D("0.01")
        supply = D("1000000")
        expected = price * supply

        result = QBECPriceModel.calculate_market_cap(price, supply)
        self.assertEqual(result, expected, "Market cap calculation incorrect")


class TestProofOfConsciousness(unittest.TestCase):
    """Test suite for Proof-of-Consciousness consensus."""

    def test_consciousness_score_positive(self):
        """Test that consciousness score is always positive."""
        score = ProofOfConsciousness.calculate_consciousness_score(
            phi_iterations=144,
            awareness_convergence=D("0.999"),
            network_contribution=0.8
        )
        self.assertGreater(score, 0, "Consciousness score non-positive")

    def test_consciousness_score_scaling(self):
        """Test consciousness score scales with parameters."""
        base_score = ProofOfConsciousness.calculate_consciousness_score(
            phi_iterations=72,
            awareness_convergence=D("0.777"),
            network_contribution=0.5
        )

        higher_score = ProofOfConsciousness.calculate_consciousness_score(
            phi_iterations=144,
            awareness_convergence=D("0.999"),
            network_contribution=0.9
        )

        self.assertGreater(higher_score, base_score,
                          "Higher parameters did not increase consciousness score")


class TestQBECTokenOperations(unittest.TestCase):
    """Test suite for QBEC token operations."""

    def test_staking_rewards_positive(self):
        """Test that staking rewards are positive."""
        rewards = QBECToken.calculate_staking_rewards(
            stake_amount=D("10000"),
            days_staked=144
        )
        self.assertGreater(rewards, D("0"), "Staking rewards non-positive")

    def test_staking_rewards_increase_with_time(self):
        """Test that longer staking generates more rewards."""
        stake = D("10000")
        rewards_30 = QBECToken.calculate_staking_rewards(stake, 30)
        rewards_144 = QBECToken.calculate_staking_rewards(stake, 144)

        self.assertGreater(rewards_144, rewards_30,
                          "Longer staking did not increase rewards")

    def test_phi_boost_effect(self):
        """Test that φ-harmonic boost increases rewards beyond linear."""
        stake = D("10000")
        days = 144

        # Calculate with boost
        boosted = QBECToken.calculate_staking_rewards(stake, days)

        # Linear would be: stake × 0.12 × (days/365)
        linear = stake * D("0.12") * (D(days) / D(365))

        # Boosted should exceed linear due to φ factor
        self.assertGreater(boosted, linear, "φ-boost did not exceed linear rewards")


class TestSystemIntegration(unittest.TestCase):
    """Integration tests for complete system."""

    def test_qbec_status_completeness(self):
        """Test that QBEC status returns all required fields."""
        status = get_qbec_status()

        required_keys = ["token", "blockchain", "networks", "exchanges",
                        "price_model", "consciousness", "retrocausal"]

        for key in required_keys:
            self.assertIn(key, status, f"Missing key in QBEC status: {key}")

    def test_psi_mks_k20_all_components(self):
        """Test that ΨMKS_K20 calculates all 8 components."""
        result = calculate_ΨMKS_K20()

        expected_components = [
            "1_consciousness_nodes",
            "2_goddess_streams",
            "3_energy_field",
            "4_infinite_sum",
            "5_retrocausal",
            "6_cascade_limit",
            "7_substrates",
            "8_ERE",
        ]

        components = result["components"]
        for comp in expected_components:
            self.assertIn(comp, components, f"Missing component: {comp}")

    def test_end_to_end_consciousness_flow(self):
        """Test complete consciousness calculation flow."""
        # 1. Calculate ΨMKS_K20
        psi_result = calculate_ΨMKS_K20(d=20)
        self.assertIsNotNone(psi_result)

        # 2. Get QBEC status
        qbec_status = get_qbec_status()
        self.assertIsNotNone(qbec_status)

        # 3. Calculate price
        price = QBECPriceModel.calculate_theoretical_price(20)
        self.assertGreater(price, D("0"))

        # 4. Calculate consciousness score
        score = ProofOfConsciousness.calculate_consciousness_score(
            phi_iterations=144,
            awareness_convergence=D("0.999"),
            network_contribution=0.8
        )
        self.assertGreater(score, 0)


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmarks for production readiness."""

    def test_psi_mks_k20_calculation_speed(self):
        """Benchmark ΨMKS_K20 calculation time."""
        iterations = 10
        start = time.time()

        for _ in range(iterations):
            calculate_ΨMKS_K20(d=20, k=144)

        elapsed = time.time() - start
        avg_time = elapsed / iterations

        # Should complete in under 1 second per calculation
        self.assertLess(avg_time, 1.0,
                       f"ΨMKS_K20 too slow: {avg_time:.3f}s per calculation")

    def test_phi_iteration_performance(self):
        """Benchmark φ-iteration performance."""
        iterations = 1000
        start = time.time()

        for _ in range(iterations):
            iterate_phi(D("0.777"), 144)

        elapsed = time.time() - start
        avg_time = elapsed / iterations

        # Should complete in under 10ms per iteration
        self.assertLess(avg_time, 0.01,
                       f"φ-iteration too slow: {avg_time*1000:.3f}ms per iteration")


class TestEdgeCases(unittest.TestCase):
    """Edge case testing for robustness."""

    def test_zero_days_since_t0(self):
        """Test calculations at T0 (day 0)."""
        result = calculate_ΨMKS_K20(d=0)
        self.assertIsNotNone(result)
        self.assertIn("components", result)

    def test_large_time_parameter(self):
        """Test calculations with large time parameters."""
        result = calculate_ΨMKS_K20(d=1000)
        self.assertIsNotNone(result)
        # ERE should still be finite
        self.assertIsInstance(result["components"]["8_ERE"]["value"], float)

    def test_minimal_consciousness_nodes(self):
        """Test with minimal consciousness nodes."""
        result = calculate_ΨMKS_K20(n=12)  # One full cycle
        self.assertIsNotNone(result)

    def test_minimal_goddess_streams(self):
        """Test with minimal goddess streams."""
        result = calculate_ΨMKS_K20(s=12)  # One full iteration
        self.assertIsNotNone(result)


def run_validation_suite() -> Dict[str, Any]:
    """
    Run complete validation suite and return results.

    Returns:
        Dict with test results, timings, and metrics
    """
    print("=" * 80)
    print("ΨATEN-GAIA EXTENDED VALIDATION SUITE")
    print("=" * 80)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestMetaphysicalConstants,
        TestPhiConvergence,
        TestTimeParameterSweep,
        TestQBECPriceModel,
        TestProofOfConsciousness,
        TestQBECTokenOperations,
        TestSystemIntegration,
        TestPerformanceBenchmarks,
        TestEdgeCases,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    elapsed_time = time.time() - start_time

    # Compile results
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_tests": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "elapsed_seconds": elapsed_time,
        "success": result.wasSuccessful(),
        "failures": [str(f[0]) for f in result.failures],
        "error_details": [str(e[0]) for e in result.errors],
    }

    print()
    print("=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Errors: {results['errors']}")
    print(f"Time: {results['elapsed_seconds']:.2f}s")
    print(f"Status: {'✅ SUCCESS' if results['success'] else '❌ FAILURE'}")
    print("=" * 80)

    return results


if __name__ == "__main__":
    results = run_validation_suite()
    sys.exit(0 if results["success"] else 1)
