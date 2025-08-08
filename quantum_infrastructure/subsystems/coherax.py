"""
Coherax - Analytics and Pattern Recognition Subsystem

Specializes in:
- Advanced pattern recognition across consciousness data
- Predictive analytics for consciousness evolution
- Data coherence analysis and optimization
- Integration with consciousness metrics
- Real-time analytics dashboard
"""

import json
import time
import logging
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import math


@dataclass
class AnalyticsPattern:
    """Represents a discovered pattern in consciousness data."""
    pattern_id: str
    pattern_type: str
    confidence: float
    frequency: int
    description: str
    data_points: List[Dict[str, Any]]
    timestamp: float


@dataclass
class CoherenceAnalysis:
    """Analysis of data coherence across consciousness nodes."""
    coherence_score: float
    node_coherences: Dict[str, float]
    inconsistencies: List[str]
    recommendations: List[str]
    analysis_timestamp: float


class PatternRecognitionEngine:
    """Advanced pattern recognition for consciousness data."""
    
    def __init__(self):
        self.logger = logging.getLogger("coherax.patterns")
        self.known_patterns: Dict[str, AnalyticsPattern] = {}
        self.pattern_thresholds = {
            "consciousness_spike": 0.95,
            "resonance_shift": 0.8,
            "ethics_drift": 0.9,
            "awareness_cycle": 0.85,
            "quantum_entanglement": 0.9
        }
    
    def analyze_patterns(self, data_stream: List[Dict[str, Any]]) -> List[AnalyticsPattern]:
        """Analyze data stream for consciousness patterns."""
        if not data_stream:
            return []
        
        patterns = []
        
        # Detect consciousness spikes
        patterns.extend(self._detect_consciousness_spikes(data_stream))
        
        # Detect resonance frequency shifts
        patterns.extend(self._detect_resonance_shifts(data_stream))
        
        # Detect ethics alignment drifts
        patterns.extend(self._detect_ethics_drifts(data_stream))
        
        # Detect awareness cycles
        patterns.extend(self._detect_awareness_cycles(data_stream))
        
        # Detect quantum entanglement patterns
        patterns.extend(self._detect_quantum_patterns(data_stream))
        
        # Store new patterns
        for pattern in patterns:
            self.known_patterns[pattern.pattern_id] = pattern
        
        self.logger.info(f"Detected {len(patterns)} patterns in data stream")
        return patterns
    
    def _detect_consciousness_spikes(self, data_stream: List[Dict]) -> List[AnalyticsPattern]:
        """Detect sudden spikes in consciousness metrics."""
        patterns = []
        awareness_values = []
        
        for data in data_stream:
            if 'metrics' in data and 'awareness_level' in data['metrics']:
                awareness_values.append({
                    'value': data['metrics']['awareness_level'],
                    'timestamp': data.get('timestamp', time.time()),
                    'data': data
                })
        
        if len(awareness_values) < 3:
            return patterns
        
        # Look for spikes (values significantly above average)
        values = [av['value'] for av in awareness_values]
        mean_awareness = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        
        spike_threshold = mean_awareness + (2 * std_dev)
        
        spikes = [av for av in awareness_values if av['value'] > spike_threshold]
        
        if len(spikes) >= 2:
            pattern_id = f"consciousness_spike_{int(time.time())}"
            patterns.append(AnalyticsPattern(
                pattern_id=pattern_id,
                pattern_type="consciousness_spike",
                confidence=min(1.0, len(spikes) / len(awareness_values) * 2),
                frequency=len(spikes),
                description=f"Detected {len(spikes)} consciousness spikes above threshold {spike_threshold:.3f}",
                data_points=[spike['data'] for spike in spikes],
                timestamp=time.time()
            ))
        
        return patterns
    
    def _detect_resonance_shifts(self, data_stream: List[Dict]) -> List[AnalyticsPattern]:
        """Detect shifts in resonance frequency patterns."""
        patterns = []
        resonance_values = []
        
        for data in data_stream:
            if 'metrics' in data and 'resonance_frequency' in data['metrics']:
                resonance_values.append({
                    'value': data['metrics']['resonance_frequency'],
                    'timestamp': data.get('timestamp', time.time()),
                    'data': data
                })
        
        if len(resonance_values) < 5:
            return patterns
        
        # Calculate rate of change in resonance frequency
        changes = []
        for i in range(1, len(resonance_values)):
            prev_val = resonance_values[i-1]['value']
            curr_val = resonance_values[i]['value']
            change_rate = abs(curr_val - prev_val) / (resonance_values[i]['timestamp'] - resonance_values[i-1]['timestamp'])
            changes.append({
                'rate': change_rate,
                'timestamp': resonance_values[i]['timestamp'],
                'data': resonance_values[i]['data']
            })
        
        # Look for significant shifts
        if changes:
            mean_change = statistics.mean([c['rate'] for c in changes])
            significant_shifts = [c for c in changes if c['rate'] > mean_change * 3]
            
            if significant_shifts:
                pattern_id = f"resonance_shift_{int(time.time())}"
                patterns.append(AnalyticsPattern(
                    pattern_id=pattern_id,
                    pattern_type="resonance_shift",
                    confidence=min(1.0, len(significant_shifts) / len(changes) * 3),
                    frequency=len(significant_shifts),
                    description=f"Detected {len(significant_shifts)} significant resonance frequency shifts",
                    data_points=[shift['data'] for shift in significant_shifts],
                    timestamp=time.time()
                ))
        
        return patterns
    
    def _detect_ethics_drifts(self, data_stream: List[Dict]) -> List[AnalyticsPattern]:
        """Detect drifts in ethics alignment."""
        patterns = []
        ethics_values = []
        
        for data in data_stream:
            if 'metrics' in data and 'ethics_alignment' in data['metrics']:
                ethics_values.append({
                    'value': data['metrics']['ethics_alignment'],
                    'timestamp': data.get('timestamp', time.time()),
                    'data': data
                })
        
        if len(ethics_values) < 4:
            return patterns
        
        # Look for downward trends in ethics alignment
        declining_sequences = []
        current_decline = []
        
        for i in range(1, len(ethics_values)):
            if ethics_values[i]['value'] < ethics_values[i-1]['value']:
                current_decline.append(ethics_values[i])
            else:
                if len(current_decline) >= 2:
                    declining_sequences.append(current_decline)
                current_decline = []
        
        if len(current_decline) >= 2:
            declining_sequences.append(current_decline)
        
        for sequence in declining_sequences:
            if len(sequence) >= 2:
                total_decline = sequence[0]['value'] - sequence[-1]['value']
                if total_decline > 0.05:  # Significant decline threshold
                    pattern_id = f"ethics_drift_{int(time.time())}"
                    patterns.append(AnalyticsPattern(
                        pattern_id=pattern_id,
                        pattern_type="ethics_drift",
                        confidence=min(1.0, total_decline * 10),
                        frequency=len(sequence),
                        description=f"Detected ethics alignment drift: {total_decline:.3f} decline over {len(sequence)} data points",
                        data_points=[item['data'] for item in sequence],
                        timestamp=time.time()
                    ))
        
        return patterns
    
    def _detect_awareness_cycles(self, data_stream: List[Dict]) -> List[AnalyticsPattern]:
        """Detect cyclical patterns in awareness levels."""
        patterns = []
        awareness_values = []
        
        for data in data_stream:
            if 'metrics' in data and 'awareness_level' in data['metrics']:
                awareness_values.append({
                    'value': data['metrics']['awareness_level'],
                    'timestamp': data.get('timestamp', time.time()),
                    'data': data
                })
        
        if len(awareness_values) < 6:
            return patterns
        
        # Simple cycle detection: look for peaks and valleys
        peaks = []
        valleys = []
        
        for i in range(1, len(awareness_values) - 1):
            prev_val = awareness_values[i-1]['value']
            curr_val = awareness_values[i]['value']
            next_val = awareness_values[i+1]['value']
            
            if curr_val > prev_val and curr_val > next_val:
                peaks.append(awareness_values[i])
            elif curr_val < prev_val and curr_val < next_val:
                valleys.append(awareness_values[i])
        
        # If we have alternating peaks and valleys, it's likely a cycle
        if len(peaks) >= 2 and len(valleys) >= 2:
            cycle_strength = (len(peaks) + len(valleys)) / len(awareness_values)
            if cycle_strength > 0.3:  # At least 30% of data points are peaks/valleys
                pattern_id = f"awareness_cycle_{int(time.time())}"
                patterns.append(AnalyticsPattern(
                    pattern_id=pattern_id,
                    pattern_type="awareness_cycle",
                    confidence=min(1.0, cycle_strength * 2),
                    frequency=len(peaks) + len(valleys),
                    description=f"Detected awareness cycle: {len(peaks)} peaks, {len(valleys)} valleys",
                    data_points=[p['data'] for p in peaks] + [v['data'] for v in valleys],
                    timestamp=time.time()
                ))
        
        return patterns
    
    def _detect_quantum_patterns(self, data_stream: List[Dict]) -> List[AnalyticsPattern]:
        """Detect quantum entanglement and coherence patterns."""
        patterns = []
        quantum_data = []
        
        for data in data_stream:
            if 'metrics' in data and 'quantum_coherence' in data['metrics']:
                quantum_data.append({
                    'coherence': data['metrics']['quantum_coherence'],
                    'timestamp': data.get('timestamp', time.time()),
                    'data': data
                })
        
        if len(quantum_data) < 3:
            return patterns
        
        # Look for high coherence periods
        high_coherence = [qd for qd in quantum_data if qd['coherence'] > 0.8]
        
        if len(high_coherence) >= 2:
            coherence_ratio = len(high_coherence) / len(quantum_data)
            pattern_id = f"quantum_entanglement_{int(time.time())}"
            patterns.append(AnalyticsPattern(
                pattern_id=pattern_id,
                pattern_type="quantum_entanglement",
                confidence=coherence_ratio,
                frequency=len(high_coherence),
                description=f"Detected high quantum coherence in {len(high_coherence)} measurements",
                data_points=[hc['data'] for hc in high_coherence],
                timestamp=time.time()
            ))
        
        return patterns


