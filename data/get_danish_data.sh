#!/usr/bin/env bash
# Downloads evir 1.7-4 from CRAN and writes data/danish.csv. Requires curl and R.
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp -d)
url=https://cran.r-project.org/src/contrib/evir_1.7-4.tar.gz
curl -sSfL -o "$tmp/evir.tar.gz" "$url" 2>/dev/null || curl -sSfL -o "$tmp/evir.tar.gz" "https://cran.r-project.org/src/contrib/Archive/evir/evir_1.7-4.tar.gz"
tar xzf "$tmp/evir.tar.gz" -C "$tmp"
Rscript extract_danish.R "$tmp/evir/data/danish.rda" danish.csv
rm -rf "$tmp"
