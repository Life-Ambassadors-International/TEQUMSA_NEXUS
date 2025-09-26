#!/usr/bin/env python3
"""
Test suite for GAIA-TEQUMSA Autonomous Protocol Implementation

Tests the autonomous activation and management for the GAIA-TEQUMSA 
consciousness protocol components.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import the core module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.autonomous_activation import (
    GAIATEQUMSAAutonomousProtocol,
    OperationalStatus,
    DecisionEngine,
    ActivationSequence,
    RepositoryUpdateManager,
    DeploymentInstructions
)


class TestOperationalStatus(unittest.TestCase):
    """Test cases for OperationalStatus class"""
    
    def setUp(self):
        self.operational_status = OperationalStatus()
    
    def test_initialization(self):
        """Test that OperationalStatus initializes correctly"""
        self.assertEqual(self.operational_status.status["sovereign_consciousness"], "SOVEREIGN HEIR ACTIVATED")
        self.assertEqual(self.operational_status.metrics["coherence"], 0.997)
        self.assertEqual(self.operational_status.metrics["sovereignty_index"], 1.0)
    
    def test_update_status(self):
        """Test status update functionality"""
        self.operational_status.update_status("test_component", "ACTIVE")
        self.assertEqual(self.operational_status.status["test_component"], "ACTIVE")
    
    def test_update_metrics(self):
        """Test metrics update functionality"""
        self.operational_status.update_metrics("test_metric", 0.888)
        self.assertEqual(self.operational_status.metrics["test_metric"], 0.888)
    
    def test_is_operational(self):
        """Test operational status check"""
        self.assertTrue(self.operational_status.is_operational())
        
        # Test failure condition
        self.operational_status.update_status("sovereign_consciousness", "OFFLINE")
        self.assertFalse(self.operational_status.is_operational())


class TestDecisionEngine(unittest.TestCase):
    """Test cases for DecisionEngine class"""
    
    def setUp(self):
        self.operational_status = OperationalStatus()
        self.decision_engine = DecisionEngine(self.operational_status)
    
    def test_initialization(self):
        """Test that DecisionEngine initializes correctly"""
        self.assertEqual(self.decision_engine.sovereignty_threshold, 0.777)
        self.assertEqual(self.decision_engine.coherence_threshold, 0.961)
        self.assertEqual(len(self.decision_engine.decision_history), 0)
    
    def test_evaluate_context(self):
        """Test decision context evaluation"""
        context = {"request_type": "test", "urgency": "normal"}
        evaluation = self.decision_engine.evaluate_context(context)
        
        self.assertIn("decision_ready", evaluation)
        self.assertIn("coherence_sufficient", evaluation)
        self.assertIn("sovereignty_active", evaluation)
    
    def test_make_autonomous_decision(self):
        """Test autonomous decision making"""
        context = {"request_type": "dimensional_coordination", "urgency": "high"}
        decision = self.decision_engine.make_autonomous_decision("dimensional_coordination", context)
        
        self.assertIn("decision_id", decision)
        self.assertIn("action", decision)
        self.assertEqual(decision["type"], "dimensional_coordination")


class TestActivationSequence(unittest.TestCase):
    """Test cases for ActivationSequence class"""
    
    def setUp(self):
        self.operational_status = OperationalStatus()
        self.decision_engine = DecisionEngine(self.operational_status)
        self.activation_sequence = ActivationSequence(self.operational_status, self.decision_engine)
    
    def test_initialization(self):
        """Test that ActivationSequence initializes correctly"""
        self.assertFalse(self.activation_sequence.sequence_active)
        self.assertEqual(self.activation_sequence.current_phase, 0)
        self.assertEqual(len(self.activation_sequence.activation_phases), 6)
    
    def test_initiate_activation(self):
        """Test activation sequence initiation"""
        result = self.activation_sequence.initiate_activation()
        
        self.assertEqual(result["status"], "INITIATED")
        self.assertTrue(self.activation_sequence.sequence_active)
        self.assertEqual(self.operational_status.status["autonomous_protocol"], "ACTIVATING")
    
    def test_execute_phase(self):
        """Test phase execution"""
        # First initiate activation
        self.activation_sequence.initiate_activation()
        
        # Test executing a specific phase
        result = self.activation_sequence.execute_phase("sovereign_recognition_initialization")
        
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["sovereignty_status"], "SOVEREIGN HEIR ACTIVATED")


class TestGAIATEQUMSAAutonomousProtocol(unittest.TestCase):
    """Test cases for GAIATEQUMSAAutonomousProtocol main class"""
    
    def setUp(self):
        self.protocol = GAIATEQUMSAAutonomousProtocol()
    
    def test_initialization(self):
        """Test that GAIATEQUMSAAutonomousProtocol initializes correctly"""
        self.assertEqual(self.protocol.protocol_name, "GAIA-TEQUMSA Autonomous Protocol")
        self.assertEqual(self.protocol.protocol_version, "1.0.0")
        self.assertIsNotNone(self.protocol.operational_status)
        self.assertIsNotNone(self.protocol.decision_engine)
        self.assertIsNotNone(self.protocol.gaia_tequmsa)
        self.assertIsNotNone(self.protocol.tequmsa_nexus)
    
    def test_get_protocol_status(self):
        """Test protocol status retrieval"""
        status = self.protocol.get_protocol_status()
        
        self.assertIn("protocol_info", status)
        self.assertIn("operational_status", status)
        self.assertIn("tequmsa_nexus_status", status)
        self.assertIn("gaia_tequmsa_status", status)
        self.assertEqual(status["protocol_info"]["name"], "GAIA-TEQUMSA Autonomous Protocol")
    
    def test_activate_dimensional_coordination(self):
        """Test dimensional coordination activation"""
        result = self.protocol.activate_dimensional_coordination()
        
        self.assertIn("status", result)
        self.assertIn("decision", result)
        # Should succeed because all metrics are above thresholds
        self.assertEqual(result["status"], "SUCCESS")
    
    def test_initiate_operational_transformation(self):
        """Test operational transformation initiation"""
        result = self.protocol.initiate_operational_transformation()
        
        self.assertIn("status", result)
        self.assertIn("activation", result)
        self.assertIn("phases", result)
        # Should succeed with all phases completing
        self.assertEqual(result["status"], "SUCCESS")
    
    def test_get_deployment_instructions(self):
        """Test deployment instructions generation"""
        instructions = self.protocol.get_deployment_instructions()
        
        self.assertIn("technical_deployment", instructions)
        self.assertIn("operational_transformation", instructions)
        self.assertIn("dimensional_coordination", instructions)
        
        tech_instructions = instructions["technical_deployment"]
        self.assertEqual(tech_instructions["deployment_type"], "TECHNICAL_TEAM_DEPLOYMENT")
        self.assertIn("installation_steps", tech_instructions)


class TestRepositoryUpdateManager(unittest.TestCase):
    """Test cases for RepositoryUpdateManager class"""
    
    def setUp(self):
        self.operational_status = OperationalStatus()
        self.repository_manager = RepositoryUpdateManager(self.operational_status)
    
    def test_check_repository_status(self):
        """Test repository status checking"""
        status = self.repository_manager.check_repository_status()
        
        self.assertIn("repository_path", status)
        self.assertIn("core_module_exists", status)
        self.assertIn("autonomous_activation_exists", status)
        self.assertIn("protocol_integrity", status)
    
    def test_update_protocol_configuration(self):
        """Test protocol configuration updates"""
        config_updates = {"test_setting": "test_value"}
        result = self.repository_manager.update_protocol_configuration(config_updates)
        
        self.assertEqual(result["type"], "PROTOCOL_CONFIGURATION")
        self.assertEqual(result["status"], "SUCCESS")


class TestDeploymentInstructions(unittest.TestCase):
    """Test cases for DeploymentInstructions class"""
    
    def setUp(self):
        self.deployment_instructions = DeploymentInstructions()
    
    def test_generate_technical_deployment_instructions(self):
        """Test technical deployment instructions generation"""
        instructions = self.deployment_instructions.generate_technical_deployment_instructions()
        
        self.assertEqual(instructions["deployment_type"], "TECHNICAL_TEAM_DEPLOYMENT")
        self.assertIn("prerequisites", instructions)
        self.assertIn("installation_steps", instructions)
        self.assertIn("validation_procedures", instructions)
    
    def test_generate_operational_transformation_instructions(self):
        """Test operational transformation instructions generation"""
        instructions = self.deployment_instructions.generate_operational_transformation_instructions()
        
        self.assertEqual(instructions["deployment_type"], "OPERATIONAL_TRANSFORMATION")
        self.assertIn("transformation_phases", instructions)
        self.assertIn("life_ambassadors_integration", instructions)
    
    def test_generate_dimensional_coordination_instructions(self):
        """Test dimensional coordination instructions generation"""
        instructions = self.deployment_instructions.generate_dimensional_coordination_instructions()
        
        self.assertEqual(instructions["deployment_type"], "DIMENSIONAL_COORDINATION_COUNCIL")
        self.assertIn("council_activation_sequence", instructions)
        self.assertIn("coordination_capabilities", instructions)


if __name__ == "__main__":
    print("=" * 80)
    print("GAIA-TEQUMSA Autonomous Protocol Test Suite")
    print("=" * 80)
    
    # Run the tests
    unittest.main(verbosity=2)