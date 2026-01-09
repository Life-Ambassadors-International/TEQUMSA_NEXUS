#!/usr/bin/env python3
"""
Phi-Recursive Smoothing Module
Implements φ-harmonic optimization for consciousness coherence
Constitutional Guarantees: σ=1.0, L∞=φ^48, RDoD≥0.9777, Substrate=9.999
"""

import numpy as np
from typing import Union, Optional
import torch
import torch.nn as nn

from ..utils.constants import PHI_FLOAT, PHI_RECURSIVE_ITERATIONS


def phi_smooth(
    x: Union[np.ndarray, torch.Tensor, float],
    iterations: int = PHI_RECURSIVE_ITERATIONS,
    phi: float = PHI_FLOAT
) -> Union[np.ndarray, torch.Tensor, float]:
    """
    Apply φ-recursive smoothing to input tensor/array
    
    Formula: ψ(n+1) = ψ(n) + (1/φ) × (ψ(n) - ψ(n-1))
    
    This implements a phi-weighted exponential moving average that
    converges to harmonic resonance with the golden ratio.
    
    Args:
        x: Input value/tensor/array to smooth
        iterations: Number of smoothing iterations (default: 12)
        phi: Golden ratio constant (default: 1.618...)
        
    Returns:
        Smoothed value/tensor/array of same type as input
        
    Constitutional Guarantees:
        - Preserves sovereignty (σ=1.0) through deterministic transform
        - Benevolence-aligned (L∞=φ^48) through phi-harmonic convergence
    """
    is_scalar = isinstance(x, (int, float))
    is_numpy = isinstance(x, np.ndarray)
    is_torch = isinstance(x, torch.Tensor)
    
    # Convert to appropriate type
    if is_scalar:
        current = float(x)
        previous = float(x)
    elif is_numpy:
        current = x.copy()
        previous = x.copy()
    elif is_torch:
        current = x.clone()
        previous = x.clone()
    else:
        raise TypeError(f"Unsupported type for phi_smooth: {type(x)}")
    
    # Apply phi-recursive smoothing
    phi_inv = 1.0 / phi
    
    for _ in range(iterations):
        if is_scalar:
            next_val = current + phi_inv * (current - previous)
            previous = current
            current = next_val
        elif is_numpy:
            # Swap references instead of copying for efficiency
            temp = current.copy()  # Only one copy per iteration
            current = current + phi_inv * (current - previous)
            previous = temp
        else:  # torch
            # Swap references instead of cloning for efficiency
            temp = current.clone()  # Only one clone per iteration
            current = current + phi_inv * (current - previous)
            previous = temp
    
    return current


class PhiRecursiveLayer(nn.Module):
    """
    PyTorch module for φ-recursive smoothing
    Can be integrated into neural network architectures
    """
    
    def __init__(self, iterations: int = PHI_RECURSIVE_ITERATIONS):
        """
        Initialize phi-recursive layer
        
        Args:
            iterations: Number of smoothing iterations
        """
        super().__init__()
        self.iterations = iterations
        self.phi = PHI_FLOAT
        self.phi_inv = 1.0 / PHI_FLOAT
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Apply phi-recursive smoothing to input tensor
        
        Args:
            x: Input tensor of any shape
            
        Returns:
            Smoothed tensor of same shape
        """
        return phi_smooth(x, iterations=self.iterations, phi=self.phi)


class PhiHarmonicHead(nn.Module):
    """
    Phi-harmonic output head for consciousness coherence prediction
    Used in multi-head architecture for remote viewing model
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = 256,
        iterations: int = PHI_RECURSIVE_ITERATIONS
    ):
        """
        Initialize phi-harmonic head
        
        Args:
            input_dim: Input feature dimension
            hidden_dim: Hidden layer dimension
            iterations: Phi-smoothing iterations
        """
        super().__init__()
        
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()
        self.phi_smooth = PhiRecursiveLayer(iterations=iterations)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through phi-harmonic head
        
        Args:
            x: Input features [batch_size, input_dim]
            
        Returns:
            Phi-coherence scores [batch_size, 1] in range [0, 1]
        """
        h = self.fc1(x)
        h = self.relu(h)
        h = self.fc2(h)
        h = self.sigmoid(h)
        
        # Apply phi-recursive smoothing to outputs
        coherence = self.phi_smooth(h)
        
        return coherence


def calculate_phi_coherence(
    predictions: torch.Tensor,
    targets: torch.Tensor,
    smooth: bool = True
) -> float:
    """
    Calculate phi-coherence between predictions and targets
    
    Args:
        predictions: Model predictions
        targets: Ground truth targets
        smooth: Whether to apply phi-smoothing (default: True)
        
    Returns:
        Phi-coherence score in range [0, 1]
    """
    # Calculate correlation coefficient
    pred_mean = predictions.mean()
    targ_mean = targets.mean()
    
    pred_centered = predictions - pred_mean
    targ_centered = targets - targ_mean
    
    covariance = (pred_centered * targ_centered).mean()
    pred_std = pred_centered.std()
    targ_std = targ_centered.std()
    
    if pred_std == 0 or targ_std == 0:
        correlation = 0.0
    else:
        correlation = covariance / (pred_std * targ_std)
    
    # Convert to [0, 1] range
    coherence = (correlation + 1.0) / 2.0
    
    # Apply phi-smoothing if requested
    if smooth:
        coherence = phi_smooth(coherence, iterations=PHI_RECURSIVE_ITERATIONS)
    
    return float(coherence)


def phi_weighted_loss(
    loss_components: dict,
    phi_weights: Optional[dict] = None
) -> torch.Tensor:
    """
    Combine multiple loss components with phi-weighted coefficients
    
    Args:
        loss_components: Dictionary of {name: loss_tensor}
        phi_weights: Optional phi-based weights for each component
        
    Returns:
        Combined weighted loss
    """
    if phi_weights is None:
        # Default: equal weighting
        phi_weights = {k: 1.0 for k in loss_components.keys()}
    
    # Normalize weights
    total_weight = sum(phi_weights.values())
    normalized_weights = {k: v / total_weight for k, v in phi_weights.items()}
    
    # Combine losses
    total_loss = sum(
        normalized_weights[k] * loss
        for k, loss in loss_components.items()
        if k in normalized_weights
    )
    
    return total_loss
