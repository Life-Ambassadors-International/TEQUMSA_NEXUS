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
if ! grep -E "RDoD trajectory:|Combined Merkle root:" "$OUTPUT_FILE"; then
  echo "Summary extraction warning (non-fatal): script completed, but trajectory/root lines were not found."
  echo "Please verify results in ~/.tequmsa/lattice.db and full command output above."
fi
rm -f "$OUTPUT_FILE"
