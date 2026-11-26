#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Ask Your KPIs — one command to run everything.
#
#    ./run.sh            → set up (first time only) and open the app
#    ./run.sh --rebuild  → also regenerate the data from scratch (needs Java 17+)
# ─────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

# 1. Pick Python (3.12 recommended)
if command -v python3.12 >/dev/null 2>&1; then PY=python3.12; else PY=python3; fi
echo "🐍 Using $($PY --version)"

# 2. Private environment + packages (first run only)
if [ ! -d .venv ]; then
  echo "📦 First run: creating environment and installing packages (1–3 minutes)..."
  $PY -m venv .venv
  .venv/bin/pip install --quiet --upgrade pip
  .venv/bin/pip install --quiet -r requirements.txt
fi

# 3. Optional: rebuild data from scratch
if [ "${1:-}" = "--rebuild" ]; then
  ./scripts/generate_data.sh
  .venv/bin/python scripts/load_raw.py
  .venv/bin/python scripts/explore.py > docs/data_profile.txt
  .venv/bin/python scripts/export_app_data.py
fi

# 4. Launch
echo "🚀 Opening the app at http://localhost:8501  (press Ctrl+C here to stop)"
.venv/bin/streamlit run app/Home.py
