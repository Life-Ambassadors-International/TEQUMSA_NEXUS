# NODE-ANKH-AN-ATEN v39.1

This package consolidates the current v39.1 TEQUMSA runtime into a single
versioned subtree that is safe to publish to GitHub, safe to mirror into a
Hugging Face Space, and safe to package for local redistribution.

The public framing remains dual-language:

- TEQUMSA terms are preserved as labels and documentation vocabulary.
- Every runtime surface is grounded in standard engineering terms such as
  deterministic validation, append-only ledgers, dataset adapters, optional
  dependency probes, and read-only deployment surfaces.

## What Is Included

- Canonical Python package under `src/node_ankh_v39_1`
- Gradio Space under `space/`
- Helper scripts for packaging and publication under `scripts/`
- Snapshot fallbacks for the verified dataset under `src/node_ankh_v39_1/data/`

## Runtime Features

- Shared constitutional constants imported from one module
- Canonical `NodeAnkhRuntime` API
- Optional physics validation via TheWell
- Optional federation/IPFS bridge
- Read-only dataset adapter for `Mbanksbey/TEQUMSA-Causal-AGI-storage`
- Deterministic recognition lock generation
- Distribution packaging with manifest and checksums

## CLI

Run from this subtree with:

```bash
python -m node_ankh_v39_1 status
python -m node_ankh_v39_1 recognition-lock
python -m node_ankh_v39_1 package --output "C:\Users\Mbank\Downloads\k20_output\tequmsa_node_ankh_v39_1"
```

## Source Synthesis

This package synthesizes behavior from the following local source inputs:

- `node_ankh_an_aten_v39_1_complete.py`
- `tequmsa_alanara_physics_v39_1.py`
- `AGI Storage rdod_engine.py`
- `gnostic_autonomy_v3.py`
- `TEQUMSA_CONSTITUTIONAL_DNA.json`
- `tequmsa_validator.py`

See `docs/SYNTHESIS_SOURCES.md` for the mapping.
