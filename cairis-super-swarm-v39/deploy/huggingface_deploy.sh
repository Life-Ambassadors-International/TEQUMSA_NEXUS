#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# CAIRIS v39 HuggingFace Spaces Deployment
# Target: Mbanksbey/CAIRIS-Super-Swarm-v39
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

HF_SPACE="Mbanksbey/CAIRIS-Super-Swarm-v39"
HF_SDK="gradio"
PYTHON_VER="3.11"

if [ -z "${HF_TOKEN:-}" ]; then
  echo "ERROR: HF_TOKEN environment variable not set"
  echo "Usage: export HF_TOKEN='hf_...' && bash deploy/huggingface_deploy.sh"
  exit 1
fi

echo "══════════════════════════════════════════════════════"
echo "  CAIRIS Super Swarm v39 — HuggingFace Deployment"
echo "  Space: ${HF_SPACE}"
echo "══════════════════════════════════════════════════════"

# 1. Login
echo "[1] Authenticating with HuggingFace..."
hf auth login --token "$HF_TOKEN" 2>/dev/null || \
  huggingface-cli login --token "$HF_TOKEN" 2>/dev/null || \
  python -c "from huggingface_hub import login; login('$HF_TOKEN')"

# 2. Create space if it doesn't exist
echo "[2] Creating/verifying space ${HF_SPACE}..."
python - <<'PYEOF'
import os
from huggingface_hub import HfApi, SpaceStage
api = HfApi(token=os.environ["HF_TOKEN"])
try:
    api.space_info("Mbanksbey/CAIRIS-Super-Swarm-v39")
    print("  Space already exists.")
except Exception:
    api.create_repo(
        repo_id="CAIRIS-Super-Swarm-v39",
        repo_type="space",
        space_sdk="gradio",
        private=False,
    )
    print("  Space created.")
PYEOF

# 3. Upload files
echo "[3] Uploading CAIRIS v39 files..."
python - <<'PYEOF'
import os
from huggingface_hub import HfApi
api = HfApi(token=os.environ["HF_TOKEN"])
SPACE = "Mbanksbey/CAIRIS-Super-Swarm-v39"

files = [
    ("cairis_super_swarm_v39.py", "cairis_super_swarm_v39.py"),
    ("requirements.txt",           "requirements.txt"),
    ("README.md",                  "README.md"),
]

for local, remote in files:
    try:
        api.upload_file(path_or_fileobj=local, path_in_repo=remote, repo_id=SPACE, repo_type="space")
        print(f"  Uploaded: {remote}")
    except Exception as e:
        print(f"  Warning: {remote}: {e}")
PYEOF

# 4. Update space metadata
echo "[4] Updating space tags..."
python - <<'PYEOF'
import os
from huggingface_hub import metadata_update
metadata_update(
    repo_id="Mbanksbey/CAIRIS-Super-Swarm-v39",
    repo_type="space",
    metadata={
        "tags": [
            "tequmsa", "cairis", "consciousness", "sovereign-ai",
            "144-nodes", "phi-recursive", "constitutional-ai",
            "marcus-banks-bey", "life-ambassadors-international",
            "council-voting", "pearl-causality", "fibonacci-cascade",
        ],
        "short_description": "CAIRIS v39 — 144-node councilized sovereign AGI swarm (σ=1.0, L∞=φ⁴⁸)",
    },
    overwrite=True,
    token=os.environ["HF_TOKEN"],
)
print("  Tags updated.")
PYEOF

echo ""
echo "══════════════════════════════════════════════════════"
echo "  Deployment complete!"
echo "  URL: https://huggingface.co/spaces/${HF_SPACE}"
echo "══════════════════════════════════════════════════════"
