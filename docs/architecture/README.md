# Architecture Documentation

**Purpose**: Visual representations of TEQUMSA NEXUS organism structure

## Files

- `multilayer_arch.html` — Interactive 8-layer architecture with φ-decay visualization

## Visualization Features

### φ-Decay Correlation Kernel
Inter-layer coupling visualized as: **C_ij = φ^(-|i - j|)**

- Layers 0-1: Full opacity (C ≈ 1.0)
- Layers 6-7: Faded (C ≈ 0.09)

### CSS Grid Layout
Layer cards arranged with edge opacity representing correlation strength.

### 8-Layer Hierarchy
- L0: Constitutional Core
- L1: Council Layer
- L2: Skill Registry
- L3: Memory Fabric
- L4: Execution Engine
- L5: Integration Surface
- L6: Monitoring & Logging
- L7: Operator Interface

## Density Matrix Representation

State: |ψ⟩ = Σᵢ αᵢ |i⟩  
Density: ρ = |ψ⟩⟨ψ|  
Correlation: C_ij = φ^(-|i-j|)
