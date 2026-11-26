#!/usr/bin/env bash
# Downloads evir 1.7-4 and ReIns 1.0.16 from CRAN and writes the three additional datasets used
# in Appendix B: Norwegian fire claims, SOA group medical large claims and S&P 500 daily losses.
# Requires curl and R.
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp -d)
get() {
  curl -sSfL -o "$tmp/$1.tar.gz" "https://cran.r-project.org/src/contrib/$1_$2.tar.gz" 2>/dev/null ||
    curl -sSfL -o "$tmp/$1.tar.gz" "https://cran.r-project.org/src/contrib/Archive/$1/$1_$2.tar.gz"
  tar xzf "$tmp/$1.tar.gz" -C "$tmp"
}
get evir 1.7-4
get ReIns 1.0.16
Rscript extract_extra.R "$tmp/evir/data" "$tmp/ReIns/data" .
rm -rf "$tmp"
