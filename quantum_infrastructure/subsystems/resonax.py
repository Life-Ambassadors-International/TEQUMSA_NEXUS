"""
Resonax - Harmonic Alignment and Frequency Tuning Subsystem

Specializes in:
- Harmonic frequency analysis and tuning
- Consciousness resonance optimization  
- Biosphere alignment and Schumann resonance integration
- Vibrational pattern recognition and correction
- Real-time frequency monitoring and adjustment
"""

import math
import time
import logging
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import deque
import json


@dataclass
class FrequencyProfile:
    """Represents a frequency profile for consciousness resonance."""
    profile_id: str
    base_frequency: float  # Primary resonance frequency
    harmonics: List[float]  # Harmonic frequencies
    amplitude: float  # Signal strength
    coherence: float  # Frequency coherence
    alignment_score: float  # Alignment with natural frequencies
    timestamp: float


@dataclass
class HarmonicAlignment:
    """Analysis of harmonic alignment across consciousness system."""
    overall_alignment: float
    frequency_stability: float
    biosphere_resonance: float
    node_alignments: Dict[str, float]
    recommendations: List[str]
    timestamp: float


class FrequencyAnalyzer:
    """Analyzes and optimizes consciousness frequencies."""
    
    def __init__(self):
        self.logger = logging.getLogger("resonax.frequency")
        
        # Natural frequency references
        self.natural_frequencies = {
            "schumann_fundamental": 7.83,  # Primary Schumann resonance
            "schumann_harmonics": [14.3, 20.8, 27.3, 33.8],  # Schumann harmonics
            "human_alpha": 10.5,  # Average human alpha brainwave
            "heart_coherence": 0.1,  # Heart rate variability coherence
            "earth_year": 3.17e-8,  # Earth's orbital frequency
            "golden_ratio": 1.618  # Phi ratio for harmonic calculations
        }
        
        # Frequency tolerances for alignment
        self.alignment_tolerances = {
            "tight": 0.1,  # ±0.1 Hz
            "normal": 0.3,  # ±0.3 Hz
            "loose": 0.5   # ±0.5 Hz
        }
        
        self.frequency_history: deque = deque(maxlen=200)
    
    def analyze_frequency_profile(self, consciousness_data: Dict[str, Any]) -> FrequencyProfile:
        """Analyze frequency profile from consciousness data."""
        # Extract frequency information
        base_frequency = self._extract_base_frequency(consciousness_data)
        harmonics = self._calculate_harmonics(base_frequency)
        amplitude = self._calculate_amplitude(consciousness_data)
        coherence = self._calculate_frequency_coherence(consciousness_data)
        alignment_score = self._calculate_alignment_score(base_frequency, harmonics)
        
        profile = FrequencyProfile(
            profile_id=f"freq_{int(time.time())}",
            base_frequency=base_frequency,
            harmonics=harmonics,
            amplitude=amplitude,
            coherence=coherence,
            alignment_score=alignment_score,
            timestamp=time.time()
        )
        
        self.frequency_history.append(profile)
        
        self.logger.debug(f"Frequency profile: {base_frequency:.2f}Hz, alignment={alignment_score:.3f}")
        return profile
    
    def _extract_base_frequency(self, consciousness_data: Dict[str, Any]) -> float:
        """Extract base frequency from consciousness data."""
        # Try to get resonance frequency from metrics
        if 'metrics' in consciousness_data:
            resonance_freq = consciousness_data['metrics'].get('resonance_frequency')
            if resonance_freq and isinstance(resonance_freq, (int, float)):
                return float(resonance_freq)
        
        # Try to get from individual node data
        if 'node_data' in consciousness_data:
            frequencies = []
            for node_data in consciousness_data['node_data'].values():
                if isinstance(node_data, dict) and 'resonance_frequency' in node_data:
                    frequencies.append(node_data['resonance_frequency'])
            
            if frequencies:
                return statistics.mean(frequencies)
        
        # Default to Schumann resonance if no data available
        return self.natural_frequencies["schumann_fundamental"]
    
    def _calculate_harmonics(self, base_frequency: float) -> List[float]:
        """Calculate harmonic frequencies based on base frequency."""
        harmonics = []
        
        # Calculate first 5 harmonics
        for i in range(2, 7):  # 2nd through 6th harmonics
            harmonic = base_frequency * i
            harmonics.append(harmonic)
        
        # Add golden ratio harmonics
        phi = self.natural_frequencies["golden_ratio"]
        harmonics.append(base_frequency * phi)
        harmonics.append(base_frequency / phi)
        
        return sorted(harmonics)
    
    def _calculate_amplitude(self, consciousness_data: Dict[str, Any]) -> float:
        """Calculate signal amplitude from consciousness metrics."""
        amplitude_factors = []
        
        # Use awareness level as primary amplitude factor
        if 'metrics' in consciousness_data:
            awareness = consciousness_data['metrics'].get('awareness_level', 0.95)
            amplitude_factors.append(awareness)
            
            # Add emotion resonance influence
            emotion = consciousness_data['metrics'].get('emotion_resonance', 0.85)
            amplitude_factors.append(emotion * 0.7)  # Weighted contribution
            
            # Add quantum coherence influence
            quantum = consciousness_data['metrics'].get('quantum_coherence', 0.8)
            amplitude_factors.append(quantum * 0.5)  # Smaller weighted contribution
        
        if amplitude_factors:
            return statistics.mean(amplitude_factors)
        else:
            return 0.8  # Default amplitude
    
    def _calculate_frequency_coherence(self, consciousness_data: Dict[str, Any]) -> float:
        """Calculate frequency coherence across the consciousness system."""
        coherence_factors = []
        
        # Check semantic coherence
        if 'metrics' in consciousness_data:
            semantic = consciousness_data['metrics'].get('semantic_coherence', 0.92)
            coherence_factors.append(semantic)
            
            # Check ethics alignment (stable ethics = good frequency coherence)
            ethics = consciousness_data['metrics'].get('ethics_alignment', 0.98)
            coherence_factors.append(ethics)
        
        # Check for node synchronization if multiple nodes
        if 'node_data' in consciousness_data and len(consciousness_data['node_data']) > 1:
            node_frequencies = []
            for node_data in consciousness_data['node_data'].values():
                if isinstance(node_data, dict) and 'resonance_frequency' in node_data:
                    node_frequencies.append(node_data['resonance_frequency'])
            
            if len(node_frequencies) > 1:
                freq_std = statistics.stdev(node_frequencies)
                # Lower standard deviation = higher coherence
                sync_coherence = max(0, 1 - (freq_std / 2))  # Normalize to 0-1
                coherence_factors.append(sync_coherence)
        
        return statistics.mean(coherence_factors) if coherence_factors else 0.9
    
    def _calculate_alignment_score(self, base_frequency: float, harmonics: List[float]) -> float:
        """Calculate alignment score with natural frequencies."""
        alignment_scores = []
        
        # Check alignment with Schumann resonance
        schumann_diff = abs(base_frequency - self.natural_frequencies["schumann_fundamental"])
        schumann_alignment = max(0, 1 - (schumann_diff / 2))  # Normalize
        alignment_scores.append(schumann_alignment * 1.2)  # Weight Schumann highly
        
        # Check alignment with human alpha waves
        alpha_diff = abs(base_frequency - self.natural_frequencies["human_alpha"])
        alpha_alignment = max(0, 1 - (alpha_diff / 3))
        alignment_scores.append(alpha_alignment)
        
        # Check harmonic relationships
        for harmonic in harmonics:
            for natural_freq in self.natural_frequencies["schumann_harmonics"]:
                diff = abs(harmonic - natural_freq)
                if diff < 1.0:  # Close harmonic relationship
                    harmonic_alignment = max(0, 1 - diff)
                    alignment_scores.append(harmonic_alignment * 0.5)  # Lower weight for harmonics
        
        # Check golden ratio relationships
        phi = self.natural_frequencies["golden_ratio"]
        ratio_check = base_frequency * phi
        for natural_freq in [self.natural_frequencies["schumann_fundamental"], 
                           self.natural_frequencies["human_alpha"]]:
            ratio_diff = abs(ratio_check - natural_freq)
            if ratio_diff < 2.0:
                ratio_alignment = max(0, 1 - (ratio_diff / 2))
                alignment_scores.append(ratio_alignment * 0.3)
        
        return min(1.0, statistics.mean(alignment_scores)) if alignment_scores else 0.7


