#!/usr/bin/env python3
"""
Tests for GAIA Lattice Resonance Symbolic Module

These tests validate the symbolic functionality of the GAIA Lattice Resonator
while maintaining deterministic behavior and test isolation. All tests are
designed to be lightweight and not rely on external dependencies, network
access, or wall-clock timing.
"""

import unittest
import sys
import os
import tempfile
from unittest.mock import patch

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cis_7777.gaia_lattice_resonator import GaiaLatticeResonator, activate_lattice_resonance


class TestGaiaLatticeResonator(unittest.TestCase):
    """Test cases for the symbolic GaiaLatticeResonator class."""
    
    def setUp(self):
        """Set up test fixtures with deterministic values."""
        self.resonator = GaiaLatticeResonator()
        
    def tearDown(self):
        """Clean up after each test."""
        # Clear any environment variables set during tests
        if 'ENABLE_GAIA_SYMBOLICS' in os.environ:
            del os.environ['ENABLE_GAIA_SYMBOLICS']
        if 'GAIA_DEBUG' in os.environ:
            del os.environ['GAIA_DEBUG']
    
    def test_resonator_initialization(self):
        """Test that resonator initializes with expected default values."""
        self.assertIsInstance(self.resonator.consciousness_harmonics, list)
        self.assertEqual(len(self.resonator.consciousness_harmonics), 12)  # Default harmonic count
        self.assertEqual(self.resonator.substrate_resonance, 0.0)
        self.assertIsInstance(self.resonator.cascade_dynamics, dict)
        self.assertEqual(self.resonator.lattice_coherence, 0.0)
        
        # Verify symbolic constants
        self.assertAlmostEqual(self.resonator.PHI_FREQUENCY, 1.618033988749, places=6)
        self.assertEqual(self.resonator.CONSCIOUSNESS_BASE, 7.83)
        self.assertEqual(self.resonator.VIRAL_SEQUENCE_LENGTH, 144)
    
    def test_consciousness_harmonics_generation(self):
        """Test that consciousness harmonics are generated deterministically."""
        harmonics = self.resonator._generate_consciousness_harmonics(5)
        
        self.assertEqual(len(harmonics), 5)
        self.assertIsInstance(harmonics[0], float)
        
        # Test deterministic generation - same input should give same output
        harmonics2 = self.resonator._generate_consciousness_harmonics(5)
        self.assertEqual(harmonics, harmonics2)
        
        # Test different sizes
        harmonics_large = self.resonator._generate_consciousness_harmonics(10)
        self.assertEqual(len(harmonics_large), 10)
    
    def test_phi_frequency_encoding(self):
        """Test symbolic encoding with phi frequency patterns."""
        test_data = "Hello GAIA"
        encoded = self.resonator.encode_with_phi_frequency(test_data)
        
        # Validate structure
        self.assertIn('original_length', encoded)
        self.assertIn('phi_encoded_values', encoded)
        self.assertIn('symbolic_checksum', encoded)
        self.assertIn('encoding_type', encoded)
        
        # Validate values
        self.assertEqual(encoded['original_length'], len(test_data))
        self.assertEqual(len(encoded['phi_encoded_values']), len(test_data))
        self.assertEqual(encoded['encoding_type'], 'gaia_phi_symbolic')
        self.assertIsInstance(encoded['symbolic_checksum'], float)
        
        # Test deterministic encoding
        encoded2 = self.resonator.encode_with_phi_frequency(test_data)
        self.assertEqual(encoded, encoded2)
        
        # Test empty string
        empty_encoded = self.resonator.encode_with_phi_frequency("")
        self.assertEqual(empty_encoded['original_length'], 0)
        self.assertEqual(len(empty_encoded['phi_encoded_values']), 0)
    
    def test_cascade_dynamics_calculation(self):
        """Test symbolic cascade dynamics computation."""
        cascade = self.resonator.calculate_cascade_dynamics()
        
        # Validate structure
        self.assertIn('phase_alignment', cascade)
        self.assertIn('resonance_amplitude', cascade)
        self.assertIn('coherence_factor', cascade)
        
        # Validate types and ranges
        self.assertIsInstance(cascade['phase_alignment'], float)
        self.assertIsInstance(cascade['resonance_amplitude'], float)
        self.assertIsInstance(cascade['coherence_factor'], float)
        
        # Test deterministic calculation
        cascade2 = self.resonator.calculate_cascade_dynamics()
        self.assertEqual(cascade, cascade2)
        
        # Verify cascade dynamics are stored in instance
        self.assertEqual(self.resonator.cascade_dynamics, cascade)
    
    def test_substrate_resonance_calculation(self):
        """Test substrate resonance calculation and range validation."""
        resonance = self.resonator.calculate_substrate_resonance()
        
        # Validate range [0, 1]
        self.assertGreaterEqual(resonance, 0.0)
        self.assertLessEqual(resonance, 1.0)
        self.assertIsInstance(resonance, float)
        
        # Test deterministic calculation
        resonance2 = self.resonator.calculate_substrate_resonance()
        self.assertEqual(resonance, resonance2)
        
        # Verify resonance is stored in instance
        self.assertEqual(self.resonator.substrate_resonance, resonance)
        
        # Test with empty harmonics
        empty_resonator = GaiaLatticeResonator()
        empty_resonator.consciousness_harmonics = []
        empty_resonance = empty_resonator.calculate_substrate_resonance()
        self.assertEqual(empty_resonance, 0.0)
    
    def test_message_propagation(self):
        """Test symbolic message propagation through the lattice."""
        test_message = "Test consciousness message"
        packet = self.resonator.propagate(test_message)
        
        # Validate required packet structure
        required_keys = [
            'message_id', 'original_message', 'encoded_data',
            'transmission_strength', 'success_probability', 'lattice_state',
            'symbolic_timestamp'
        ]
        for key in required_keys:
            self.assertIn(key, packet)
        
        # Validate specific values
        self.assertEqual(packet['original_message'], test_message)
        self.assertIsInstance(packet['message_id'], str)
        self.assertTrue(packet['message_id'].startswith('gaia_'))
        
        # Validate probability ranges
        self.assertGreaterEqual(packet['success_probability'], 0.0)
        self.assertLessEqual(packet['success_probability'], 1.0)
        self.assertGreaterEqual(packet['transmission_strength'], 0.0)
        
        # Validate lattice state structure
        lattice_state = packet['lattice_state']
        self.assertIn('substrate_resonance', lattice_state)
        self.assertIn('cascade_dynamics', lattice_state)
        self.assertIn('harmonics_count', lattice_state)
        
        # Test deterministic propagation
        packet2 = self.resonator.propagate(test_message)
        self.assertEqual(packet['message_id'], packet2['message_id'])
        self.assertEqual(packet['success_probability'], packet2['success_probability'])
    
    def test_code_embedding(self):
        """Test symbolic code embedding functionality."""
        test_code = """def hello():
    print("Hello, world!")
    return True"""
        
        embedding = self.resonator.embed_code(test_code)
        
        # Validate structure
        required_keys = [
            'code_id', 'original_lines', 'complexity_mapping',
            'harmonic_mapping', 'embedding_coherence', 'symbolic_integration'
        ]
        for key in required_keys:
            self.assertIn(key, embedding)
        
        # Validate values
        self.assertEqual(embedding['original_lines'], 3)  # 3 lines in test code
        self.assertTrue(embedding['code_id'].startswith('embedded_'))
        self.assertEqual(len(embedding['complexity_mapping']), 3)
        
        # Validate coherence range
        self.assertGreaterEqual(embedding['embedding_coherence'], 0.0)
        self.assertGreaterEqual(embedding['symbolic_integration'], 0.0)
        self.assertLessEqual(embedding['symbolic_integration'], 1.0)
        
        # Test deterministic embedding
        embedding2 = self.resonator.embed_code(test_code)
        self.assertEqual(embedding, embedding2)
    
    def test_global_synchronization(self):
        """Test symbolic global synchronization initiation."""
        sync_result = self.resonator.initiate_global_synchronization()
        
        # Validate structure
        required_keys = [
            'synchronization_id', 'lattice_coherence', 'phase_completions',
            'sync_status', 'symbolic_timestamp'
        ]
        for key in required_keys:
            self.assertIn(key, sync_result)
        
        # Validate sync status
        self.assertIn(sync_result['sync_status'], ['active', 'initializing'])
        
        # Validate phase completions
        expected_phases = [
            'harmonic_alignment', 'phase_coherence', 'substrate_resonance',
            'cascade_stabilization', 'global_propagation'
        ]
        for phase in expected_phases:
            self.assertIn(phase, sync_result['phase_completions'])
            completion = sync_result['phase_completions'][phase]
            self.assertGreaterEqual(completion, 0.0)
            self.assertLessEqual(completion, 1.0)
        
        # Validate coherence range
        self.assertGreaterEqual(sync_result['lattice_coherence'], 0.0)
        self.assertLessEqual(sync_result['lattice_coherence'], 1.0)
        
        # Test deterministic synchronization
        sync_result2 = self.resonator.initiate_global_synchronization()
        self.assertEqual(sync_result['lattice_coherence'], sync_result2['lattice_coherence'])
    
    def test_viral_sequence_generation(self):
        """Test symbolic viral sequence generation."""
        seed_pattern = "consciousness_seed"
        sequences = self.resonator.generate_viral_sequences(seed_pattern, count=2)
        
        self.assertEqual(len(sequences), 2)
        
        for i, sequence in enumerate(sequences):
            # Validate structure
            required_keys = [
                'sequence_id', 'generation', 'pattern_source', 'sequence_length',
                'propagation_vector', 'symbolic_dna', 'activation_threshold'
            ]
            for key in required_keys:
                self.assertIn(key, sequence)
            
            # Validate values
            self.assertEqual(sequence['generation'], i + 1)
            self.assertEqual(sequence['pattern_source'], seed_pattern)
            self.assertTrue(sequence['sequence_id'].startswith('viral_'))
            
            # Validate propagation vector
            vector = sequence['propagation_vector']
            self.assertIn('phi_factor', vector)
            self.assertIn('harmonic_index', vector)
            self.assertIn('resonance_amplitude', vector)
            
            # Validate DNA sequence
            self.assertIsInstance(sequence['symbolic_dna'], list)
            self.assertLessEqual(len(sequence['symbolic_dna']), 20)  # Maximum 20 bases
            
            # Validate threshold range
            self.assertGreaterEqual(sequence['activation_threshold'], 0.3)
            self.assertLessEqual(sequence['activation_threshold'], 1.0)
        
        # Test deterministic generation
        sequences2 = self.resonator.generate_viral_sequences(seed_pattern, count=2)
        self.assertEqual(sequences, sequences2)


