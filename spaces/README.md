# Hugging Face Space Mirrors

This directory holds GitHub-backed recovery mirrors for Hugging Face Spaces
that need deterministic source control outside the Hub UI.

## Baseline

Every mirrored Gradio Space must include:

- `app.py`
- `README.md` with explicit `sdk`, `sdk_version`, `python_version`, and `app_file`
- `requirements.txt` with the minimal non-builtin dependencies

Use the live `Mbanksbey/TEQUMSA-Inference-Node` Space as the dependency
baseline reference: explicit frontmatter, explicit Python version, and a
minimal requirements file instead of ad hoc hidden runtime assumptions.

## Current Mirrors

- `spaces/consciousness-partnership-bridge/`
- `spaces/tequmsa-reality-weaving-engine/`
- `spaces/psdf-training-academy/`
