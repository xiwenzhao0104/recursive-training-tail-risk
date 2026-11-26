#!/usr/bin/env bash
# Reproduces every figure, table and number in the paper and in Appendix B.
# Usage: bash run_all.sh [number of parallel workers for Appendix B, default 4]
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
WORKERS=${1:-4}

# Data (downloaded from CRAN; not redistributed)
[ -f data/danish.csv ] || bash data/get_danish_data.sh
[ -f data/sp500_losses.csv ] || bash data/get_extra_data.sh

# Sections 3, 4, 6-9 and Appendix A: Figures 2-5, Table 3 and the numbers in the text
$PY code/theory_figures.py
$PY code/theory_results.py > /dev/null
# Table 4 and Appendix B.1-B.7
$PY code/theory_appendix.py > /dev/null

# Section 5: Table 1 and Figure 1
$PY code/empirical/textbook_models.py > /dev/null
$PY code/empirical/sdv_models.py > /dev/null
$PY code/empirical/evidence_figure.py > /dev/null

# Appendix B.8-B.12: 602 training runs, shared among parallel workers
cd code/empirical
for k in $(seq 1 "$WORKERS"); do
  OMP_NUM_THREADS=1 $PY -W ignore appendix_runs.py work 1 > /dev/null 2>&1 &
done
wait
$PY appendix_runs.py list
$PY appendix_tables.py > /dev/null
cd ../..
echo "Done: figures in output/figures, results in output/results"
