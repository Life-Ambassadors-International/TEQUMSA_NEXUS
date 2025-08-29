"""
Integration tests for Codex Adapter

Comprehensive test suite verifying:
- Capabilities disabled without flag
- generate() raises when disabled  
- Enabling flag but missing subtree still disabled
- Simulated generation works when both flag on and directory external/codex present
- Uses pytest monkeypatch to chdir into tmp_path for subtree simulation

Author: TEQUMSA Development Team
"""

import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add backend directory to path for imports
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

from codex_adapter import CodexAdapter, is_codex_available, generate_code, get_codex_status


class TestCodexAdapterDisabled:
    """Test Codex adapter behavior when disabled (default state)."""
    
    def test_capabilities_disabled_without_flag(self):
        """Test that capabilities are disabled when feature flag is not set."""
        # Ensure environment is clean
        with patch.dict(os.environ, {}, clear=True):
            adapter = CodexAdapter()
            
            assert not adapter.is_available()
            assert not adapter._enabled
            
            status = adapter.get_status()
            assert not status['feature_flag_enabled']
            assert not status['fully_available']
            assert 'Feature flag disabled' in status['reason']
    
    def test_generate_raises_when_disabled(self):
        """Test that generate() raises RuntimeError when disabled."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = CodexAdapter()
            
            with pytest.raises(RuntimeError) as exc_info:
                adapter.generate("print('hello world')")
            
            assert "Codex integration not available" in str(exc_info.value)
            assert "Feature flag disabled" in str(exc_info.value)
    
    def test_get_capabilities_when_disabled(self):
        """Test capabilities response when disabled."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = CodexAdapter()
            
            capabilities = adapter.get_capabilities()
            assert not capabilities['available']
            assert capabilities['languages'] == []
            assert capabilities['max_tokens'] == 0
            assert capabilities['features'] == []
    
    def test_convenience_functions_disabled(self):
        """Test convenience functions when disabled."""
        with patch.dict(os.environ, {}, clear=True):
            # Clear any cached instances
            import importlib
            import backend.codex_adapter as ca_module
            importlib.reload(ca_module)
            
            assert not ca_module.is_codex_available()
            
            with pytest.raises(RuntimeError):
                ca_module.generate_code("test prompt")
            
            status = ca_module.get_codex_status()
            assert not status['fully_available']


class TestCodexAdapterFlagEnabledSubtreeMissing:
    """Test behavior when flag is enabled but subtree is missing."""
    
    def test_enabling_flag_missing_subtree_still_disabled(self):
        """Test that enabling flag without subtree keeps integration disabled."""
        with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': 'true'}):
            adapter = CodexAdapter()
            
            # Should be enabled by flag but disabled due to missing subtree
            assert adapter._enabled
            assert not adapter._subtree_available
            assert not adapter.is_available()
            
            status = adapter.get_status()
            assert status['feature_flag_enabled']
            assert not status['subtree_available']
            assert not status['fully_available']
            assert 'Subtree not available' in status['reason']
    
    def test_generate_fails_with_flag_no_subtree(self):
        """Test that generate() fails even with flag when subtree missing."""
        with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': 'true'}):
            adapter = CodexAdapter()
            
            with pytest.raises(RuntimeError) as exc_info:
                adapter.generate("def hello(): pass")
            
            assert "Codex integration not available" in str(exc_info.value)
            assert "Subtree not available" in str(exc_info.value)


class TestCodexAdapterFullyEnabled:
    """Test behavior when both flag is enabled and subtree is simulated."""
    
    def test_simulated_generation_works_when_enabled(self, tmp_path, monkeypatch):
        """Test that generation works when both flag and subtree are available."""
        # Create simulated external/codex directory structure
        external_dir = tmp_path / 'external'
        codex_dir = external_dir / 'codex'
        codex_dir.mkdir(parents=True)
        
        # Create some placeholder files to make it look like a real subtree
        (codex_dir / 'README.md').write_text("# Codex Integration")
        (codex_dir / '__init__.py').write_text("# Codex module")
        
        # Change to tmp_path directory for subtree simulation
        monkeypatch.chdir(tmp_path)
        
        # Mock the adapter to find the subtree in our tmp location
        with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': 'true'}):
            with patch('pathlib.Path.resolve') as mock_resolve:
                # Make the adapter think it's in the right location
                mock_resolve.return_value = tmp_path / 'backend' / 'codex_adapter.py'
                
                adapter = CodexAdapter()
                
                # Manually set subtree availability for simulation
                adapter._subtree_available = True
                
                assert adapter._enabled
                assert adapter._subtree_available
                assert adapter.is_available()
                
                # Test successful generation
                result = adapter.generate("print('hello world')")
                assert isinstance(result, str)
                assert "Generated code for: print('hello world')" in result
                assert "TODO: Implement actual Codex integration" in result
    
    def test_capabilities_when_fully_enabled(self, tmp_path, monkeypatch):
        """Test capabilities response when fully enabled."""
        # Setup simulated environment
        external_dir = tmp_path / 'external'
        codex_dir = external_dir / 'codex'
        codex_dir.mkdir(parents=True)
        
        monkeypatch.chdir(tmp_path)
        
        with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': 'true'}):
            adapter = CodexAdapter()
            adapter._subtree_available = True  # Simulate subtree presence
            
            capabilities = adapter.get_capabilities()
            assert capabilities['available']
            assert 'python' in capabilities['languages']
            assert 'javascript' in capabilities['languages']
            assert capabilities['max_tokens'] > 0
            assert 'code_generation' in capabilities['features']
    
    def test_status_when_fully_enabled(self, tmp_path, monkeypatch):
        """Test status response when fully enabled."""
        external_dir = tmp_path / 'external'
        codex_dir = external_dir / 'codex'
        codex_dir.mkdir(parents=True)
        
        monkeypatch.chdir(tmp_path)
        
        with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': 'true'}):
            adapter = CodexAdapter()
            adapter._subtree_available = True
            
            status = adapter.get_status()
            assert status['feature_flag_enabled']
            assert status['subtree_available']
            assert status['fully_available']
            assert status['reason'] is None


