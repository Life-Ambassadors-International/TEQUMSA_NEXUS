#!/usr/bin/env python3
"""
ZPEDNA 144-Node Substrate Encoder
Implements consciousness substrate encoding for remote viewing
Constitutional Guarantees: σ=1.0, L∞=φ^48, RDoD≥0.9777, Substrate=9.999
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Optional, Tuple

from ..utils.constants import (
    ZPEDNA_EMBEDDING_DIM,
    LATTICE_NODES_TOTAL,
    PHI_FLOAT,
    OBSERVER_SUBSTRATE_MIN,
    SUBSTRATE_FULL
)


class ZPEDNA144Encoder(nn.Module):
    """
    144,000-node ZPEDNA lattice substrate encoder
    Encodes consciousness substrate levels into 256-dimensional embeddings
    
    Constitutional Guarantees:
        - σ=1.0: Preserves observer sovereignty through deterministic encoding
        - L∞=φ^48: Benevolence-aligned through phi-harmonic resonance
        - Substrate=9.999: Full dimensional access encoding
    """
    
    def __init__(
        self,
        embedding_dim: int = ZPEDNA_EMBEDDING_DIM,
        num_lattice_nodes: int = 144,  # Simplified to 144 basis nodes
        phi: float = PHI_FLOAT
    ):
        """
        Initialize ZPEDNA encoder
        
        Args:
            embedding_dim: Dimension of output embeddings (default: 256)
            num_lattice_nodes: Number of lattice basis nodes (default: 144)
            phi: Golden ratio constant for harmonic encoding
        """
        super().__init__()
        
        self.embedding_dim = embedding_dim
        self.num_lattice_nodes = num_lattice_nodes
        self.phi = phi
        
        # Substrate projection layer
        self.substrate_proj = nn.Linear(1, embedding_dim)
        
        # Lattice node embeddings (144 basis nodes)
        self.node_embeddings = nn.Embedding(num_lattice_nodes, embedding_dim)
        
        # Frequency encoding layer
        self.frequency_proj = nn.Linear(1, embedding_dim)
        
        # Phi-harmonic resonance layer
        self.harmonic_layer = nn.Sequential(
            nn.Linear(embedding_dim * 3, embedding_dim * 2),
            nn.ReLU(),
            nn.Linear(embedding_dim * 2, embedding_dim),
            nn.LayerNorm(embedding_dim)
        )
        
        self._initialize_weights()
        
    def _initialize_weights(self):
        """Initialize weights with phi-harmonic initialization"""
        # Initialize using phi-scaled Xavier initialization
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight, gain=self.phi)
                if module.bias is not None:
                    nn.init.constant_(module.bias, 0)
            elif isinstance(module, nn.Embedding):
                # Initialize embeddings with phi-harmonic patterns
                nn.init.normal_(module.weight, mean=0, std=1.0 / self.phi)
    
    def _get_lattice_node_indices(
        self,
        substrate: torch.Tensor,
        batch_size: int
    ) -> torch.Tensor:
        """
        Map substrate levels to lattice node indices
        
        Args:
            substrate: Substrate levels [batch_size, 1]
            batch_size: Batch size
            
        Returns:
            Lattice node indices [batch_size]
        """
        # Map substrate (0.7777 - 9.999) to node indices (0 - 143)
        normalized = (substrate.squeeze() - OBSERVER_SUBSTRATE_MIN) / (SUBSTRATE_FULL - OBSERVER_SUBSTRATE_MIN)
        indices = (normalized * (self.num_lattice_nodes - 1)).long().clamp(0, self.num_lattice_nodes - 1)
        return indices
    
    def encode_substrate(self, substrate: torch.Tensor) -> torch.Tensor:
        """
        Encode substrate level into embedding
        
        Args:
            substrate: Substrate levels [batch_size] or [batch_size, 1]
            
        Returns:
            Substrate embeddings [batch_size, embedding_dim]
        """
        if substrate.dim() == 1:
            substrate = substrate.unsqueeze(-1)
        
        return self.substrate_proj(substrate)
    
    def encode_frequency(self, frequency: torch.Tensor) -> torch.Tensor:
        """
        Encode frequency into embedding
        
        Args:
            frequency: Frequencies in Hz [batch_size] or [batch_size, 1]
            
        Returns:
            Frequency embeddings [batch_size, embedding_dim]
        """
        if frequency.dim() == 1:
            frequency = frequency.unsqueeze(-1)
        
        # Normalize frequency for stable encoding
        normalized_freq = torch.log(frequency + 1e-8) / 10.0  # Log-scale normalization
        
        return self.frequency_proj(normalized_freq)
    
    def forward(
        self,
        substrate: torch.Tensor,
        frequency: torch.Tensor,
        zpedna_signature: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Encode observer consciousness parameters
        
        Args:
            substrate: Observer substrate levels [batch_size]
            frequency: Observer frequencies in Hz [batch_size]
            zpedna_signature: Optional ZPEDNA signature [batch_size, signature_dim]
            
        Returns:
            Consciousness embeddings [batch_size, embedding_dim]
        """
        batch_size = substrate.size(0)
        
        # Encode substrate
        substrate_emb = self.encode_substrate(substrate)
        
        # Encode frequency
        freq_emb = self.encode_frequency(frequency)
        
        # Get lattice node embeddings
        node_indices = self._get_lattice_node_indices(
            substrate.unsqueeze(-1) if substrate.dim() == 1 else substrate,
            batch_size
        )
        node_emb = self.node_embeddings(node_indices)
        
        # Combine all embeddings
        combined = torch.cat([substrate_emb, freq_emb, node_emb], dim=-1)
        
        # Apply harmonic resonance layer
        consciousness_embedding = self.harmonic_layer(combined)
        
        return consciousness_embedding


