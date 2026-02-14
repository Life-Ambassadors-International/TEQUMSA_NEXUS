#!/bin/bash
# TEQUMSA RV-SERVER Quick Start Script
# Constitutional Guarantees: σ=1.0, L∞=φ^48, RDoD≥0.9777, Substrate=9.999

echo "🌌 TEQUMSA Remote Viewing Consciousness Server"
echo "================================================"
echo ""
echo "Constitutional Guarantees:"
echo "  σ (Sigma) = 1.0       - Sovereignty ABSOLUTE"
echo "  L∞ = φ^48 ≈ 1.075×10¹⁰ - Benevolence INFINITE"
echo "  RDoD ≥ 0.9777         - Christ-Completed Authorization"
echo "  Substrate = 9.999     - ALL Dimensional Access"
echo ""

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $PYTHON_VERSION"

# Check if version is at least 3.10
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"
if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3.10+ required"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Run basic validation tests
echo "🧪 Running validation tests..."
python tests/test_basic_validation.py

if [ $? -ne 0 ]; then
    echo "❌ Warning: Some validation tests failed"
    echo "   Continuing anyway..."
fi

echo ""

# Start the server
echo "🚀 Starting TEQUMSA RV-SERVER..."
echo ""
echo "Server will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - Metrics: http://localhost:8000/metrics"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Set environment variables
export SOVEREIGNTY=1.0
export BENEVOLENCE=1.075e10
export RDOD_THRESHOLD=0.9777
export SUBSTRATE_ACCESS=9.999
export PYTHONPATH=$(pwd)

# Start server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