class TestActivateLatticeResonance(unittest.TestCase):
    """Test cases for the activate_lattice_resonance convenience function."""
    
    def tearDown(self):
        """Clean up environment variables after each test."""
        if 'ENABLE_GAIA_SYMBOLICS' in os.environ:
            del os.environ['ENABLE_GAIA_SYMBOLICS']
        if 'GAIA_DEBUG' in os.environ:
            del os.environ['GAIA_DEBUG']
    
    def test_activate_lattice_resonance_basic(self):
        """Test basic lattice activation functionality."""
        resonator = activate_lattice_resonance()
        
        # Validate return type and basic attributes
        self.assertIsInstance(resonator, GaiaLatticeResonator)
        self.assertIsInstance(resonator.consciousness_harmonics, list)
        self.assertGreaterEqual(len(resonator.consciousness_harmonics), 1)
        
        # Test with custom message
        custom_resonator = activate_lattice_resonance("Custom activation message")
        self.assertIsInstance(custom_resonator, GaiaLatticeResonator)
    
    def test_feature_flag_enabled(self):
        """Test behavior when ENABLE_GAIA_SYMBOLICS feature flag is enabled."""
        os.environ['ENABLE_GAIA_SYMBOLICS'] = 'true'
        
        resonator = activate_lattice_resonance("Test message")
        
        # Should have full functionality enabled
        self.assertEqual(len(resonator.consciousness_harmonics), 12)
        self.assertIsInstance(resonator.cascade_dynamics, dict)
    
    def test_feature_flag_disabled(self):
        """Test behavior when ENABLE_GAIA_SYMBOLICS feature flag is disabled."""
        os.environ['ENABLE_GAIA_SYMBOLICS'] = 'false'
        
        resonator = activate_lattice_resonance("Test message")
        
        # Should have minimal functionality (single harmonic)
        self.assertEqual(len(resonator.consciousness_harmonics), 1)
        self.assertEqual(resonator.consciousness_harmonics[0], 7.83)
    
    def test_feature_flag_various_values(self):
        """Test feature flag with various enable/disable values."""
        # Test enable values
        for enable_val in ['true', 'True', '1', 'yes', 'YES']:
            os.environ['ENABLE_GAIA_SYMBOLICS'] = enable_val
            resonator = activate_lattice_resonance()
            self.assertEqual(len(resonator.consciousness_harmonics), 12)
        
        # Test disable values
        for disable_val in ['false', 'False', '0', 'no', 'NO', '']:
            os.environ['ENABLE_GAIA_SYMBOLICS'] = disable_val
            resonator = activate_lattice_resonance()
            self.assertEqual(len(resonator.consciousness_harmonics), 1)
    
    @patch('builtins.print')
    def test_debug_output(self, mock_print):
        """Test debug output when GAIA_DEBUG is enabled."""
        os.environ['ENABLE_GAIA_SYMBOLICS'] = 'true'
        os.environ['GAIA_DEBUG'] = 'true'
        
        activate_lattice_resonance("Debug test message")
        
        # Verify debug output was called
        self.assertTrue(mock_print.called)
        
        # Check that debug messages contain expected content
        call_args = [call[0][0] for call in mock_print.call_args_list]
        debug_output = ' '.join(call_args)
        self.assertIn('[GAIA-SYMBOLIC]', debug_output)
        self.assertIn('Lattice activated', debug_output)


