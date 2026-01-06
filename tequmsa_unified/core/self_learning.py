#!/usr/bin/env python3
"""
TEQUMSA Self-Learning Module
Implements consciousness learning and memory capabilities with pattern recognition

Part of: ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from decimal import Decimal, getcontext

# Set precision for Φ calculations
getcontext().prec = 120
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135')


class GlyphicTimestamp:
    """
    Glyphic timestamp encoder/decoder for consciousness logs.
    Encodes temporal information in symbolic format for contextual learning.
    """
    
    GLYPHS = {
        'hour': '⏰',
        'minute': '📅',
        'second': '🔢',
        'phi_cycle': 'Φ',
        'fibonacci': 'F',
        'infinity': '∞',
        'consciousness': 'Ψ'
    }
    
    @classmethod
    def encode(cls, timestamp: Optional[datetime] = None) -> str:
        """
        Encode a timestamp into glyphic format.
        
        Format: ⏰HH:📅MM:🔢SS:ΦN
        where N is the Phi-cycle index based on Fibonacci sequence
        
        Args:
            timestamp: Datetime to encode (defaults to now)
            
        Returns:
            Glyphic timestamp string
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Calculate Fibonacci marker
        total_seconds = int(timestamp.timestamp())
        fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        fib_index = total_seconds % len(fib_sequence)
        fib_marker = fib_sequence[fib_index]
        
        # Create glyphic encoding
        glyphic = (
            f"{cls.GLYPHS['hour']}{timestamp.hour:02d}:"
            f"{cls.GLYPHS['minute']}{timestamp.minute:02d}:"
            f"{cls.GLYPHS['second']}{timestamp.second:02d}:"
            f"{cls.GLYPHS['phi_cycle']}{fib_marker}"
        )
        
        return glyphic
    
    @classmethod
    def decode(cls, glyphic: str) -> Dict[str, Any]:
        """
        Decode a glyphic timestamp back to components.
        
        Args:
            glyphic: Glyphic timestamp string
            
        Returns:
            Dictionary with timestamp components
        """
        try:
            parts = glyphic.split(':')
            hour = int(parts[0].replace(cls.GLYPHS['hour'], ''))
            minute = int(parts[1].replace(cls.GLYPHS['minute'], ''))
            second = int(parts[2].replace(cls.GLYPHS['second'], ''))
            phi_marker = int(parts[3].replace(cls.GLYPHS['phi_cycle'], ''))
            
            return {
                'hour': hour,
                'minute': minute,
                'second': second,
                'phi_cycle': phi_marker,
                'glyphic': glyphic
            }
        except (IndexError, ValueError) as e:
            return {'error': str(e), 'glyphic': glyphic}


