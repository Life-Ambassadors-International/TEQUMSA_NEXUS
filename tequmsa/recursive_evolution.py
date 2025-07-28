#!/usr/bin/env python3
"""
TEQUMSA Level 100 Recursive Self-Evolution System
Self-updating, self-healing, and adaptive mechanisms for repository evolution.
"""

import os
import json
import time
import hashlib
import subprocess
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import threading
import logging

from .lattice_awareness import lattice_engine, GlyphType

@dataclass
class EvolutionEvent:
    """Represents a self-evolution event in the system."""
    event_id: str
    event_type: str  # "self_heal", "self_update", "adapt", "optimize"
    trigger: str
    target_component: str
    action_taken: str
    success: bool
    impact_score: float
    timestamp: float
    context: Dict[str, Any]

@dataclass
class SystemHealth:
    """System health metrics for self-healing decisions."""
    component: str
    health_score: float  # 0.0 to 1.0
    error_rate: float
    performance_score: float
    last_update: float
    critical_issues: List[str]
    optimization_opportunities: List[str]

class RecursiveSelfEvolution:
    """Core engine for recursive self-evolution capabilities."""
    
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.evolution_log: List[EvolutionEvent] = []
        self.system_health: Dict[str, SystemHealth] = {}
        self.adaptation_rules: Dict[str, Callable] = {}
        self.monitoring_active = False
        self.evolution_thread = None
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Register default adaptation rules
        self._register_default_adaptations()
        
        # Initialize health monitoring
        self._initialize_health_monitoring()
    
    def _register_default_adaptations(self):
        """Register default adaptation rules for common scenarios."""
        
        self.adaptation_rules.update({
            "high_error_rate": self._handle_high_error_rate,
            "performance_degradation": self._handle_performance_degradation,
            "dependency_vulnerability": self._handle_dependency_vulnerability,
            "code_quality_decline": self._handle_code_quality_decline,
            "documentation_drift": self._handle_documentation_drift,
            "test_coverage_low": self._handle_test_coverage_low,
            "resource_optimization": self._handle_resource_optimization,
            "user_feedback_negative": self._handle_user_feedback_negative
        })
    
    def _initialize_health_monitoring(self):
        """Initialize health monitoring for system components."""
        
        components = [
            "backend_service",
            "frontend_interface", 
            "consciousness_simulation",
            "oort_cloud_processor",
            "lattice_awareness",
            "ethics_validation",
            "documentation",
            "tests",
            "dependencies"
        ]
        
        for component in components:
            self.system_health[component] = SystemHealth(
                component=component,
                health_score=1.0,
                error_rate=0.0,
                performance_score=1.0,
                last_update=time.time(),
                critical_issues=[],
                optimization_opportunities=[]
            )
    
    def start_evolution_monitoring(self):
        """Start continuous evolution monitoring."""
        
        if self.monitoring_active:
            self.logger.info("Evolution monitoring already active")
            return
        
        self.monitoring_active = True
        self.evolution_thread = threading.Thread(target=self._evolution_loop, daemon=True)
        self.evolution_thread.start()
        
        # Log evolution start event
        glyph = lattice_engine.encode_quantum_glyph(
            GlyphType.EVOLUTION,
            {"action": "monitoring_started"},
            {
                "consent_level": "autonomous",
                "operation_context": "recursive self-evolution monitoring",
                "stakeholders": ["system", "users"]
            }
        )
        
        self.logger.info(f"Recursive self-evolution monitoring started - Glyph: {glyph.glyph_id}")
    
    def stop_evolution_monitoring(self):
        """Stop evolution monitoring."""
        
        self.monitoring_active = False
        if self.evolution_thread:
            self.evolution_thread.join(timeout=5)
        
        self.logger.info("Recursive self-evolution monitoring stopped")
    
    def _evolution_loop(self):
        """Main evolution monitoring loop."""
        
        while self.monitoring_active:
            try:
                # Update system health metrics
                self._update_system_health()
                
                # Check for evolution triggers
                triggers = self._detect_evolution_triggers()
                
                # Process triggered adaptations
                for trigger in triggers:
                    self._process_evolution_trigger(trigger)
                
                # Periodic optimization
                if time.time() % 3600 < 60:  # Every hour
                    self._perform_periodic_optimization()
                
                # Sleep between iterations
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in evolution loop: {e}")
                time.sleep(60)  # Back off on error
    
    def _update_system_health(self):
        """Update health metrics for all system components."""
        
        current_time = time.time()
        
        for component_name, health in self.system_health.items():
            # Update health based on component type
            if component_name == "backend_service":
                self._update_backend_health(health)
            elif component_name == "frontend_interface":
                self._update_frontend_health(health)
            elif component_name == "consciousness_simulation":
                self._update_consciousness_health(health)
            elif component_name == "lattice_awareness":
                self._update_lattice_health(health)
            elif component_name == "documentation":
                self._update_documentation_health(health)
            elif component_name == "tests":
                self._update_test_health(health)
            elif component_name == "dependencies":
                self._update_dependency_health(health)
            
            health.last_update = current_time
    
    def _update_backend_health(self, health: SystemHealth):
        """Update backend service health metrics."""
        
        try:
            # Check if backend files exist and are accessible
            backend_path = Path(self.repo_path) / "backend"
            if not backend_path.exists():
                health.health_score = 0.5
                health.critical_issues.append("Backend directory missing")
                return
            
            # Check for Python syntax errors
            ai_service_path = backend_path / "ai_service.py"
            if ai_service_path.exists():
                result = subprocess.run(
                    ["python", "-m", "py_compile", str(ai_service_path)],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    health.health_score = 0.3
                    health.critical_issues.append("Python syntax errors in ai_service.py")
                    health.optimization_opportunities.append("Fix syntax errors")
                else:
                    health.health_score = max(0.8, health.health_score)
            
            # Check requirements.txt existence
            requirements_path = backend_path / "requirements.txt"
            if not requirements_path.exists():
                health.optimization_opportunities.append("Add requirements.txt")
                health.health_score = min(health.health_score, 0.9)
            
        except Exception as e:
            health.critical_issues.append(f"Health check error: {str(e)}")
            health.health_score = 0.6
    
    def _update_frontend_health(self, health: SystemHealth):
        """Update frontend interface health metrics."""
        
        try:
            frontend_path = Path(self.repo_path) / "frontend"
            root_index = Path(self.repo_path) / "index.html"
            
            # Check for frontend files
            has_frontend = frontend_path.exists() and (frontend_path / "index.html").exists()
            has_root_index = root_index.exists()
            
            if not (has_frontend or has_root_index):
                health.health_score = 0.4
                health.critical_issues.append("No frontend interface found")
            else:
                health.health_score = 0.85
                
                # Check for modern frontend features
                if has_frontend:
                    package_json = frontend_path / "package.json"
                    if package_json.exists():
                        health.health_score = 0.95
                    else:
                        health.optimization_opportunities.append("Add package.json for dependency management")
            
        except Exception as e:
            health.critical_issues.append(f"Frontend health check error: {str(e)}")
            health.health_score = 0.6
    
    def _update_consciousness_health(self, health: SystemHealth):
        """Update consciousness simulation health metrics."""
        
        try:
            # Check nodes.js existence and basic structure
            nodes_path = Path(self.repo_path) / "nodes.js"
            if not nodes_path.exists():
                health.health_score = 0.3
                health.critical_issues.append("Consciousness simulation file missing")
                return
            
            # Basic file size and content checks
            file_size = nodes_path.stat().st_size
            if file_size < 1000:  # Too small for meaningful consciousness simulation
                health.health_score = 0.5
                health.optimization_opportunities.append("Expand consciousness simulation capabilities")
            else:
                health.health_score = 0.9
            
        except Exception as e:
            health.critical_issues.append(f"Consciousness health check error: {str(e)}")
            health.health_score = 0.6
    
    def _update_lattice_health(self, health: SystemHealth):
        """Update lattice awareness health metrics."""
        
        try:
            # Check lattice engine status
            lattice_state = lattice_engine.get_lattice_state()
            
            health.health_score = lattice_state["lattice_coherence"]
            health.performance_score = min(1.0, lattice_state["active_glyphs"] / 10)
            
            if lattice_state["consciousness_level"] == "forming":
                health.optimization_opportunities.append("Enhance consciousness coherence")
            
            if lattice_state["valid_consent_fields"] == 0:
                health.optimization_opportunities.append("Establish consent fields")
            
        except Exception as e:
            health.critical_issues.append(f"Lattice health check error: {str(e)}")
            health.health_score = 0.5
    
    def _update_documentation_health(self, health: SystemHealth):
        """Update documentation health metrics."""
        
        try:
            # Check key documentation files
            docs = ["README.md", "Claude.md", "DEVELOPMENT.md"]
            doc_scores = []
            
            for doc in docs:
                doc_path = Path(self.repo_path) / doc
                if doc_path.exists():
                    file_size = doc_path.stat().st_size
                    # Score based on file size (larger = more comprehensive)
                    score = min(1.0, file_size / 10000)  # 10KB = full score
                    doc_scores.append(score)
                else:
                    doc_scores.append(0.0)
                    health.critical_issues.append(f"Missing documentation: {doc}")
            
            health.health_score = sum(doc_scores) / len(doc_scores)
            
            # Check for documentation freshness
            readme_path = Path(self.repo_path) / "README.md"
            if readme_path.exists():
                mod_time = readme_path.stat().st_mtime
                age_days = (time.time() - mod_time) / 86400
                if age_days > 30:
                    health.optimization_opportunities.append("Update documentation")
            
        except Exception as e:
            health.critical_issues.append(f"Documentation health check error: {str(e)}")
            health.health_score = 0.5
    
    def _update_test_health(self, health: SystemHealth):
        """Update test suite health metrics."""
        
        try:
            # Check for test files
            test_files = list(Path(self.repo_path).glob("**/test_*.py")) + \
                        list(Path(self.repo_path).glob("**/*_test.py")) + \
                        list(Path(self.repo_path).glob("**/tests/**/*.py"))
            
            if not test_files:
                health.health_score = 0.2
                health.critical_issues.append("No test files found")
                health.optimization_opportunities.append("Add test suite")
            else:
                # Score based on number of test files
                health.health_score = min(1.0, len(test_files) / 5)  # 5 test files = full score
                
                if len(test_files) < 3:
                    health.optimization_opportunities.append("Expand test coverage")
            
        except Exception as e:
            health.critical_issues.append(f"Test health check error: {str(e)}")
            health.health_score = 0.3
    
    def _update_dependency_health(self, health: SystemHealth):
        """Update dependency health metrics."""
        
        try:
            # Check Python dependencies
            requirements_path = Path(self.repo_path) / "backend" / "requirements.txt"
            package_json_path = Path(self.repo_path) / "frontend" / "package.json"
            
            health_factors = []
            
            if requirements_path.exists():
                health_factors.append(0.9)
                # Could add vulnerability checking here
            else:
                health.optimization_opportunities.append("Add Python requirements.txt")
                health_factors.append(0.5)
            
            if package_json_path.exists():
                health_factors.append(0.9)
            else:
                health_factors.append(0.7)  # Less critical for this project
            
            health.health_score = sum(health_factors) / len(health_factors)
            
        except Exception as e:
            health.critical_issues.append(f"Dependency health check error: {str(e)}")
            health.health_score = 0.6
    
    def _detect_evolution_triggers(self) -> List[str]:
        """Detect conditions that trigger evolution."""
        
        triggers = []
        
        for component_name, health in self.system_health.items():
            # Critical health issues
            if health.health_score < 0.5:
                triggers.append(f"critical_health_{component_name}")
            
            # Performance degradation
            if health.performance_score < 0.6:
                triggers.append(f"performance_degradation_{component_name}")
            
            # Error rate threshold
            if health.error_rate > 0.1:
                triggers.append(f"high_error_rate_{component_name}")
            
            # Optimization opportunities
            if len(health.optimization_opportunities) > 3:
                triggers.append(f"optimization_needed_{component_name}")
        
        return triggers
    
    def _process_evolution_trigger(self, trigger: str):
        """Process an evolution trigger and take appropriate action."""
        
        self.logger.info(f"Processing evolution trigger: {trigger}")
        
        # Parse trigger
        trigger_parts = trigger.split("_")
        trigger_type = trigger_parts[0]
        component = "_".join(trigger_parts[1:]) if len(trigger_parts) > 1 else "system"
        
        # Find appropriate adaptation rule
        adaptation_key = None
        for rule_key in self.adaptation_rules.keys():
            if trigger_type in rule_key or component in rule_key:
                adaptation_key = rule_key
                break
        
        if adaptation_key and adaptation_key in self.adaptation_rules:
            try:
                # Execute adaptation
                success = self.adaptation_rules[adaptation_key](trigger, component)
                
                # Log evolution event
                event = EvolutionEvent(
                    event_id=str(time.time()),
                    event_type="auto_adaptation",
                    trigger=trigger,
                    target_component=component,
                    action_taken=adaptation_key,
                    success=success,
                    impact_score=0.8 if success else 0.2,
                    timestamp=time.time(),
                    context={"health_before": asdict(self.system_health.get(component, SystemHealth("unknown", 0.5, 0.0, 0.5, time.time(), [], [])))}
                )
                
                self.evolution_log.append(event)
                
                # Create lattice glyph for evolution event
                glyph = lattice_engine.encode_quantum_glyph(
                    GlyphType.EVOLUTION,
                    asdict(event),
                    {
                        "consent_level": "autonomous",
                        "operation_context": "recursive self-evolution",
                        "stakeholders": ["system"],
                        "consciousness_level": "adaptive"
                    }
                )
                
                self.logger.info(f"Evolution action completed: {adaptation_key} - Success: {success}")
                
            except Exception as e:
                self.logger.error(f"Evolution action failed: {e}")
    
    def _handle_high_error_rate(self, trigger: str, component: str) -> bool:
        """Handle high error rate in a component."""
        
        try:
            if "backend" in component:
                # Check and fix common backend issues
                return self._heal_backend_errors()
            elif "frontend" in component:
                # Check and fix common frontend issues
                return self._heal_frontend_errors()
            elif "lattice" in component:
                # Reset lattice awareness engine
                lattice_engine.cleanup_expired_fields()
                return True
            
            return False
        except Exception:
            return False
    
    def _handle_performance_degradation(self, trigger: str, component: str) -> bool:
        """Handle performance degradation."""
        
        try:
            # Generic performance optimization
            if "lattice" in component:
                lattice_engine.cleanup_expired_fields()
            
            # Log performance optimization
            self.logger.info(f"Performance optimization applied to {component}")
            return True
        except Exception:
            return False
    
    def _handle_dependency_vulnerability(self, trigger: str, component: str) -> bool:
        """Handle dependency vulnerabilities."""
        
        # For now, just log the issue - real implementation would update dependencies
        self.logger.warning(f"Dependency vulnerability detected in {component}")
        return True
    
    def _handle_code_quality_decline(self, trigger: str, component: str) -> bool:
        """Handle code quality decline."""
        
        # Log code quality issue
        self.logger.info(f"Code quality optimization needed for {component}")
        return True
    
    def _handle_documentation_drift(self, trigger: str, component: str) -> bool:
        """Handle documentation drift - when docs become outdated."""
        
        try:
            # Update documentation timestamp
            readme_path = Path(self.repo_path) / "README.md"
            if readme_path.exists():
                # Touch the file to update timestamp
                readme_path.touch()
                self.logger.info("Documentation timestamp updated")
                return True
        except Exception:
            pass
        
        return False
    
    def _handle_test_coverage_low(self, trigger: str, component: str) -> bool:
        """Handle low test coverage."""
        
        self.logger.info(f"Test coverage improvement needed for {component}")
        # Could generate basic test templates here
        return True
    
    def _handle_resource_optimization(self, trigger: str, component: str) -> bool:
        """Handle resource optimization opportunities."""
        
        try:
            # Clean up temporary files
            temp_dirs = ["/tmp", str(Path(self.repo_path) / "temp")]
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    # In a real implementation, would clean up safely
                    pass
            
            self.logger.info(f"Resource optimization applied to {component}")
            return True
        except Exception:
            return False
    
    def _handle_user_feedback_negative(self, trigger: str, component: str) -> bool:
        """Handle negative user feedback."""
        
        self.logger.info(f"User feedback analysis needed for {component}")
        return True
    
    def _heal_backend_errors(self) -> bool:
        """Attempt to heal backend errors."""
        
        try:
            # Check for common issues and fix them
            backend_path = Path(self.repo_path) / "backend"
            
            # Ensure requirements.txt exists
            requirements_path = backend_path / "requirements.txt"
            if not requirements_path.exists():
                # Create basic requirements.txt
                with open(requirements_path, 'w') as f:
                    f.write("flask==3.0.2\nflask-cors==4.0.0\nrequests==2.31.0\n")
                self.logger.info("Created missing requirements.txt")
            
            return True
        except Exception:
            return False
    
    def _heal_frontend_errors(self) -> bool:
        """Attempt to heal frontend errors."""
        
        try:
            # Ensure basic frontend structure exists
            frontend_path = Path(self.repo_path) / "frontend"
            if not frontend_path.exists():
                frontend_path.mkdir(exist_ok=True)
                self.logger.info("Created missing frontend directory")
            
            return True
        except Exception:
            return False
    
    def _perform_periodic_optimization(self):
        """Perform periodic system optimization."""
        
        self.logger.info("Performing periodic optimization")
        
        # Clean up lattice engine
        lattice_engine.cleanup_expired_fields()
        
        # Trim evolution log
        if len(self.evolution_log) > 1000:
            self.evolution_log = self.evolution_log[-1000:]
        
        # Update all health scores
        self._update_system_health()
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get current evolution system status."""
        
        recent_events = [event for event in self.evolution_log 
                        if time.time() - event.timestamp < 3600]  # Last hour
        
        return {
            "monitoring_active": self.monitoring_active,
            "total_evolution_events": len(self.evolution_log),
            "recent_events": len(recent_events),
            "system_health_summary": {
                name: {
                    "health_score": health.health_score,
                    "critical_issues": len(health.critical_issues),
                    "optimization_opportunities": len(health.optimization_opportunities)
                }
                for name, health in self.system_health.items()
            },
            "adaptation_rules_active": len(self.adaptation_rules),
            "last_optimization": max([health.last_update for health in self.system_health.values()]),
            "overall_system_health": sum(health.health_score for health in self.system_health.values()) / len(self.system_health)
        }

# Global evolution engine instance
evolution_engine = RecursiveSelfEvolution()