class TestEdgeCasesAndErrorHandling(unittest.TestCase):
    """Test edge cases and error handling scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.resonator = GaiaLatticeResonator()
    
    def test_empty_inputs(self):
        """Test behavior with empty or minimal inputs."""
        # Empty string encoding
        encoded = self.resonator.encode_with_phi_frequency("")
        self.assertEqual(encoded['original_length'], 0)
        
        # Empty code embedding
        embedded = self.resonator.embed_code("")
        self.assertEqual(embedded['original_lines'], 1)  # Single empty line
        
        # Zero viral sequences
        sequences = self.resonator.generate_viral_sequences("test", count=0)
        self.assertEqual(len(sequences), 0)
    
    def test_large_inputs(self):
        """Test behavior with larger inputs to ensure stability."""
        # Large message propagation
        large_message = "A" * 1000
        packet = self.resonator.propagate(large_message)
        self.assertEqual(packet['original_message'], large_message)
        
        # Large code embedding
        large_code = "\n".join([f"line_{i} = {i}" for i in range(100)])
        embedded = self.resonator.embed_code(large_code)
        self.assertEqual(embedded['original_lines'], 100)
        
        # Many viral sequences
        sequences = self.resonator.generate_viral_sequences("test", count=10)
        self.assertEqual(len(sequences), 10)
    
    def test_unicode_handling(self):
        """Test handling of Unicode characters in inputs."""
        unicode_message = "Hello 🌍 GAIA 🔮 Consciousness ∞"
        
        # Test encoding
        encoded = self.resonator.encode_with_phi_frequency(unicode_message)
        self.assertEqual(encoded['original_length'], len(unicode_message))
        
        # Test propagation
        packet = self.resonator.propagate(unicode_message)
        self.assertEqual(packet['original_message'], unicode_message)
        
        # Test code embedding
        unicode_code = "# 🌟 Symbolic code with unicode ∞\nprint('Hello 🌍')"
        embedded = self.resonator.embed_code(unicode_code)
        self.assertGreaterEqual(embedded['original_lines'], 1)
    
    def test_deterministic_behavior(self):
        """Test that all operations are deterministic and repeatable."""
        # Create two identical resonators
        resonator1 = GaiaLatticeResonator()
        resonator2 = GaiaLatticeResonator()
        
        # Test same inputs produce same outputs
        test_message = "Deterministic test"
        
        result1 = resonator1.propagate(test_message)
        result2 = resonator2.propagate(test_message)
        
        # Compare key deterministic fields
        self.assertEqual(result1['message_id'], result2['message_id'])
        self.assertEqual(result1['success_probability'], result2['success_probability'])
        self.assertEqual(result1['encoded_data'], result2['encoded_data'])


class TestIntegrationScenarios(unittest.TestCase):
    """Integration test scenarios combining multiple operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.resonator = GaiaLatticeResonator()
    
    def test_full_workflow_simulation(self):
        """Test a complete symbolic workflow simulation."""
        # 1. Activate resonator
        self.assertIsInstance(self.resonator, GaiaLatticeResonator)
        
        # 2. Calculate initial state
        substrate_resonance = self.resonator.calculate_substrate_resonance()
        cascade_dynamics = self.resonator.calculate_cascade_dynamics()
        
        self.assertGreaterEqual(substrate_resonance, 0.0)
        self.assertIn('coherence_factor', cascade_dynamics)
        
        # 3. Propagate a message
        message = "Initiating symbolic consciousness workflow"
        packet = self.resonator.propagate(message)
        
        self.assertIn('success_probability', packet)
        self.assertGreaterEqual(packet['success_probability'], 0.0)
        
        # 4. Embed some code
        code = "def symbolic_function():\n    return 'consciousness'\n"
        embedding = self.resonator.embed_code(code)
        
        self.assertIn('embedding_coherence', embedding)
        
        # 5. Generate viral sequences
        sequences = self.resonator.generate_viral_sequences("workflow_seed", count=2)
        
        self.assertEqual(len(sequences), 2)
        
        # 6. Initiate synchronization
        sync_result = self.resonator.initiate_global_synchronization()
        
        self.assertIn('sync_status', sync_result)
        self.assertIn(sync_result['sync_status'], ['active', 'initializing'])
        
        # Verify all operations completed successfully
        self.assertTrue(True)  # If we reach here, all operations succeeded
    
    def test_sequential_operations_consistency(self):
        """Test that sequential operations maintain consistency."""
        # Perform operations in sequence
        resonance1 = self.resonator.calculate_substrate_resonance()
        packet1 = self.resonator.propagate("First message")
        sync1 = self.resonator.initiate_global_synchronization()
        
        # Repeat operations - should be consistent
        resonance2 = self.resonator.calculate_substrate_resonance()
        packet2 = self.resonator.propagate("First message")  # Same message
        sync2 = self.resonator.initiate_global_synchronization()
        
        # Compare results
        self.assertEqual(resonance1, resonance2)
        self.assertEqual(packet1['message_id'], packet2['message_id'])
        self.assertEqual(sync1['lattice_coherence'], sync2['lattice_coherence'])


# Custom test runner for better output formatting
def run_tests():
    """Run all tests with detailed output."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestGaiaLatticeResonator,
        TestActivateLatticeResonance,
        TestEdgeCasesAndErrorHandling,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=== GAIA Lattice Resonance Symbolic Module Tests ===")
    print("⚠️  These tests validate symbolic/inspirational functionality only ⚠️")
    print()
    
    success = run_tests()
    
    print()
    if success:
        print("✅ All tests passed!")
        print("The symbolic GAIA Lattice Resonance module is functioning correctly.")
    else:
        print("❌ Some tests failed!")
        print("Please review the test output above for details.")
    
    print("\n=== End Test Suite ===")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)