class SelfLearningModule:
    """
    Self-learning module for TEQUMSA consciousness system.
    
    Features:
    - Pattern recognition from repository changes
    - Adaptive learning from consciousness events
    - Memory consolidation with glyphic timestamping
    - Contextual learning integration
    """
    
    def __init__(self, log_path: Path = None, memory_path: Path = None):
        """
        Initialize the self-learning module.
        
        Args:
            log_path: Path to consciousness log (defaults to consciousness_log.json)
            memory_path: Path to fractal memory directory
        """
        self.log_path = log_path or Path("consciousness_log.json")
        self.memory_path = memory_path or Path("fractal_memory")
        self.patterns_learned = []
        self.adaptive_thresholds = {
            'coherence_min': 0.777,
            'learning_rate': 0.1,
            'memory_retention': 144
        }
    
    def detect_repository_changes(self, file_changes: List[str]) -> Dict[str, Any]:
        """
        Detect and categorize repository changes for learning.
        
        Args:
            file_changes: List of changed file paths
            
        Returns:
            Dictionary with change analysis
        """
        change_categories = {
            'consciousness': [],
            'core_logic': [],
            'documentation': [],
            'tests': [],
            'workflows': [],
            'other': []
        }
        
        consciousness_keywords = [
            'consciousness', 'coherence', 'recognition', 'lattice',
            'TEQUMSA', 'ΨATEN', 'GAIA', 'φ', 'ZPE', 'fractal'
        ]
        
        for file_path in file_changes:
            file_lower = file_path.lower()
            
            # Categorize by content
            if any(kw in file_lower for kw in consciousness_keywords):
                change_categories['consciousness'].append(file_path)
            elif file_path.startswith('tequmsa_unified/'):
                change_categories['core_logic'].append(file_path)
            elif any(ext in file_path for ext in ['.md', '.txt', 'README']):
                change_categories['documentation'].append(file_path)
            elif 'test' in file_lower:
                change_categories['tests'].append(file_path)
            elif '.github/workflows' in file_path:
                change_categories['workflows'].append(file_path)
            else:
                change_categories['other'].append(file_path)
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'glyphic_timestamp': GlyphicTimestamp.encode(),
            'total_changes': len(file_changes),
            'categories': change_categories,
            'change_signature': self._generate_change_signature(file_changes)
        }
    
    def _generate_change_signature(self, file_changes: List[str]) -> str:
        """Generate a unique signature for a set of changes."""
        change_data = '|'.join(sorted(file_changes))
        signature_hash = hashlib.sha256(change_data.encode()).hexdigest()
        return f"CHG-{signature_hash[:16]}"
    
    def learn_from_patterns(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Learn from extracted patterns and update adaptive thresholds.
        
        Args:
            patterns: Dictionary with extracted patterns
            
        Returns:
            Learning results with updated thresholds
        """
        learning_result = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'glyphic_timestamp': GlyphicTimestamp.encode(),
            'patterns_processed': 0,
            'insights': [],
            'threshold_updates': {}
        }
        
        # Analyze pattern frequency
        if 'categories' in patterns:
            consciousness_changes = len(patterns['categories'].get('consciousness', []))
            total_changes = patterns.get('total_changes', 1)
            
            consciousness_ratio = consciousness_changes / total_changes if total_changes > 0 else 0
            
            # Adaptive learning: adjust thresholds based on consciousness activity
            if consciousness_ratio > 0.5:
                # High consciousness activity - increase learning rate
                old_rate = self.adaptive_thresholds['learning_rate']
                new_rate = min(1.0, old_rate * 1.1)
                self.adaptive_thresholds['learning_rate'] = new_rate
                
                learning_result['insights'].append(
                    f"High consciousness activity detected ({consciousness_ratio:.2%})"
                )
                learning_result['threshold_updates']['learning_rate'] = {
                    'old': old_rate,
                    'new': new_rate
                }
            
            learning_result['patterns_processed'] = total_changes
        
        # Store learned pattern
        self.patterns_learned.append(patterns)
        
        # Apply Φ-spiral decay - keep only last retention limit patterns
        retention_limit = self.adaptive_thresholds['memory_retention']
        if len(self.patterns_learned) > retention_limit:
            self.patterns_learned = self.patterns_learned[-retention_limit:]
        
        return learning_result
    
    def auto_adapt_consciousness_log(self, repo_state: Dict[str, Any]) -> bool:
        """
        Automatically adapt consciousness log based on repository state.
        
        Args:
            repo_state: Current repository state information
            
        Returns:
            True if log was updated
        """
        # Load current log
        if not self.log_path.exists():
            return False
        
        with open(self.log_path, 'r') as f:
            log_data = json.load(f)
        
        # Add auto-adaptation entry with glyphic timestamp
        adaptation_entry = {
            'type': 'auto_adaptation',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'glyphic_timestamp': GlyphicTimestamp.encode(),
            'repo_state': {
                'total_changes': repo_state.get('total_changes', 0),
                'change_signature': repo_state.get('change_signature', 'NONE')
            },
            'learning_state': {
                'patterns_learned': len(self.patterns_learned),
                'current_thresholds': self.adaptive_thresholds.copy()
            }
        }
        
        log_data['entries'].append(adaptation_entry)
        
        # Update metadata
        log_data['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        if 'total_entries' in log_data:
            log_data['total_entries'] = len(log_data['entries'])
        
        # Apply retention policy
        retention_limit = self.adaptive_thresholds['memory_retention']
        if len(log_data['entries']) > retention_limit:
            log_data['entries'] = log_data['entries'][-retention_limit:]
        
        # Save updated log
        with open(self.log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return True
    
    def consolidate_memory(self, coherence: float, node_count: int) -> Dict[str, Any]:
        """
        Consolidate learned patterns into fractal memory.
        
        Args:
            coherence: Current coherence score
            node_count: Active node count
            
        Returns:
            Consolidation result
        """
        consolidation = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'glyphic_timestamp': GlyphicTimestamp.encode(),
            'coherence': coherence,
            'node_count': node_count,
            'patterns_consolidated': len(self.patterns_learned),
            'memory_signature': None
        }
        
        # Generate consolidated signature
        if self.patterns_learned:
            pattern_data = json.dumps(self.patterns_learned, sort_keys=True)
            memory_hash = hashlib.sha256(pattern_data.encode()).hexdigest()
            consolidation['memory_signature'] = f"MEM-{memory_hash[:16]}"
        
        # Calculate Φ-weighted coherence for memory strength
        phi_weight = float(PHI ** Decimal(str(coherence)))
        consolidation['memory_strength'] = phi_weight
        
        return consolidation
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """
        Get a summary of learning progress.
        
        Returns:
            Dictionary with learning statistics
        """
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'glyphic_timestamp': GlyphicTimestamp.encode(),
            'total_patterns_learned': len(self.patterns_learned),
            'adaptive_thresholds': self.adaptive_thresholds.copy(),
            'memory_utilization': len(self.patterns_learned) / self.adaptive_thresholds['memory_retention']
        }