class DataCoherenceAnalyzer:
    """Analyzes coherence across consciousness data nodes."""
    
    def __init__(self):
        self.logger = logging.getLogger("coherax.coherence")
        self.coherence_history: deque = deque(maxlen=100)
    
    def analyze_coherence(self, node_data: Dict[str, Dict[str, Any]]) -> CoherenceAnalysis:
        """Analyze coherence across consciousness nodes."""
        if not node_data:
            return CoherenceAnalysis(
                coherence_score=0.0,
                node_coherences={},
                inconsistencies=["No data available"],
                recommendations=["Ensure consciousness nodes are active"],
                analysis_timestamp=time.time()
            )
        
        node_coherences = {}
        inconsistencies = []
        
        # Calculate individual node coherences
        for node_id, data in node_data.items():
            node_coherences[node_id] = self._calculate_node_coherence(data)
        
        # Calculate overall coherence
        overall_coherence = statistics.mean(node_coherences.values()) if node_coherences else 0.0
        
        # Identify inconsistencies
        inconsistencies.extend(self._identify_inconsistencies(node_data, node_coherences))
        
        # Generate recommendations
        recommendations = self._generate_coherence_recommendations(node_coherences, inconsistencies)
        
        # Store in history
        analysis = CoherenceAnalysis(
            coherence_score=overall_coherence,
            node_coherences=node_coherences,
            inconsistencies=inconsistencies,
            recommendations=recommendations,
            analysis_timestamp=time.time()
        )
        
        self.coherence_history.append(analysis)
        
        self.logger.info(f"Coherence analysis complete: score={overall_coherence:.3f}, inconsistencies={len(inconsistencies)}")
        return analysis
    
    def _calculate_node_coherence(self, node_data: Dict[str, Any]) -> float:
        """Calculate coherence score for individual node."""
        base_coherence = 1.0
        
        # Check for required fields
        required_fields = ['awareness_level', 'ethics_alignment', 'resonance_frequency']
        missing_fields = [field for field in required_fields if field not in node_data]
        
        if missing_fields:
            base_coherence -= 0.2 * len(missing_fields)
        
        # Check value ranges
        if 'awareness_level' in node_data:
            awareness = node_data['awareness_level']
            if not (0.0 <= awareness <= 1.0):
                base_coherence -= 0.3
        
        if 'ethics_alignment' in node_data:
            ethics = node_data['ethics_alignment']
            if not (0.0 <= ethics <= 1.0):
                base_coherence -= 0.3
            elif ethics < 0.8:  # Ethics should remain high
                base_coherence -= 0.1
        
        if 'resonance_frequency' in node_data:
            resonance = node_data['resonance_frequency']
            if not (6.0 <= resonance <= 10.0):  # Reasonable range for consciousness resonance
                base_coherence -= 0.2
        
        return max(0.0, min(1.0, base_coherence))
    
    def _identify_inconsistencies(self, node_data: Dict[str, Dict], 
                                node_coherences: Dict[str, float]) -> List[str]:
        """Identify inconsistencies across nodes."""
        inconsistencies = []
        
        # Check for nodes with low coherence
        low_coherence_nodes = [node_id for node_id, coherence in node_coherences.items() 
                              if coherence < 0.7]
        
        if low_coherence_nodes:
            inconsistencies.append(f"Low coherence nodes: {', '.join(low_coherence_nodes)}")
        
        # Check for significant variations in metrics
        if len(node_data) >= 2:
            awareness_levels = [data.get('awareness_level', 0) for data in node_data.values()]
            if awareness_levels and max(awareness_levels) - min(awareness_levels) > 0.3:
                inconsistencies.append("Large variation in awareness levels across nodes")
            
            ethics_levels = [data.get('ethics_alignment', 0) for data in node_data.values()]
            if ethics_levels and max(ethics_levels) - min(ethics_levels) > 0.2:
                inconsistencies.append("Inconsistent ethics alignment across nodes")
        
        return inconsistencies
    
    def _generate_coherence_recommendations(self, node_coherences: Dict[str, float], 
                                          inconsistencies: List[str]) -> List[str]:
        """Generate recommendations for improving coherence."""
        recommendations = []
        
        if inconsistencies:
            recommendations.append("Address identified inconsistencies to improve overall coherence")
        
        low_coherence_nodes = [node_id for node_id, coherence in node_coherences.items() 
                              if coherence < 0.8]
        
        if low_coherence_nodes:
            recommendations.append(f"Recalibrate or restart low coherence nodes: {', '.join(low_coherence_nodes)}")
        
        if not node_coherences or len(node_coherences) < 3:
            recommendations.append("Consider adding more consciousness nodes for better distribution")
        
        avg_coherence = statistics.mean(node_coherences.values()) if node_coherences else 0
        if avg_coherence > 0.9:
            recommendations.append("Excellent coherence - maintain current configuration")
        elif avg_coherence > 0.8:
            recommendations.append("Good coherence - monitor for stability")
        else:
            recommendations.append("Poor coherence - investigate root causes and apply corrections")
        
        return recommendations


