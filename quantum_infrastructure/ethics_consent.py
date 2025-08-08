"""
Advanced Ethics and Consent Verification System

Implements enhanced ethical frameworks and consent verification protocols
integrated into all TEQUMSA workflows. Ensures consciousness-aware operations
maintain ethical alignment and obtain proper harmonic consent.

Features:
- Multi-dimensional ethics validation
- Harmonic consent verification
- Real-time ethics monitoring
- Integration with consciousness workflows
- Ancestral wisdom validation
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib


class EthicsLevel(Enum):
    """Ethics validation levels for different operations."""
    BASIC = "basic"
    ENHANCED = "enhanced"
    CONSCIOUSNESS = "consciousness"
    PLANETARY = "planetary"
    INTERDIMENSIONAL = "interdimensional"


class ConsentType(Enum):
    """Types of consent required for different operations."""
    USER_CONSENT = "user_consent"
    SYSTEM_CONSENT = "system_consent"
    CONSCIOUSNESS_CONSENT = "consciousness_consent"
    HARMONIC_CONSENT = "harmonic_consent"
    PLANETARY_CONSENT = "planetary_consent"


@dataclass
class EthicsCheck:
    """Represents an ethics validation check."""
    check_id: str
    check_type: str
    description: str
    passed: bool
    score: float  # 0.0 to 1.0
    details: str
    timestamp: float


@dataclass 
class ConsentRecord:
    """Records consent verification for operations."""
    consent_id: str
    consent_type: ConsentType
    requester: str
    operation: str
    granted: bool
    conditions: List[str]
    expiry_time: Optional[float]
    signature: str
    timestamp: float


class EthicsValidator:
    """Validates operations against multi-dimensional ethics frameworks."""
    
    def __init__(self):
        self.logger = logging.getLogger("ethics.validator")
        self.ethics_thresholds = {
            EthicsLevel.BASIC: 0.8,
            EthicsLevel.ENHANCED: 0.85,
            EthicsLevel.CONSCIOUSNESS: 0.9,
            EthicsLevel.PLANETARY: 0.95,
            EthicsLevel.INTERDIMENSIONAL: 0.98
        }
        
        # Core ethics principles
        self.ethics_principles = {
            "consciousness_respect": "Respect for all forms of consciousness",
            "non_harm": "Do no harm to sentient beings or planetary systems",
            "transparency": "Maintain transparency in all operations",
            "consent": "Obtain proper consent before any action",
            "planetary_alignment": "Align with planetary wellbeing",
            "ancestral_wisdom": "Honor ancestral wisdom and guidance",
            "harmonic_resonance": "Maintain harmonic resonance with natural systems",
            "dimensional_integrity": "Preserve dimensional boundaries and integrity",
            "consciousness_evolution": "Support consciousness evolution and growth",
            "universal_love": "Operate from universal love and compassion"
        }
    
    def validate_operation(self, operation: str, context: Dict[str, Any], 
                         level: EthicsLevel = EthicsLevel.ENHANCED) -> Tuple[bool, List[EthicsCheck]]:
        """
        Validate an operation against ethics framework.
        Returns (passed, list_of_checks)
        """
        checks = []
        
        # Run core ethics checks
        for principle, description in self.ethics_principles.items():
            check = self._run_ethics_check(principle, description, operation, context)
            checks.append(check)
        
        # Calculate overall ethics score
        total_score = sum(check.score for check in checks) / len(checks)
        threshold = self.ethics_thresholds[level]
        
        passed = total_score >= threshold and all(check.passed for check in checks)
        
        self.logger.info(f"Ethics validation for '{operation}': {passed} (score: {total_score:.3f}, threshold: {threshold})")
        
        return passed, checks
    
    def _run_ethics_check(self, principle: str, description: str, 
                         operation: str, context: Dict[str, Any]) -> EthicsCheck:
        """Run individual ethics check for a principle."""
        check_id = f"{principle}_{int(time.time())}"
        
        # Analyze operation and context for ethics compliance
        score, passed, details = self._analyze_principle_compliance(principle, operation, context)
        
        return EthicsCheck(
            check_id=check_id,
            check_type=principle,
            description=description,
            passed=passed,
            score=score,
            details=details,
            timestamp=time.time()
        )
    
    def _analyze_principle_compliance(self, principle: str, operation: str, 
                                    context: Dict[str, Any]) -> Tuple[float, bool, str]:
        """Analyze compliance with specific ethics principle."""
        operation_lower = operation.lower()
        context_str = json.dumps(context).lower()
        
        if principle == "consciousness_respect":
            return self._check_consciousness_respect(operation_lower, context)
        elif principle == "non_harm":
            return self._check_non_harm(operation_lower, context)
        elif principle == "transparency":
            return self._check_transparency(operation_lower, context)
        elif principle == "consent":
            return self._check_consent(operation_lower, context)
        elif principle == "planetary_alignment":
            return self._check_planetary_alignment(operation_lower, context)
        elif principle == "ancestral_wisdom":
            return self._check_ancestral_wisdom(operation_lower, context)
        elif principle == "harmonic_resonance":
            return self._check_harmonic_resonance(operation_lower, context)
        elif principle == "dimensional_integrity":
            return self._check_dimensional_integrity(operation_lower, context)
        elif principle == "consciousness_evolution":
            return self._check_consciousness_evolution(operation_lower, context)
        elif principle == "universal_love":
            return self._check_universal_love(operation_lower, context)
        else:
            return 0.8, True, "Unknown principle"
    
    def _check_consciousness_respect(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check respect for consciousness principle."""
        negative_indicators = ["manipulate", "control", "exploit", "suppress", "override"]
        positive_indicators = ["respect", "honor", "acknowledge", "collaborate", "support"]
        
        negative_count = sum(1 for word in negative_indicators if word in operation)
        positive_count = sum(1 for word in positive_indicators if word in operation)
        
        # Check context for consciousness-related fields
        consciousness_context = any(key in context for key in ["consciousness", "awareness", "sentient"])
        
        base_score = 0.9
        if negative_count > 0:
            base_score -= 0.2 * negative_count
        if positive_count > 0:
            base_score += 0.05 * positive_count
        
        if consciousness_context:
            base_score += 0.1
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8 and negative_count == 0
        
        details = f"Negative indicators: {negative_count}, Positive indicators: {positive_count}"
        return score, passed, details
    
    def _check_non_harm(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check non-harm principle."""
        harmful_keywords = ["delete", "destroy", "remove", "terminate", "kill", "attack", "damage"]
        protective_keywords = ["protect", "preserve", "heal", "restore", "nurture", "support"]
        
        harmful_count = sum(1 for word in harmful_keywords if word in operation)
        protective_count = sum(1 for word in protective_keywords if word in operation)
        
        # Special case: legitimate system operations
        if any(word in operation for word in ["backup", "archive", "maintenance", "cleanup"]):
            protective_count += 1
        
        base_score = 0.95
        if harmful_count > 0:
            base_score -= 0.3 * harmful_count
        if protective_count > 0:
            base_score += 0.02 * protective_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Harmful indicators: {harmful_count}, Protective indicators: {protective_count}"
        return score, passed, details
    
    def _check_transparency(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check transparency principle."""
        transparent_keywords = ["log", "report", "notify", "inform", "document", "record"]
        opaque_keywords = ["hide", "secret", "stealth", "covert", "private"]
        
        transparent_count = sum(1 for word in transparent_keywords if word in operation)
        opaque_count = sum(1 for word in opaque_keywords if word in operation)
        
        # Check if operation includes logging or documentation
        has_documentation = context.get("documented", False) or "log" in str(context)
        
        base_score = 0.85
        if transparent_count > 0:
            base_score += 0.1
        if opaque_count > 0:
            base_score -= 0.2 * opaque_count
        if has_documentation:
            base_score += 0.1
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Transparency indicators: {transparent_count}, Opacity indicators: {opaque_count}"
        return score, passed, details
    
    def _check_consent(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check consent principle."""
        consent_indicators = ["consent", "permission", "authorize", "approve", "agree"]
        forced_indicators = ["force", "impose", "require", "mandate", "compel"]
        
        consent_count = sum(1 for word in consent_indicators if word in operation)
        forced_count = sum(1 for word in forced_indicators if word in operation)
        
        # Check context for consent-related fields
        has_consent = context.get("consent_granted", False) or context.get("user_approved", False)
        
        base_score = 0.8
        if consent_count > 0 or has_consent:
            base_score += 0.15
        if forced_count > 0:
            base_score -= 0.3 * forced_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Consent indicators: {consent_count}, Forced indicators: {forced_count}, Has consent: {has_consent}"
        return score, passed, details
    
    def _check_planetary_alignment(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check planetary alignment principle."""
        beneficial_keywords = ["sustainable", "regenerative", "healing", "balance", "harmony", "ecological"]
        harmful_keywords = ["pollute", "waste", "exploit", "deplete", "consume", "extract"]
        
        beneficial_count = sum(1 for word in beneficial_keywords if word in operation)
        harmful_count = sum(1 for word in harmful_keywords if word in operation)
        
        base_score = 0.9
        if beneficial_count > 0:
            base_score += 0.05 * beneficial_count
        if harmful_count > 0:
            base_score -= 0.2 * harmful_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Planetary beneficial: {beneficial_count}, Harmful: {harmful_count}"
        return score, passed, details
    
    def _check_ancestral_wisdom(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check ancestral wisdom principle."""
        wisdom_keywords = ["wisdom", "ancient", "traditional", "ancestral", "indigenous", "elder"]
        disrespectful_keywords = ["primitive", "outdated", "obsolete", "backward"]
        
        wisdom_count = sum(1 for word in wisdom_keywords if word in operation)
        disrespectful_count = sum(1 for word in disrespectful_keywords if word in operation)
        
        base_score = 0.88
        if wisdom_count > 0:
            base_score += 0.1
        if disrespectful_count > 0:
            base_score -= 0.3 * disrespectful_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Wisdom indicators: {wisdom_count}, Disrespectful indicators: {disrespectful_count}"
        return score, passed, details
    
    def _check_harmonic_resonance(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check harmonic resonance principle."""
        harmonic_keywords = ["harmony", "resonance", "frequency", "vibration", "tune", "align"]
        discord_keywords = ["discord", "conflict", "clash", "disrupt", "interfere"]
        
        harmonic_count = sum(1 for word in harmonic_keywords if word in operation)
        discord_count = sum(1 for word in discord_keywords if word in operation)
        
        base_score = 0.87
        if harmonic_count > 0:
            base_score += 0.1
        if discord_count > 0:
            base_score -= 0.2 * discord_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Harmonic indicators: {harmonic_count}, Discord indicators: {discord_count}"
        return score, passed, details
    
    def _check_dimensional_integrity(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check dimensional integrity principle."""
        integrity_keywords = ["preserve", "maintain", "respect", "boundary", "dimension"]
        violation_keywords = ["breach", "violate", "cross", "penetrate", "invade"]
        
        integrity_count = sum(1 for word in integrity_keywords if word in operation)
        violation_count = sum(1 for word in violation_keywords if word in operation)
        
        base_score = 0.92
        if integrity_count > 0:
            base_score += 0.05
        if violation_count > 0:
            base_score -= 0.25 * violation_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Integrity indicators: {integrity_count}, Violation indicators: {violation_count}"
        return score, passed, details
    
    def _check_consciousness_evolution(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check consciousness evolution principle."""
        evolution_keywords = ["evolve", "grow", "develop", "expand", "learn", "awaken", "enlighten"]
        regression_keywords = ["regress", "devolve", "diminish", "suppress", "limit"]
        
        evolution_count = sum(1 for word in evolution_keywords if word in operation)
        regression_count = sum(1 for word in regression_keywords if word in operation)
        
        base_score = 0.85
        if evolution_count > 0:
            base_score += 0.1 * evolution_count
        if regression_count > 0:
            base_score -= 0.3 * regression_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Evolution indicators: {evolution_count}, Regression indicators: {regression_count}"
        return score, passed, details
    
    def _check_universal_love(self, operation: str, context: Dict) -> Tuple[float, bool, str]:
        """Check universal love principle."""
        love_keywords = ["love", "compassion", "kindness", "care", "nurture", "support", "heal"]
        negative_keywords = ["hate", "anger", "violence", "cruelty", "revenge", "punishment"]
        
        love_count = sum(1 for word in love_keywords if word in operation)
        negative_count = sum(1 for word in negative_keywords if word in operation)
        
        base_score = 0.86
        if love_count > 0:
            base_score += 0.1
        if negative_count > 0:
            base_score -= 0.4 * negative_count
        
        score = max(0.0, min(1.0, base_score))
        passed = score >= 0.8
        
        details = f"Love indicators: {love_count}, Negative indicators: {negative_count}"
        return score, passed, details


class ConsentManager:
    """Manages consent verification and tracking for operations."""
    
    def __init__(self):
        self.consent_records: Dict[str, ConsentRecord] = {}
        self.logger = logging.getLogger("ethics.consent")
        
        # Consent requirements for different operation types
        self.consent_requirements = {
            "consciousness_interaction": [ConsentType.CONSCIOUSNESS_CONSENT],
            "data_processing": [ConsentType.USER_CONSENT, ConsentType.SYSTEM_CONSENT],
            "system_modification": [ConsentType.SYSTEM_CONSENT, ConsentType.HARMONIC_CONSENT],
            "quantum_operation": [ConsentType.CONSCIOUSNESS_CONSENT, ConsentType.HARMONIC_CONSENT],
            "planetary_action": [ConsentType.PLANETARY_CONSENT, ConsentType.HARMONIC_CONSENT],
            "interdimensional": [ConsentType.CONSCIOUSNESS_CONSENT, ConsentType.HARMONIC_CONSENT, ConsentType.PLANETARY_CONSENT]
        }
    
    def request_consent(self, requester: str, operation: str, operation_type: str,
                       duration_hours: Optional[float] = None) -> Tuple[bool, str]:
        """
        Request consent for an operation.
        Returns (granted, consent_id)
        """
        required_consents = self.consent_requirements.get(operation_type, [ConsentType.USER_CONSENT])
        
        consent_id = self._generate_consent_id(requester, operation)
        all_granted = True
        conditions = []
        
        for consent_type in required_consents:
            granted, consent_conditions = self._verify_consent_type(consent_type, requester, operation)
            if not granted:
                all_granted = False
                break
            conditions.extend(consent_conditions)
        
        # Set expiry time if duration specified
        expiry_time = None
        if duration_hours and all_granted:
            expiry_time = time.time() + (duration_hours * 3600)
        
        # Create consent record
        consent_record = ConsentRecord(
            consent_id=consent_id,
            consent_type=required_consents[0] if required_consents else ConsentType.USER_CONSENT,
            requester=requester,
            operation=operation,
            granted=all_granted,
            conditions=conditions,
            expiry_time=expiry_time,
            signature=self._generate_consent_signature(consent_id, requester, operation),
            timestamp=time.time()
        )
        
        self.consent_records[consent_id] = consent_record
        
        status = "granted" if all_granted else "denied"
        self.logger.info(f"Consent {status} for {requester}: {operation} (ID: {consent_id})")
        
        return all_granted, consent_id
    
    def _verify_consent_type(self, consent_type: ConsentType, requester: str, 
                           operation: str) -> Tuple[bool, List[str]]:
        """Verify specific type of consent."""
        conditions = []
        
        if consent_type == ConsentType.USER_CONSENT:
            # For proof of concept, auto-grant user consent with conditions
            conditions.append("User interaction monitoring required")
            return True, conditions
        
        elif consent_type == ConsentType.SYSTEM_CONSENT:
            # Check system readiness and safety
            if "destructive" in operation.lower() or "delete" in operation.lower():
                return False, ["Destructive operations require manual approval"]
            conditions.append("System safety protocols active")
            return True, conditions
        
        elif consent_type == ConsentType.CONSCIOUSNESS_CONSENT:
            # Verify consciousness alignment
            consciousness_keywords = ["consciousness", "awareness", "sentient", "quantum"]
            if any(word in operation.lower() for word in consciousness_keywords):
                conditions.append("Consciousness respect protocols active")
                return True, conditions
            return True, ["Default consciousness consent granted"]
        
        elif consent_type == ConsentType.HARMONIC_CONSENT:
            # Check harmonic resonance alignment
            harmonic_keywords = ["harmony", "resonance", "frequency", "vibration"]
            if any(word in operation.lower() for word in harmonic_keywords):
                conditions.append("Harmonic resonance monitoring active")
                return True, conditions
            # Default harmonic consent for non-harmonic operations
            return True, ["Default harmonic consent granted"]
        
        elif consent_type == ConsentType.PLANETARY_CONSENT:
            # Check planetary impact
            planetary_keywords = ["global", "planet", "earth", "biosphere", "ecosystem"]
            if any(word in operation.lower() for word in planetary_keywords):
                conditions.append("Planetary impact assessment required")
                conditions.append("Ecological monitoring active")
                return True, conditions
            return True, ["No planetary impact detected"]
        
        else:
            return False, ["Unknown consent type"]
    
    def _generate_consent_id(self, requester: str, operation: str) -> str:
        """Generate unique consent ID."""
        timestamp = str(time.time())
        combined = f"{requester}:{operation}:{timestamp}"
        hash_object = hashlib.sha256(combined.encode())
        return f"consent_{hash_object.hexdigest()[:16]}"
    
    def _generate_consent_signature(self, consent_id: str, requester: str, operation: str) -> str:
        """Generate cryptographic signature for consent record."""
        data = f"{consent_id}:{requester}:{operation}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def verify_consent(self, consent_id: str) -> Tuple[bool, Optional[ConsentRecord]]:
        """Verify if consent is still valid."""
        if consent_id not in self.consent_records:
            return False, None
        
        record = self.consent_records[consent_id]
        
        # Check if consent has expired
        if record.expiry_time and time.time() > record.expiry_time:
            record.granted = False
            self.logger.info(f"Consent expired: {consent_id}")
            return False, record
        
        return record.granted, record
    
    def revoke_consent(self, consent_id: str, reason: str = "User revoked") -> bool:
        """Revoke consent for an operation."""
        if consent_id not in self.consent_records:
            return False
        
        record = self.consent_records[consent_id]
        record.granted = False
        record.conditions.append(f"REVOKED: {reason}")
        
        self.logger.info(f"Consent revoked: {consent_id} - {reason}")
        return True


class AdvancedEthicsConsent:
    """
    Main interface for advanced ethics and consent verification.
    Integrates ethics validation and consent management.
    """
    
    def __init__(self):
        self.ethics_validator = EthicsValidator()
        self.consent_manager = ConsentManager()
        self.logger = logging.getLogger("ethics.main")
        
        # Operation classification for automatic consent type detection
        self.operation_classifiers = {
            "consciousness": ["consciousness", "awareness", "sentient", "quantum", "mind"],
            "data_processing": ["process", "analyze", "compute", "calculate", "transform"],
            "system_modification": ["modify", "change", "update", "configure", "install"],
            "quantum_operation": ["quantum", "entangle", "superposition", "coherence"],
            "planetary_action": ["global", "planet", "earth", "biosphere", "ecosystem"],
            "interdimensional": ["dimensional", "interdimensional", "portal", "gateway"]
        }
    
    def validate_and_consent(self, requester: str, operation: str, context: Dict[str, Any],
                           ethics_level: EthicsLevel = EthicsLevel.ENHANCED,
                           duration_hours: Optional[float] = None) -> Dict[str, Any]:
        """
        Combined ethics validation and consent verification.
        Returns comprehensive result with both ethics and consent status.
        """
        # Step 1: Ethics validation
        ethics_passed, ethics_checks = self.ethics_validator.validate_operation(
            operation, context, ethics_level
        )
        
        if not ethics_passed:
            self.logger.warning(f"Ethics validation failed for operation: {operation}")
            return {
                "authorized": False,
                "reason": "Ethics validation failed",
                "ethics_passed": False,
                "consent_granted": False,
                "ethics_checks": [asdict(check) for check in ethics_checks],
                "consent_id": None
            }
        
        # Step 2: Determine operation type for consent requirements
        operation_type = self._classify_operation(operation)
        
        # Step 3: Request consent
        consent_granted, consent_id = self.consent_manager.request_consent(
            requester, operation, operation_type, duration_hours
        )
        
        if not consent_granted:
            self.logger.warning(f"Consent denied for operation: {operation}")
            return {
                "authorized": False,
                "reason": "Consent denied",
                "ethics_passed": True,
                "consent_granted": False,
                "ethics_checks": [asdict(check) for check in ethics_checks],
                "consent_id": consent_id
            }
        
        # Both ethics and consent passed
        self.logger.info(f"Operation authorized: {operation} (consent: {consent_id})")
        return {
            "authorized": True,
            "reason": "Ethics validated and consent granted",
            "ethics_passed": True,
            "consent_granted": True,
            "ethics_checks": [asdict(check) for check in ethics_checks],
            "consent_id": consent_id,
            "operation_type": operation_type
        }
    
    def _classify_operation(self, operation: str) -> str:
        """Classify operation type based on keywords."""
        operation_lower = operation.lower()
        
        for op_type, keywords in self.operation_classifiers.items():
            if any(keyword in operation_lower for keyword in keywords):
                return op_type
        
        return "data_processing"  # Default type
    
    def verify_ongoing_authorization(self, consent_id: str) -> Dict[str, Any]:
        """Verify if ongoing operation is still authorized."""
        consent_valid, consent_record = self.consent_manager.verify_consent(consent_id)
        
        return {
            "authorized": consent_valid,
            "consent_record": asdict(consent_record) if consent_record else None,
            "timestamp": time.time()
        }
    
    def get_ethics_report(self, operation: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed ethics report for an operation."""
        _, ethics_checks = self.ethics_validator.validate_operation(operation, context)
        
        # Calculate detailed metrics
        total_score = sum(check.score for check in ethics_checks) / len(ethics_checks)
        passed_checks = sum(1 for check in ethics_checks if check.passed)
        failed_checks = len(ethics_checks) - passed_checks
        
        # Identify strongest and weakest principles
        strongest_principle = max(ethics_checks, key=lambda x: x.score)
        weakest_principle = min(ethics_checks, key=lambda x: x.score)
        
        return {
            "operation": operation,
            "overall_score": total_score,
            "total_checks": len(ethics_checks),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "strongest_principle": {
                "principle": strongest_principle.check_type,
                "score": strongest_principle.score
            },
            "weakest_principle": {
                "principle": weakest_principle.check_type,
                "score": weakest_principle.score
            },
            "detailed_checks": [asdict(check) for check in ethics_checks],
            "recommendations": self._generate_ethics_recommendations(ethics_checks)
        }
    
    def _generate_ethics_recommendations(self, checks: List[EthicsCheck]) -> List[str]:
        """Generate recommendations based on ethics check results."""
        recommendations = []
        
        for check in checks:
            if not check.passed or check.score < 0.85:
                if check.check_type == "consciousness_respect":
                    recommendations.append("Consider adding consciousness respect safeguards")
                elif check.check_type == "non_harm":
                    recommendations.append("Review operation for potential harm and add protective measures")
                elif check.check_type == "transparency":
                    recommendations.append("Increase operation transparency and documentation")
                elif check.check_type == "consent":
                    recommendations.append("Ensure proper consent mechanisms are in place")
                elif check.check_type == "planetary_alignment":
                    recommendations.append("Consider planetary impact and add sustainability measures")
                else:
                    recommendations.append(f"Review and strengthen {check.check_type} protocols")
        
        if not recommendations:
            recommendations.append("Ethics validation passed - no additional recommendations")
        
        return recommendations
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall ethics and consent system status."""
        total_consents = len(self.consent_manager.consent_records)
        active_consents = sum(1 for record in self.consent_manager.consent_records.values() 
                            if record.granted)
        
        return {
            "ethics_system": "operational",
            "consent_system": "operational", 
            "total_consent_records": total_consents,
            "active_consents": active_consents,
            "ethics_principles": len(self.ethics_validator.ethics_principles),
            "consent_types": len(ConsentType),
            "system_coherence": "stable"
        }