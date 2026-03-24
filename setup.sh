#!/usr/bin/env bash
# ============================================================
# SCROLLS Vanilla RAG and DOS RAG Benchmark - Environment Setup
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  SCROLLS Vanilla RAG + DOS RAG - Setup"
echo "========================================"
echo "Environment manager: Python venv"
echo "Note: venv isolates packages, but it does not install a new Python version."
echo ""

PYTHON_BIN=""
for candidate in python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PYTHON_BIN="$candidate"
        break
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "No suitable Python interpreter found."
    exit 1
fi

PYTHON_VERSION="$("$PYTHON_BIN" -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
case "$PYTHON_VERSION" in
    3.10|3.11|3.12)
        ;;
    *)
        echo "Selected interpreter: $PYTHON_BIN ($PYTHON_VERSION)"
        echo "This repo uses Python's built-in venv for package isolation."
        echo "A venv inherits the Python version used to create it, so it cannot upgrade Python 3.8 to 3.11."
        echo "vLLM setup is expected to work on Python 3.10-3.12."
        echo "Install python3.12 or python3.11 on the server, or create a conda/micromamba env with one of those versions, then rerun setup.sh."
        exit 1
        ;;
esac

echo "Using Python interpreter: $PYTHON_BIN ($PYTHON_VERSION)"

if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment ..."
    "$PYTHON_BIN" -m venv venv
else
    echo "[1/4] Virtual environment already exists."
fi

source venv/bin/activate

echo "[2/4] Upgrading pip ..."
pip install --upgrade pip --quiet

echo "[3/4] Installing Python dependencies ..."
pip install -r requirements.txt --quiet

echo "[4/4] Finalizing output directories ..."

mkdir -p outputs

echo ""
echo "========================================"
echo "  Setup complete!"
echo ""
echo "  Important:    bash setup.sh runs in a child shell."
echo "                It cannot leave your current shell activated."
echo "                Run the next command in your current shell:"
echo "  Activate:     source venv/bin/activate"
echo "  Smoke tier:   python smoke_test.py"
echo "  Subset tier:  python run_benchmark.py --run-tier subset"
echo "  SCROLLS full: python run_benchmark.py --run-tier scrolls_full"
echo "  Analysis:     python analyze_outputs.py --run-tier subset"
echo "========================================"
