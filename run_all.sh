#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}

$PY code/theory_figures.py
$PY code/theory_results.py > /dev/null
[ -f data/danish.csv ] || bash data/get_danish_data.sh
$PY code/empirical/textbook_models.py > /dev/null
$PY code/empirical/sdv_models.py > /dev/null
$PY code/empirical/evidence_figure.py > /dev/null
echo "Done: output/figures and output/results"