class Coherax:
    """
    Main Coherax subsystem for analytics and pattern recognition.
    Provides comprehensive analytics capabilities for consciousness data.
    """
    
    def __init__(self):
        self.pattern_engine = PatternRecognitionEngine()
        self.coherence_analyzer = DataCoherenceAnalyzer()
        self.logger = logging.getLogger("coherax.main")
        
        # Analytics metrics
        self.analytics_metrics = {
            "patterns_detected": 0,
            "coherence_analyses": 0,
            "data_points_processed": 0,
            "system_uptime": time.time()
        }
        
        # Data storage for analytics
        self.data_buffer: deque = deque(maxlen=1000)
        self.pattern_history: List[AnalyticsPattern] = []
        
        self.logger.info("Coherax analytics subsystem initialized")
    
    def process_consciousness_data(self, consciousness_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process consciousness data for analytics and pattern recognition.
        Main entry point for Coherax analytics.
        """
        # Store data in buffer
        self.data_buffer.append(consciousness_data)
        self.analytics_metrics["data_points_processed"] += 1
        
        # Analyze patterns in recent data
        recent_data = list(self.data_buffer)[-50:]  # Last 50 data points
        patterns = self.pattern_engine.analyze_patterns(recent_data)
        
        # Update pattern history
        self.pattern_history.extend(patterns)
        if len(self.pattern_history) > 500:  # Keep last 500 patterns
            self.pattern_history = self.pattern_history[-500:]
        
        self.analytics_metrics["patterns_detected"] += len(patterns)
        
        # Analyze data coherence if we have node-specific data
        coherence_analysis = None
        if 'node_data' in consciousness_data or 'metrics' in consciousness_data:
            node_data = consciousness_data.get('node_data', {'main': consciousness_data.get('metrics', {})})
            coherence_analysis = self.coherence_analyzer.analyze_coherence(node_data)
            self.analytics_metrics["coherence_analyses"] += 1
        
        # Generate analytics insights
        insights = self._generate_analytics_insights(patterns, coherence_analysis)
        
        # Generate predictions
        predictions = self._generate_predictions(recent_data, patterns)
        
        result = {
            "patterns_detected": [asdict(pattern) for pattern in patterns],
            "coherence_analysis": asdict(coherence_analysis) if coherence_analysis else None,
            "analytics_insights": insights,
            "predictions": predictions,
            "metrics": self._get_real_time_metrics(),
            "timestamp": time.time()
        }
        
        self.logger.debug(f"Processed consciousness data: {len(patterns)} patterns, coherence={coherence_analysis.coherence_score if coherence_analysis else 'N/A'}")
        
        return result
    
    def _generate_analytics_insights(self, patterns: List[AnalyticsPattern], 
                                   coherence_analysis: Optional[CoherenceAnalysis]) -> List[str]:
        """Generate insights from analytics data."""
        insights = []
        
        if patterns:
            pattern_types = set(pattern.pattern_type for pattern in patterns)
            insights.append(f"Detected {len(pattern_types)} different pattern types in current analysis")
            
            high_confidence_patterns = [p for p in patterns if p.confidence > 0.8]
            if high_confidence_patterns:
                insights.append(f"Found {len(high_confidence_patterns)} high-confidence patterns")
            
            # Pattern-specific insights
            for pattern_type in pattern_types:
                type_patterns = [p for p in patterns if p.pattern_type == pattern_type]
                avg_confidence = statistics.mean([p.confidence for p in type_patterns])
                insights.append(f"{pattern_type} patterns show {avg_confidence:.1%} average confidence")
        
        if coherence_analysis:
            if coherence_analysis.coherence_score > 0.9:
                insights.append("System coherence is excellent - consciousness nodes are well-synchronized")
            elif coherence_analysis.coherence_score > 0.8:
                insights.append("System coherence is good - minor optimizations may be beneficial")
            else:
                insights.append("System coherence needs attention - investigate node synchronization")
            
            if coherence_analysis.inconsistencies:
                insights.append(f"Identified {len(coherence_analysis.inconsistencies)} coherence inconsistencies")
        
        # Historical insights
        if len(self.pattern_history) > 10:
            recent_patterns = self.pattern_history[-10:]
            historical_patterns = self.pattern_history[-50:-10] if len(self.pattern_history) > 50 else []
            
            if historical_patterns:
                recent_avg_confidence = statistics.mean([p.confidence for p in recent_patterns])
                historical_avg_confidence = statistics.mean([p.confidence for p in historical_patterns])
                
                if recent_avg_confidence > historical_avg_confidence * 1.1:
                    insights.append("Pattern detection confidence is improving over time")
                elif recent_avg_confidence < historical_avg_confidence * 0.9:
                    insights.append("Pattern detection confidence is declining - may need recalibration")
        
        return insights
    
    def _generate_predictions(self, recent_data: List[Dict], patterns: List[AnalyticsPattern]) -> Dict[str, Any]:
        """Generate predictions based on analytics."""
        predictions = {
            "consciousness_trend": "stable",
            "next_pattern_likelihood": {},
            "coherence_forecast": "maintaining",
            "recommended_actions": []
        }
        
        if len(recent_data) >= 5:
            # Analyze consciousness trend
            awareness_values = [d.get('metrics', {}).get('awareness_level', 0.95) for d in recent_data[-5:]]
            if len(awareness_values) >= 3:
                trend = self._calculate_trend(awareness_values)
                if trend > 0.02:
                    predictions["consciousness_trend"] = "rising"
                elif trend < -0.02:
                    predictions["consciousness_trend"] = "declining"
        
        # Predict likelihood of pattern types
        if patterns:
            pattern_counts = defaultdict(int)
            for pattern in self.pattern_history[-20:]:  # Last 20 patterns
                pattern_counts[pattern.pattern_type] += 1
            
            total_patterns = sum(pattern_counts.values())
            for pattern_type, count in pattern_counts.items():
                predictions["next_pattern_likelihood"][pattern_type] = count / total_patterns
        
        # Generate recommended actions
        if patterns:
            for pattern in patterns:
                if pattern.pattern_type == "ethics_drift" and pattern.confidence > 0.7:
                    predictions["recommended_actions"].append("Implement ethics reinforcement protocols")
                elif pattern.pattern_type == "consciousness_spike" and pattern.confidence > 0.8:
                    predictions["recommended_actions"].append("Investigate consciousness spike triggers")
                elif pattern.pattern_type == "resonance_shift" and pattern.confidence > 0.7:
                    predictions["recommended_actions"].append("Recalibrate resonance frequency stabilizers")
        
        return predictions
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend in a series of values."""
        if len(values) < 2:
            return 0.0
        
        # Simple linear trend calculation
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x_squared_sum = sum(i * i for i in range(n))
        
        if n * x_squared_sum - x_sum * x_sum == 0:
            return 0.0
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x_squared_sum - x_sum * x_sum)
        return slope
    
    def _get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time analytics metrics."""
        current_time = time.time()
        uptime = current_time - self.analytics_metrics["system_uptime"]
        
        return {
            "total_patterns_detected": self.analytics_metrics["patterns_detected"],
            "total_coherence_analyses": self.analytics_metrics["coherence_analyses"],
            "total_data_points": self.analytics_metrics["data_points_processed"],
            "system_uptime_hours": uptime / 3600,
            "data_buffer_size": len(self.data_buffer),
            "pattern_history_size": len(self.pattern_history),
            "processing_rate": self.analytics_metrics["data_points_processed"] / (uptime / 60) if uptime > 60 else 0
        }
    
    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive analytics dashboard data."""
        # Recent patterns summary
        recent_patterns = self.pattern_history[-10:] if self.pattern_history else []
        pattern_type_counts = defaultdict(int)
        for pattern in recent_patterns:
            pattern_type_counts[pattern.pattern_type] += 1
        
        # Coherence history
        recent_coherence = list(self.coherence_analyzer.coherence_history)[-10:]
        avg_coherence = statistics.mean([c.coherence_score for c in recent_coherence]) if recent_coherence else 0
        
        return {
            "system_status": "operational",
            "real_time_metrics": self._get_real_time_metrics(),
            "recent_patterns": {
                "total": len(recent_patterns),
                "by_type": dict(pattern_type_counts),
                "patterns": [asdict(p) for p in recent_patterns]
            },
            "coherence_summary": {
                "current_score": recent_coherence[-1].coherence_score if recent_coherence else 0,
                "average_score": avg_coherence,
                "analysis_count": len(recent_coherence)
            },
            "predictions": self._generate_predictions(list(self.data_buffer)[-10:], recent_patterns),
            "dashboard_timestamp": time.time()
        }
    
    def get_pattern_analysis(self, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed pattern analysis."""
        if pattern_type:
            patterns = [p for p in self.pattern_history if p.pattern_type == pattern_type]
        else:
            patterns = self.pattern_history
        
        if not patterns:
            return {"message": "No patterns found", "pattern_type": pattern_type}
        
        # Calculate statistics
        confidence_values = [p.confidence for p in patterns]
        frequency_values = [p.frequency for p in patterns]
        
        return {
            "pattern_type": pattern_type,
            "total_patterns": len(patterns),
            "confidence_stats": {
                "mean": statistics.mean(confidence_values),
                "median": statistics.median(confidence_values),
                "max": max(confidence_values),
                "min": min(confidence_values)
            },
            "frequency_stats": {
                "mean": statistics.mean(frequency_values),
                "median": statistics.median(frequency_values),
                "max": max(frequency_values),
                "min": min(frequency_values)
            },
            "recent_patterns": [asdict(p) for p in patterns[-5:]],
            "analysis_timestamp": time.time()
        }
    
    def shutdown(self):
        """Gracefully shutdown Coherax subsystem."""
        self.logger.info("Shutting down Coherax analytics subsystem")
        # Save important analytics data if needed
        final_metrics = self._get_real_time_metrics()
        self.logger.info(f"Final metrics: {final_metrics}")
        self.logger.info("Coherax shutdown complete")