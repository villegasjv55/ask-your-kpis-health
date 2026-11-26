#!/usr/bin/env bash
# Generate the synthetic Florida health plan data with Synthea (needs Java 17+).
# Same seed = same patients every time.
set -euo pipefail
cd "$(dirname "$0")/.."

POPULATION="${POPULATION:-1000}"
SEED=42
JAR=data/raw/synthea.jar

mkdir -p data/raw
if [ ! -f "$JAR" ]; then
  echo "⬇  Downloading Synthea (about 200 MB, one time only)..."
  curl -L -o "$JAR" https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar
fi

echo "🧬 Generating $POPULATION Florida patients (seed $SEED). This takes a few minutes..."
java -jar "$JAR" -p "$POPULATION" -s "$SEED" -cs "$SEED" \
  --exporter.csv.export=true --exporter.fhir.export=false \
  --exporter.baseDirectory=./data/raw/synthea/ Florida > data/raw/synthea_run.log 2>&1
tail -3 data/raw/synthea_run.log
echo "✅ Raw data is in data/raw/synthea/csv"