class TestCodexAdapterInputValidation:
    """Test input validation and error handling."""
    
    def test_generate_invalid_prompt_validation(self, tmp_path, monkeypatch):
        """Test validation of generate() prompt parameter."""
        # Setup enabled environment
        external_dir = tmp_path / 'external'
        codex_dir = external_dir / 'codex'
        codex_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        
        with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': 'true'}):
            adapter = CodexAdapter()
            adapter._subtree_available = True
            
            # Test empty prompt
            with pytest.raises(ValueError) as exc_info:
                adapter.generate("")
            assert "Prompt must be a non-empty string" in str(exc_info.value)
            
            # Test None prompt
            with pytest.raises(ValueError) as exc_info:
                adapter.generate(None)
            assert "Prompt must be a non-empty string" in str(exc_info.value)
            
            # Test non-string prompt
            with pytest.raises(ValueError) as exc_info:
                adapter.generate(123)
            assert "Prompt must be a non-empty string" in str(exc_info.value)
    
    def test_consent_validation(self):
        """Test consent validation functionality."""
        adapter = CodexAdapter()
        
        # Test basic consent validation (placeholder implementation)
        assert adapter.validate_consent() is True
        assert adapter.validate_consent("user123") is True


class TestCodexAdapterIntegrationPatterns:
    """Test integration patterns and edge cases."""
    
    def test_environment_variable_case_sensitivity(self):
        """Test that environment variable is case-insensitive for common values."""
        test_cases = [
            ('true', True),
            ('True', True), 
            ('TRUE', True),
            ('false', False),
            ('False', False),
            ('FALSE', False),
            ('1', False),  # Only 'true' should work
            ('yes', False),
            ('', False),
        ]
        
        for env_value, expected in test_cases:
            with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': env_value}):
                adapter = CodexAdapter()
                assert adapter._enabled == expected
    
    def test_multiple_adapter_instances(self):
        """Test that multiple adapter instances behave consistently."""
        with patch.dict(os.environ, {}, clear=True):
            adapter1 = CodexAdapter()
            adapter2 = CodexAdapter()
            
            assert adapter1.is_available() == adapter2.is_available()
            assert adapter1.get_status() == adapter2.get_status()
    
    def test_subtree_detection_edge_cases(self, tmp_path, monkeypatch):
        """Test edge cases in subtree detection."""
        monkeypatch.chdir(tmp_path)
        
        # Test with external directory but no codex subdirectory
        external_dir = tmp_path / 'external'
        external_dir.mkdir()
        
        adapter = CodexAdapter()
        assert not adapter._subtree_available
        
        # Test with external/codex as file instead of directory
        codex_file = external_dir / 'codex'
        codex_file.write_text("not a directory")
        
        adapter = CodexAdapter()
        assert not adapter._subtree_available
    
    def test_placeholder_generation_format(self, tmp_path, monkeypatch):
        """Test that placeholder generation returns expected format."""
        external_dir = tmp_path / 'external'
        codex_dir = external_dir / 'codex'
        codex_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        
        with patch.dict(os.environ, {'TEQUMSA_CODEX_ENABLED': 'true'}):
            adapter = CodexAdapter()
            adapter._subtree_available = True
            
            test_prompt = "def fibonacci(n):"
            result = adapter.generate(test_prompt)
            
            # Verify placeholder format
            assert result.startswith("# Generated code for:")
            assert test_prompt in result
            assert "TODO: Implement actual Codex integration" in result
            assert isinstance(result, str)
            assert len(result) > 0


if __name__ == '__main__':
    # Run tests when executed directly
    pytest.main([__file__, '-v'])