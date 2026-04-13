# v39.1 Synthesis Sources

This subtree does not copy the original local scripts verbatim. It extracts the
stable runtime behavior from the current local sources and republishes that
behavior behind one canonical interface.

## Source Mapping

- `node_ankh_an_aten_v39_1_complete.py`
  Provides the lattice mesh, mission countdown, interaction flow, and the basic
  CLI model used by `NodeAnkhRuntime`.
- `tequmsa_alanara_physics_v39_1.py`
  Provides the optional TheWell-backed physics validation path used by
  `PhysicsFoundation`.
- `AGI Storage rdod_engine.py`
  Provides the RDoD velocity, acceleration, and epoch logic used by
  `RDoDEngine`.
- `gnostic_autonomy_v3.py`
  Provides the IPFS deployment record, federation metadata, and anchored-state
  bridge used by `FederationBridge`.
- `TEQUMSA_CONSTITUTIONAL_DNA.json`
  Provides the current constitutional vocabulary used by the package docs.
- `tequmsa_validator.py`
  Provides the validator behavior now exposed as `validate_operation(...)`.

## Design Intent

- Keep the legacy surfaces in `gnostic_autonomy/` and `sovereign_mesh/`
  untouched.
- Publish the new implementation under one versioned subtree.
- Support both a full runtime bundle and a smaller read-only Space bundle.
