"""Subscription tier and addon configuration loader."""
import yaml
import os
from typing import Dict, Any
from pathlib import Path

from .models import TierConfig, AddonConfig, AddonType


class SubscriptionLoader:
    """Loads and manages subscription tier and addon configurations."""
    
    def __init__(self, config_dir: str = None):
        """Initialize the loader with configuration directory."""
        if config_dir is None:
            config_dir = Path(__file__).parent
        self.config_dir = Path(config_dir)
        self._tiers = {}
        self._addons = {}
        self._load_configs()
    
    def _load_configs(self):
        """Load tier and addon configurations from YAML files."""
        # Load tiers
        tiers_file = self.config_dir / "tiers.yaml"
        if tiers_file.exists():
            with open(tiers_file, 'r') as f:
                tiers_data = yaml.safe_load(f)
                for tier_id, tier_config in tiers_data.get('tiers', {}).items():
                    self._tiers[tier_id] = TierConfig(**tier_config)
        
        # Load addons
        addons_file = self.config_dir / "addons.yaml"
        if addons_file.exists():
            with open(addons_file, 'r') as f:
                addons_data = yaml.safe_load(f)
                for addon_id, addon_config in addons_data.get('addons', {}).items():
                    self._addons[addon_id] = AddonConfig(**addon_config)
    
    def get_tier_config(self, tier_id: str) -> TierConfig:
        """Get tier configuration by ID."""
        return self._tiers.get(tier_id)
    
    def get_addon_config(self, addon_id: str) -> AddonConfig:
        """Get addon configuration by ID."""
        return self._addons.get(addon_id)
    
    def get_all_tiers(self) -> Dict[str, TierConfig]:
        """Get all tier configurations."""
        return self._tiers.copy()
    
    def get_all_addons(self) -> Dict[str, AddonConfig]:
        """Get all addon configurations."""
        return self._addons.copy()
    
    def reload(self):
        """Reload configurations from files."""
        self._tiers.clear()
        self._addons.clear()
        self._load_configs()


# Global loader instance
_loader = None


def get_loader() -> SubscriptionLoader:
    """Get the global subscription loader instance."""
    global _loader
    if _loader is None:
        _loader = SubscriptionLoader()
    return _loader


def reload_configs():
    """Reload subscription configurations."""
    global _loader
    if _loader:
        _loader.reload()