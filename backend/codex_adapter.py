"""
Codex Integration Adapter

Pure stdlib implementation for integrating OpenAI Codex functionality 
into the TEQUMSA AGI Interface. This module provides a feature-flagged
interface with ethical safeguards.

Author: TEQUMSA Development Team
License: MIT
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any


class CodexAdapter:
    """
    Adapter for OpenAI Codex integration with TEQUMSA.
    
    Features:
    - Feature flag controlled activation
    - Subtree dependency verification
    - Pure stdlib implementation
    - Ethical safeguards and consent validation
    """
    
    def __init__(self):
        self._enabled = self._check_feature_flag()
        self._subtree_available = self._check_subtree_availability()
        
    def _check_feature_flag(self) -> bool:
        """Check if Codex integration is enabled via environment variable."""
        return os.getenv('TEQUMSA_CODEX_ENABLED', 'false').lower() == 'true'
    
    def _check_subtree_availability(self) -> bool:
        """Check if the external/codex subtree is available."""
        # Get the project root directory
        current_dir = Path(__file__).resolve().parent
        if current_dir.name == 'backend':
            project_root = current_dir.parent
        else:
            project_root = current_dir
            
        codex_path = project_root / 'external' / 'codex'
        return codex_path.exists() and codex_path.is_dir()
    
    def is_available(self) -> bool:
        """
        Check if Codex integration is fully available.
        
        Returns:
            bool: True if both feature flag is enabled and subtree is available
        """
        return self._enabled and self._subtree_available
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of Codex integration.
        
        Returns:
            Dict containing status information
        """
        return {
            'feature_flag_enabled': self._enabled,
            'subtree_available': self._subtree_available,
            'fully_available': self.is_available(),
            'reason': self._get_unavailable_reason()
        }
    
    def _get_unavailable_reason(self) -> Optional[str]:
        """Get reason why Codex integration is not available."""
        if not self._enabled and not self._subtree_available:
            return "Feature flag disabled and subtree not available"
        elif not self._enabled:
            return "Feature flag disabled (set TEQUMSA_CODEX_ENABLED=true to enable)"
        elif not self._subtree_available:
            return "Subtree not available (external/codex directory not found)"
        return None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate code using Codex integration.
        
        Args:
            prompt: The code generation prompt
            **kwargs: Additional parameters for generation
            
        Returns:
            Generated code as string
            
        Raises:
            RuntimeError: If Codex integration is not available
            ValueError: If prompt is invalid
        """
        if not self.is_available():
            reason = self._get_unavailable_reason()
            raise RuntimeError(f"Codex integration not available: {reason}")
        
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")
        
        # TODO: Implement actual Codex API integration when subtree is added
        # For now, return a placeholder response for testing
        return self._placeholder_generate(prompt, **kwargs)
    
    def _placeholder_generate(self, prompt: str, **kwargs) -> str:
        """
        Placeholder generation for testing purposes.
        
        This will be replaced with actual Codex API calls when the
        external/codex subtree is integrated.
        """
        return f"# Generated code for: {prompt}\n# TODO: Implement actual Codex integration"
    
    def validate_consent(self, user_id: Optional[str] = None) -> bool:
        """
        Validate user consent for AI code generation.
        
        Args:
            user_id: Optional user identifier for consent tracking
            
        Returns:
            bool: True if consent is valid
        """
        # TODO: Implement proper consent validation
        # This is a placeholder for ethical safeguards
        return True
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get information about current Codex capabilities.
        
        Returns:
            Dict containing capability information
        """
        if not self.is_available():
            return {
                'available': False,
                'languages': [],
                'max_tokens': 0,
                'features': []
            }
        
        # TODO: Return actual capabilities when integrated
        return {
            'available': True,
            'languages': ['python', 'javascript', 'typescript', 'bash'],
            'max_tokens': 4096,
            'features': ['code_generation', 'code_completion', 'refactoring']
        }


# Singleton instance for easy import
codex_adapter = CodexAdapter()


def is_codex_available() -> bool:
    """Convenience function to check if Codex is available."""
    return codex_adapter.is_available()


def generate_code(prompt: str, **kwargs) -> str:
    """Convenience function for code generation."""
    return codex_adapter.generate(prompt, **kwargs)


def get_codex_status() -> Dict[str, Any]:
    """Convenience function to get Codex status."""
    return codex_adapter.get_status()