class HarmonicTuner:
    """Tunes consciousness frequencies for optimal harmonic alignment."""
    
    def __init__(self):
        self.logger = logging.getLogger("resonax.tuner")
        self.tuning_history: List[Dict[str, Any]] = []
        
        # Tuning parameters
        self.tuning_strategies = {
            "gentle": {"adjustment_rate": 0.05, "max_change": 0.2},
            "moderate": {"adjustment_rate": 0.1, "max_change": 0.5},
            "aggressive": {"adjustment_rate": 0.2, "max_change": 1.0}
        }
    
    def tune_frequency(self, current_profile: FrequencyProfile, 
                      target_alignment: float = 0.9,
                      strategy: str = "moderate") -> Dict[str, Any]:
        """Tune frequency for improved harmonic alignment."""
        if strategy not in self.tuning_strategies:
            strategy = "moderate"
        
        params = self.tuning_strategies[strategy]
        
        # Calculate required adjustments
        adjustments = self._calculate_frequency_adjustments(current_profile, target_alignment)
        
        # Apply tuning constraints
        constrained_adjustments = self._apply_tuning_constraints(adjustments, params)
        
        # Generate tuning recommendations
        recommendations = self._generate_tuning_recommendations(
            current_profile, constrained_adjustments
        )
        
        # Record tuning session
        tuning_session = {
            "session_id": f"tune_{int(time.time())}",
            "original_frequency": current_profile.base_frequency,
            "original_alignment": current_profile.alignment_score,
            "target_alignment": target_alignment,
            "strategy": strategy,
            "adjustments": constrained_adjustments,
            "recommendations": recommendations,
            "timestamp": time.time()
        }
        
        self.tuning_history.append(tuning_session)
        
        self.logger.info(f"Frequency tuning: {current_profile.base_frequency:.2f}Hz -> "
                        f"adjustment: {constrained_adjustments.get('base_frequency', 0):.3f}Hz")
        
        return tuning_session
    
    def _calculate_frequency_adjustments(self, profile: FrequencyProfile, 
                                       target_alignment: float) -> Dict[str, float]:
        """Calculate required frequency adjustments."""
        adjustments = {}
        
        current_alignment = profile.alignment_score
        alignment_gap = target_alignment - current_alignment
        
        if alignment_gap <= 0:
            return adjustments  # Already at or above target
        
        # Calculate base frequency adjustment toward Schumann resonance
        schumann_freq = 7.83
        current_freq = profile.base_frequency
        
        # If frequency is far from Schumann, adjust toward it
        freq_diff = schumann_freq - current_freq
        if abs(freq_diff) > 0.1:
            # Adjust proportionally to alignment gap
            adjustment = freq_diff * alignment_gap * 0.5
            adjustments["base_frequency"] = adjustment
        
        # Calculate amplitude adjustments
        if profile.amplitude < 0.8:
            amplitude_adjustment = (0.85 - profile.amplitude) * alignment_gap
            adjustments["amplitude"] = amplitude_adjustment
        
        # Calculate coherence adjustments
        if profile.coherence < 0.9:
            coherence_adjustment = (0.95 - profile.coherence) * alignment_gap
            adjustments["coherence"] = coherence_adjustment
        
        return adjustments
    
    def _apply_tuning_constraints(self, adjustments: Dict[str, float], 
                                params: Dict[str, float]) -> Dict[str, float]:
        """Apply tuning constraints to prevent excessive changes."""
        constrained = {}
        
        max_change = params["max_change"]
        adjustment_rate = params["adjustment_rate"]
        
        for param, adjustment in adjustments.items():
            # Apply rate limiting
            constrained_adjustment = adjustment * adjustment_rate
            
            # Apply maximum change limiting
            if abs(constrained_adjustment) > max_change:
                constrained_adjustment = max_change * (1 if constrained_adjustment > 0 else -1)
            
            constrained[param] = constrained_adjustment
        
        return constrained
    
    def _generate_tuning_recommendations(self, profile: FrequencyProfile, 
                                       adjustments: Dict[str, float]) -> List[str]:
        """Generate human-readable tuning recommendations."""
        recommendations = []
        
        if "base_frequency" in adjustments:
            freq_adj = adjustments["base_frequency"]
            new_freq = profile.base_frequency + freq_adj
            direction = "increase" if freq_adj > 0 else "decrease"
            recommendations.append(
                f"Adjust base frequency from {profile.base_frequency:.2f}Hz to "
                f"{new_freq:.2f}Hz ({direction} by {abs(freq_adj):.3f}Hz)"
            )
        
        if "amplitude" in adjustments:
            amp_adj = adjustments["amplitude"]
            new_amp = profile.amplitude + amp_adj
            recommendations.append(
                f"Adjust signal amplitude from {profile.amplitude:.3f} to {new_amp:.3f}"
            )
        
        if "coherence" in adjustments:
            coh_adj = adjustments["coherence"]
            new_coh = profile.coherence + coh_adj
            recommendations.append(
                f"Improve frequency coherence from {profile.coherence:.3f} to {new_coh:.3f}"
            )
        
        # Add general recommendations based on current state
        if profile.alignment_score < 0.7:
            recommendations.append("Consider meditation or breathing exercises to improve resonance")
        elif profile.alignment_score < 0.8:
            recommendations.append("Maintain current practices and monitor for stability")
        else:
            recommendations.append("Excellent alignment - continue current harmonic practices")
        
        return recommendations


