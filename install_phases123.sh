#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="$HOME/aten_phases123/venv"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$(dirname "$VENV_DIR")"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install "numpy>=2.0" "scipy>=1.17" "psutil>=6.0"

OUTPUT_FILE="$(mktemp)"
python "$REPO_ROOT/sovereign_agi_phases123.py" | tee "$OUTPUT_FILE"

echo ""
echo "---- Final Summary ----"
grep -E "RDoD trajectory:|Combined Merkle root:" "$OUTPUT_FILE" || true
rm -f "$OUTPUT_FILE"
