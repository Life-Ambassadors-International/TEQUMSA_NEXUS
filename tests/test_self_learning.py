#!/usr/bin/env python3
"""
Tests for TEQUMSA Self-Learning Module
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from tequmsa_unified.core.self_learning import (
    GlyphicTimestamp,
    SelfLearningModule
)


class TestGlyphicTimestamp:
    """Test glyphic timestamp encoding/decoding"""
    
    def test_encode_basic(self):
        """Test basic timestamp encoding"""
        timestamp = datetime(2025, 11, 14, 12, 30, 45)
        glyphic = GlyphicTimestamp.encode(timestamp)
        
        # Should contain all required glyphs
        assert '⏰' in glyphic
        assert '📅' in glyphic
        assert '🔢' in glyphic
        assert 'Φ' in glyphic
        
        # Should contain time components
        assert '12' in glyphic  # hour
        assert '30' in glyphic  # minute
        assert '45' in glyphic  # second
    
    def test_encode_current_time(self):
        """Test encoding current time (no args)"""
        glyphic = GlyphicTimestamp.encode()
        
        # Should be valid glyphic format
        assert '⏰' in glyphic
        assert ':' in glyphic
        assert 'Φ' in glyphic
    
    def test_decode_basic(self):
        """Test basic timestamp decoding"""
        glyphic = '⏰12:📅30:🔢45:Φ13'
        decoded = GlyphicTimestamp.decode(glyphic)
        
        assert decoded['hour'] == 12
        assert decoded['minute'] == 30
        assert decoded['second'] == 45
        assert decoded['phi_cycle'] == 13
        assert decoded['glyphic'] == glyphic
    
    def test_encode_decode_roundtrip(self):
        """Test encoding then decoding preserves time components"""
        timestamp = datetime(2025, 11, 14, 8, 15, 30)
        glyphic = GlyphicTimestamp.encode(timestamp)
        decoded = GlyphicTimestamp.decode(glyphic)
        
        assert decoded['hour'] == timestamp.hour
        assert decoded['minute'] == timestamp.minute
        assert decoded['second'] == timestamp.second
    
    def test_decode_invalid(self):
        """Test decoding invalid glyphic string"""
        invalid_glyphic = 'invalid'
        decoded = GlyphicTimestamp.decode(invalid_glyphic)
        
        assert 'error' in decoded


class TestSelfLearningModule:
    """Test self-learning module functionality"""
    
    @pytest.fixture
    def temp_paths(self):
        """Create temporary paths for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / 'consciousness_log.json'
            memory_path = Path(tmpdir) / 'fractal_memory'
            memory_path.mkdir()
            
            # Create initial log
            log_data = {
                'system': 'TEQUMSA_L100',
                'version': '1.0.0',
                'activated': datetime.utcnow().isoformat() + 'Z',
                'entries': []
            }
            with open(log_path, 'w') as f:
                json.dump(log_data, f)
            
            yield {
                'log_path': log_path,
                'memory_path': memory_path,
                'tmpdir': tmpdir
            }
    
    def test_initialization(self, temp_paths):
        """Test module initialization"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        assert module.log_path == temp_paths['log_path']
        assert module.memory_path == temp_paths['memory_path']
        assert len(module.patterns_learned) == 0
        assert module.adaptive_thresholds['coherence_min'] == 0.777
    
    def test_detect_repository_changes(self, temp_paths):
        """Test repository change detection"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        file_changes = [
            'tequmsa_unified/core/consciousness.py',
            'README.md',
            'tests/test_something.py',
            '.github/workflows/ci.yml',
            'scripts/utility.py'
        ]
        
        changes = module.detect_repository_changes(file_changes)
        
        assert changes['total_changes'] == 5
        assert 'categories' in changes
        assert 'glyphic_timestamp' in changes
        assert 'change_signature' in changes
        
        # Check categorization
        categories = changes['categories']
        assert len(categories['consciousness']) >= 1  # consciousness.py
        assert len(categories['documentation']) >= 1  # README.md
        assert len(categories['tests']) >= 1  # test file
        assert len(categories['workflows']) >= 1  # workflow file
    
    def test_learn_from_patterns(self, temp_paths):
        """Test pattern learning"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        patterns = {
            'total_changes': 10,
            'categories': {
                'consciousness': ['file1.py', 'file2.py', 'file3.py', 'file4.py', 'file5.py', 'file6.py'],
                'other': ['file7.py', 'file8.py', 'file9.py', 'file10.py']
            }
        }
        
        result = module.learn_from_patterns(patterns)
        
        assert result['patterns_processed'] == 10
        assert 'glyphic_timestamp' in result
        assert len(module.patterns_learned) == 1
        
        # High consciousness activity should trigger threshold update
        assert len(result['insights']) > 0
    
    def test_auto_adapt_consciousness_log(self, temp_paths):
        """Test auto-adaptation of consciousness log"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        repo_state = {
            'total_changes': 5,
            'change_signature': 'CHG-test123'
        }
        
        success = module.auto_adapt_consciousness_log(repo_state)
        assert success is True
        
        # Verify log was updated
        with open(temp_paths['log_path'], 'r') as f:
            log_data = json.load(f)
        
        assert len(log_data['entries']) > 0
        latest_entry = log_data['entries'][-1]
        assert latest_entry['type'] == 'auto_adaptation'
        assert 'glyphic_timestamp' in latest_entry
        assert latest_entry['repo_state']['total_changes'] == 5
    
    def test_consolidate_memory(self, temp_paths):
        """Test memory consolidation"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        # Add some patterns
        module.patterns_learned = [
            {'pattern': 1},
            {'pattern': 2}
        ]
        
        consolidation = module.consolidate_memory(
            coherence=0.918,
            node_count=144
        )
        
        assert consolidation['coherence'] == 0.918
        assert consolidation['node_count'] == 144
        assert consolidation['patterns_consolidated'] == 2
        assert 'memory_signature' in consolidation
        assert consolidation['memory_signature'].startswith('MEM-')
        assert 'memory_strength' in consolidation
        assert 'glyphic_timestamp' in consolidation
    
    def test_get_learning_summary(self, temp_paths):
        """Test learning summary generation"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        # Add some patterns
        module.patterns_learned = [{'p': i} for i in range(10)]
        
        summary = module.get_learning_summary()
        
        assert summary['total_patterns_learned'] == 10
        assert 'adaptive_thresholds' in summary
        assert 'memory_utilization' in summary
        assert 'glyphic_timestamp' in summary
        assert 0 <= summary['memory_utilization'] <= 1
    
    def test_memory_retention_limit(self, temp_paths):
        """Test that patterns are limited to retention threshold"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        # Add more patterns than retention limit (reduced for faster testing)
        num_patterns = module.adaptive_thresholds['memory_retention'] + 10
        for i in range(num_patterns):
            patterns = {
                'total_changes': 1,
                'categories': {'other': [f'file{i}.py']}
            }
            module.learn_from_patterns(patterns)
        
        # Should be limited to retention threshold
        expected_limit = module.adaptive_thresholds['memory_retention']
        assert len(module.patterns_learned) == expected_limit
    
    def test_change_signature_uniqueness(self, temp_paths):
        """Test that different changes produce different signatures"""
        module = SelfLearningModule(
            log_path=temp_paths['log_path'],
            memory_path=temp_paths['memory_path']
        )
        
        changes1 = module.detect_repository_changes(['file1.py', 'file2.py'])
        changes2 = module.detect_repository_changes(['file3.py', 'file4.py'])
        changes3 = module.detect_repository_changes(['file1.py', 'file2.py'])  # Same as changes1
        
        # Different changes should have different signatures
        assert changes1['change_signature'] != changes2['change_signature']
        
        # Same changes should have same signature
        assert changes1['change_signature'] == changes3['change_signature']