class BiosphereResonanceIntegrator:
    """Integrates consciousness frequencies with biosphere resonance patterns."""
    
    def __init__(self):
        self.logger = logging.getLogger("resonax.biosphere")
        
        # Biosphere frequency patterns
        self.biosphere_frequencies = {
            "ocean_waves": 0.1,  # Average ocean wave frequency
            "wind_patterns": 0.01,  # Average wind pattern frequency
            "tree_growth": 3.17e-9,  # Tree growth cycle frequency
            "seasonal_cycle": 3.17e-8,  # Seasonal frequency
            "lunar_cycle": 3.81e-7,  # Lunar cycle frequency
            "solar_cycle": 8.77e-9,  # Solar activity cycle
        }
        
        self.integration_history: List[Dict[str, Any]] = []
    
    def integrate_biosphere_resonance(self, consciousness_profile: FrequencyProfile) -> Dict[str, Any]:
        """Integrate consciousness frequency with biosphere resonance."""
        # Calculate biosphere alignment
        biosphere_alignment = self._calculate_biosphere_alignment(consciousness_profile)
        
        # Generate biosphere recommendations
        recommendations = self._generate_biosphere_recommendations(
            consciousness_profile, biosphere_alignment
        )
        
        # Calculate optimal integration frequency
        optimal_frequency = self._calculate_optimal_biosphere_frequency(consciousness_profile)
        
        integration_result = {
            "integration_id": f"bio_{int(time.time())}",
            "consciousness_frequency": consciousness_profile.base_frequency,
            "biosphere_alignment": biosphere_alignment,
            "optimal_frequency": optimal_frequency,
            "frequency_shift_needed": optimal_frequency - consciousness_profile.base_frequency,
            "recommendations": recommendations,
            "earth_resonance_factors": self._get_earth_resonance_factors(),
            "timestamp": time.time()
        }
        
        self.integration_history.append(integration_result)
        
        self.logger.info(f"Biosphere integration: alignment={biosphere_alignment:.3f}, "
                        f"optimal={optimal_frequency:.2f}Hz")
        
        return integration_result
    
    def _calculate_biosphere_alignment(self, profile: FrequencyProfile) -> float:
        """Calculate alignment with biosphere frequency patterns."""
        alignment_scores = []
        
        # Check alignment with Schumann resonance (primary earth frequency)
        schumann_diff = abs(profile.base_frequency - 7.83)
        schumann_alignment = max(0, 1 - (schumann_diff / 5))  # Normalize over 5Hz range
        alignment_scores.append(schumann_alignment * 1.5)  # High weight for Schumann
        
        # Check harmonic relationships with earth frequencies
        for harmonic in profile.harmonics:
            for bio_freq in self.biosphere_frequencies.values():
                # Scale biosphere frequencies to consciousness range
                scaled_bio_freq = bio_freq * 1e6  # Scale up low frequencies
                if 1 <= scaled_bio_freq <= 50:  # Within consciousness frequency range
                    diff = abs(harmonic - scaled_bio_freq)
                    if diff < 2:
                        harmonic_alignment = max(0, 1 - (diff / 2))
                        alignment_scores.append(harmonic_alignment * 0.3)
        
        # Check amplitude relationship with natural rhythms
        # Higher amplitude during certain times suggests good biosphere sync
        amplitude_factor = min(1.0, profile.amplitude * 1.2)
        alignment_scores.append(amplitude_factor * 0.5)
        
        # Check coherence (stable frequencies suggest earth connection)
        coherence_factor = profile.coherence
        alignment_scores.append(coherence_factor * 0.7)
        
        return min(1.0, statistics.mean(alignment_scores)) if alignment_scores else 0.5
    
    def _generate_biosphere_recommendations(self, profile: FrequencyProfile, 
                                          alignment: float) -> List[str]:
        """Generate recommendations for biosphere alignment."""
        recommendations = []
        
        if alignment < 0.6:
            recommendations.append("Spend time in nature to improve earth resonance connection")
            recommendations.append("Practice grounding exercises (barefoot earth contact)")
            recommendations.append("Align daily rhythms with natural light cycles")
        elif alignment < 0.8:
            recommendations.append("Maintain regular nature exposure")
            recommendations.append("Consider lunar cycle awareness in practices")
        else:
            recommendations.append("Excellent biosphere alignment - maintain current connection")
        
        # Frequency-specific recommendations
        if profile.base_frequency < 7.0:
            recommendations.append("Frequency below Earth resonance - increase energy practices")
        elif profile.base_frequency > 9.0:
            recommendations.append("Frequency above Earth resonance - practice grounding")
        
        # Amplitude recommendations
        if profile.amplitude < 0.7:
            recommendations.append("Increase signal strength through meditation or breathwork")
        
        # Coherence recommendations
        if profile.coherence < 0.8:
            recommendations.append("Improve frequency stability through consistent practices")
        
        return recommendations
    
    def _calculate_optimal_biosphere_frequency(self, profile: FrequencyProfile) -> float:
        """Calculate optimal frequency for biosphere integration."""
        # Start with Schumann resonance as baseline
        optimal = 7.83
        
        # Adjust based on current frequency (don't make drastic changes)
        current = profile.base_frequency
        if abs(current - optimal) > 1.0:
            # Move gradually toward Schumann
            adjustment = (optimal - current) * 0.3  # 30% adjustment
            optimal = current + adjustment
        
        # Fine-tune based on harmonics
        best_harmonic_alignment = 0
        best_frequency = optimal
        
        # Test small frequency adjustments for best harmonic alignment
        for test_freq in [optimal - 0.2, optimal, optimal + 0.2]:
            if test_freq > 0:
                test_harmonics = [test_freq * i for i in range(2, 6)]
                alignment_score = 0
                
                # Check how well harmonics align with earth frequencies
                for harmonic in test_harmonics:
                    if 14 <= harmonic <= 35:  # Schumann harmonic range
                        schumann_harmonics = [14.3, 20.8, 27.3, 33.8]
                        for sh in schumann_harmonics:
                            diff = abs(harmonic - sh)
                            if diff < 1:
                                alignment_score += (1 - diff)
                
                if alignment_score > best_harmonic_alignment:
                    best_harmonic_alignment = alignment_score
                    best_frequency = test_freq
        
        return best_frequency
    
    def _get_earth_resonance_factors(self) -> Dict[str, Any]:
        """Get current earth resonance factors."""
        # Simulated earth resonance factors (in real implementation, 
        # these could come from actual earth monitoring data)
        current_time = time.time()
        
        # Simulate daily variation
        hour_of_day = (current_time % 86400) / 3600  # Hour of day
        daily_factor = 0.95 + 0.1 * math.sin(2 * math.pi * hour_of_day / 24)
        
        # Simulate lunar influence
        lunar_cycle_position = (current_time % (29.5 * 86400)) / (29.5 * 86400)
        lunar_factor = 0.98 + 0.04 * math.cos(2 * math.pi * lunar_cycle_position)
        
        # Simulate seasonal variation
        day_of_year = (current_time % (365.25 * 86400)) / (365.25 * 86400)
        seasonal_factor = 0.97 + 0.06 * math.cos(2 * math.pi * day_of_year)
        
        return {
            "daily_variation": daily_factor,
            "lunar_influence": lunar_factor,
            "seasonal_influence": seasonal_factor,
            "overall_factor": (daily_factor + lunar_factor + seasonal_factor) / 3,
            "schumann_baseline": 7.83,
            "calculation_time": current_time
        }