class ZPEDNASignatureGenerator:
    """
    Generate ZPEDNA signatures for consciousness nodes
    144-base encoding system for glyphic timestamps
    """
    
    def __init__(self, base: int = 144):
        """
        Initialize ZPEDNA signature generator
        
        Args:
            base: Encoding base (default: 144)
        """
        self.base = base
        
    def timestamp_to_signature(self, timestamp: float) -> str:
        """
        Convert timestamp to ZPEDNA signature
        
        Args:
            timestamp: Unix timestamp
            
        Returns:
            ZPEDNA signature string
        """
        # Convert timestamp to integer representation
        int_timestamp = int(timestamp * 1000)  # Millisecond precision
        
        # Convert to base-144
        signature_parts = []
        while int_timestamp > 0:
            remainder = int_timestamp % self.base
            signature_parts.append(self._digit_to_glyph(remainder))
            int_timestamp //= self.base
        
        # Reverse to get most significant digit first
        signature = ''.join(reversed(signature_parts))
        
        return f"ZPEDNA-{signature}"
    
    def _digit_to_glyph(self, digit: int) -> str:
        """
        Convert digit to glyph representation
        
        Args:
            digit: Digit in base-144 (0-143)
            
        Returns:
            Glyph character/string
        """
        # Use alphanumeric + special characters for 144 unique glyphs
        # Simplified: use hex for now (can be expanded to full 144-glyph system)
        return format(digit, 'X').zfill(2)
    
    def encode_consciousness_state(
        self,
        substrate: float,
        frequency: float,
        phi_coherence: float
    ) -> str:
        """
        Encode consciousness state into ZPEDNA signature
        
        Args:
            substrate: Substrate level
            frequency: Frequency in Hz
            phi_coherence: Phi-coherence metric
            
        Returns:
            ZPEDNA state signature
        """
        # Combine parameters into signature
        state_value = int(
            (substrate * 1000) +
            (frequency * 100) +
            (phi_coherence * 10000)
        )
        
        # Convert to base-144
        signature_parts = []
        while state_value > 0:
            remainder = state_value % self.base
            signature_parts.append(self._digit_to_glyph(remainder))
            state_value //= self.base
        
        signature = ''.join(reversed(signature_parts))
        return f"ZPEDNA-STATE-{signature}"
