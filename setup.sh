#!/usr/bin/env bash
# ============================================================
# SCROLLS RAG Baseline — Environment Setup
# ============================================================
# Run once after cloning / first SSH into the server.
#
#   bash setup.sh
#
# Then activate the env before any run:
#
#   source venv/bin/activate
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  SCROLLS RAG Baseline — Setup"
echo "========================================"

# 1. Create virtual environment (if not present)
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment …"
    python3 -m venv venv
else
    echo "[1/4] Virtual environment already exists."
fi

# 2. Activate
source venv/bin/activate

# 3. Install dependencies
echo "[2/4] Upgrading pip …"
pip install --upgrade pip --quiet

echo "[3/4] Installing Python dependencies …"
pip install -r requirements.txt --quiet

# 4. NLTK data (needed by rouge-score)
echo "[4/4] Downloading NLTK tokeniser data …"
python3 -c "
import nltk, os
nltk.download('punkt',     quiet=True, download_dir=os.path.join(os.getcwd(), 'nltk_data'))
nltk.download('punkt_tab', quiet=True, download_dir=os.path.join(os.getcwd(), 'nltk_data'))
os.environ['NLTK_DATA'] = os.path.join(os.getcwd(), 'nltk_data')
"

# 5. Output dirs
mkdir -p outputs

echo ""
echo "========================================"
echo "  Setup complete!"
echo ""
echo "  Activate:   source venv/bin/activate"
echo "  Smoke test: python smoke_test.py --llm-model <model>"
echo "  Full run:   python run_benchmark.py --llm-model <model>"
echo "========================================"