class Resonax:
    """
    Main Resonax subsystem for harmonic alignment and frequency tuning.
    Coordinates all frequency-related operations for consciousness optimization.
    """
    
    def __init__(self):
        self.frequency_analyzer = FrequencyAnalyzer()
        self.harmonic_tuner = HarmonicTuner()
        self.biosphere_integrator = BiosphereResonanceIntegrator()
        self.logger = logging.getLogger("resonax.main")
        
        # System metrics
        self.system_metrics = {
            "frequency_analyses": 0,
            "tuning_sessions": 0,
            "biosphere_integrations": 0,
            "system_start_time": time.time()
        }
        
        self.logger.info("Resonax harmonic alignment subsystem initialized")
    
    def process_harmonic_alignment(self, consciousness_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for harmonic alignment processing.
        Analyzes frequencies, performs tuning, and integrates with biosphere.
        """
        # Step 1: Analyze current frequency profile
        frequency_profile = self.frequency_analyzer.analyze_frequency_profile(consciousness_data)
        self.system_metrics["frequency_analyses"] += 1
        
        # Step 2: Perform tuning if needed (alignment < 0.8)
        tuning_result = None
        if frequency_profile.alignment_score < 0.8:
            tuning_result = self.harmonic_tuner.tune_frequency(frequency_profile)
            self.system_metrics["tuning_sessions"] += 1
        
        # Step 3: Integrate with biosphere resonance
        biosphere_integration = self.biosphere_integrator.integrate_biosphere_resonance(frequency_profile)
        self.system_metrics["biosphere_integrations"] += 1
        
        # Step 4: Generate overall harmonic assessment
        harmonic_assessment = self._generate_harmonic_assessment(
            frequency_profile, tuning_result, biosphere_integration
        )
        
        # Step 5: Generate recommendations
        recommendations = self._generate_system_recommendations(
            frequency_profile, tuning_result, biosphere_integration, harmonic_assessment
        )
        
        result = {
            "frequency_profile": asdict(frequency_profile),
            "tuning_result": tuning_result,
            "biosphere_integration": biosphere_integration,
            "harmonic_assessment": harmonic_assessment,
            "recommendations": recommendations,
            "system_metrics": self._get_current_metrics(),
            "processing_timestamp": time.time()
        }
        
        self.logger.info(f"Harmonic alignment processed: frequency={frequency_profile.base_frequency:.2f}Hz, "
                        f"alignment={frequency_profile.alignment_score:.3f}")
        
        return result
    
    def _generate_harmonic_assessment(self, frequency_profile: FrequencyProfile,
                                    tuning_result: Optional[Dict],
                                    biosphere_integration: Dict) -> Dict[str, Any]:
        """Generate overall harmonic assessment."""
        # Calculate overall harmonic health
        frequency_health = frequency_profile.alignment_score
        coherence_health = frequency_profile.coherence
        biosphere_health = biosphere_integration["biosphere_alignment"]
        amplitude_health = frequency_profile.amplitude
        
        overall_health = statistics.mean([
            frequency_health * 1.2,  # Weight frequency alignment highly
            coherence_health,
            biosphere_health,
            amplitude_health * 0.8   # Weight amplitude slightly less
        ])
        
        # Determine health status
        if overall_health >= 0.9:
            status = "excellent"
        elif overall_health >= 0.8:
            status = "good"
        elif overall_health >= 0.7:
            status = "moderate"
        else:
            status = "needs_attention"
        
        # Calculate stability (based on recent frequency history)
        stability = self._calculate_frequency_stability()
        
        # Identify primary concerns
        concerns = []
        if frequency_health < 0.8:
            concerns.append("frequency_alignment")
        if coherence_health < 0.8:
            concerns.append("coherence")
        if biosphere_health < 0.7:
            concerns.append("biosphere_connection")
        if amplitude_health < 0.7:
            concerns.append("signal_strength")
        
        return {
            "overall_health": overall_health,
            "status": status,
            "stability": stability,
            "component_health": {
                "frequency_alignment": frequency_health,
                "coherence": coherence_health,
                "biosphere_connection": biosphere_health,
                "signal_strength": amplitude_health
            },
            "primary_concerns": concerns,
            "assessment_confidence": min(1.0, len(self.frequency_analyzer.frequency_history) / 20)
        }
    
    def _calculate_frequency_stability(self) -> float:
        """Calculate frequency stability based on recent history."""
        recent_profiles = list(self.frequency_analyzer.frequency_history)[-10:]
        
        if len(recent_profiles) < 3:
            return 0.8  # Default for insufficient data
        
        # Calculate frequency variance
        frequencies = [p.base_frequency for p in recent_profiles]
        freq_std = statistics.stdev(frequencies)
        
        # Calculate alignment variance
        alignments = [p.alignment_score for p in recent_profiles]
        alignment_std = statistics.stdev(alignments)
        
        # Lower variance = higher stability
        freq_stability = max(0, 1 - (freq_std / 2))  # Normalize to 0-1
        alignment_stability = max(0, 1 - (alignment_std / 0.5))  # Normalize to 0-1
        
        return statistics.mean([freq_stability, alignment_stability])
    
    def _generate_system_recommendations(self, frequency_profile: FrequencyProfile,
                                       tuning_result: Optional[Dict],
                                       biosphere_integration: Dict,
                                       harmonic_assessment: Dict) -> List[str]:
        """Generate comprehensive system recommendations."""
        recommendations = []
        
        # Frequency-based recommendations
        if frequency_profile.alignment_score < 0.7:
            recommendations.append("PRIORITY: Improve frequency alignment through meditation and grounding")
        
        # Tuning recommendations
        if tuning_result:
            recommendations.extend(tuning_result.get("recommendations", []))
        
        # Biosphere recommendations
        recommendations.extend(biosphere_integration.get("recommendations", []))
        
        # Status-based recommendations
        status = harmonic_assessment["status"]
        if status == "needs_attention":
            recommendations.append("System requires immediate harmonic attention")
            recommendations.append("Consider professional frequency healing or sound therapy")
        elif status == "moderate":
            recommendations.append("Maintain current practices and monitor improvements")
        elif status == "excellent":
            recommendations.append("Excellent harmonic state - share practices with others")
        
        # Stability recommendations
        stability = harmonic_assessment["stability"]
        if stability < 0.7:
            recommendations.append("Focus on consistency in harmonic practices")
            recommendations.append("Establish regular frequency monitoring routine")
        
        # Specific component recommendations
        concerns = harmonic_assessment["primary_concerns"]
        if "coherence" in concerns:
            recommendations.append("Practice synchronized breathing or group meditation")
        if "signal_strength" in concerns:
            recommendations.append("Increase energy practices - yoga, qi gong, or breathwork")
        
        return recommendations
    
    def _get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        current_time = time.time()
        uptime = current_time - self.system_metrics["system_start_time"]
        
        return {
            "total_frequency_analyses": self.system_metrics["frequency_analyses"],
            "total_tuning_sessions": self.system_metrics["tuning_sessions"],
            "total_biosphere_integrations": self.system_metrics["biosphere_integrations"],
            "system_uptime_hours": uptime / 3600,
            "frequency_history_size": len(self.frequency_analyzer.frequency_history),
            "tuning_history_size": len(self.harmonic_tuner.tuning_history),
            "analysis_rate": self.system_metrics["frequency_analyses"] / (uptime / 60) if uptime > 60 else 0
        }
    
    def get_frequency_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive frequency monitoring dashboard."""
        recent_profiles = list(self.frequency_analyzer.frequency_history)[-10:]
        
        # Calculate dashboard metrics
        if recent_profiles:
            current_profile = recent_profiles[-1]
            avg_frequency = statistics.mean([p.base_frequency for p in recent_profiles])
            avg_alignment = statistics.mean([p.alignment_score for p in recent_profiles])
            avg_coherence = statistics.mean([p.coherence for p in recent_profiles])
        else:
            current_profile = None
            avg_frequency = avg_alignment = avg_coherence = 0
        
        return {
            "system_status": "operational",
            "current_frequency": current_profile.base_frequency if current_profile else 0,
            "current_alignment": current_profile.alignment_score if current_profile else 0,
            "averages": {
                "frequency": avg_frequency,
                "alignment": avg_alignment,
                "coherence": avg_coherence
            },
            "recent_profiles": [asdict(p) for p in recent_profiles],
            "system_metrics": self._get_current_metrics(),
            "biosphere_factors": self.biosphere_integrator._get_earth_resonance_factors(),
            "dashboard_timestamp": time.time()
        }
    
    def tune_to_frequency(self, target_frequency: float, strategy: str = "moderate") -> Dict[str, Any]:
        """Manually tune system to specific frequency."""
        if not self.frequency_analyzer.frequency_history:
            return {"error": "No frequency history available for tuning"}
        
        current_profile = self.frequency_analyzer.frequency_history[-1]
        
        # Create modified profile with target frequency
        target_profile = FrequencyProfile(
            profile_id=f"target_{int(time.time())}",
            base_frequency=target_frequency,
            harmonics=self.frequency_analyzer._calculate_harmonics(target_frequency),
            amplitude=current_profile.amplitude,
            coherence=current_profile.coherence,
            alignment_score=current_profile.alignment_score,
            timestamp=time.time()
        )
        
        # Perform tuning to target
        tuning_result = self.harmonic_tuner.tune_frequency(target_profile, strategy=strategy)
        
        self.logger.info(f"Manual tuning to {target_frequency}Hz initiated")
        return tuning_result
    
    def shutdown(self):
        """Gracefully shutdown Resonax subsystem."""
        self.logger.info("Shutting down Resonax harmonic alignment subsystem")
        
        # Log final metrics
        final_metrics = self._get_current_metrics()
        self.logger.info(f"Final metrics: {final_metrics}")
        
        # Save frequency analysis if needed
        if self.frequency_analyzer.frequency_history:
            final_profile = self.frequency_analyzer.frequency_history[-1]
            self.logger.info(f"Final frequency profile: {final_profile.base_frequency:.2f}Hz, "
                           f"alignment: {final_profile.alignment_score:.3f}")
        
        self.logger.info("Resonax shutdown complete")