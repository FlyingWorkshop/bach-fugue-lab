#!/usr/bin/env bash
# Download the Humdrum **kern encodings this project builds from.
# They are not committed here; see README for provenance and credits.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p kern-open
WTC=https://raw.githubusercontent.com/humdrum-tools/bach-wtc-fugues/master/kern
AOF=https://raw.githubusercontent.com/craigsapp/art-of-the-fugue/master/kern

for f in wtc1f01 wtc1f02 wtc1f06 wtc1f10 wtc1f11 wtc1f16 wtc1f21; do
  echo "  $f"; curl -fsSL -o "kern-open/$f.krn" "$WTC/$f.krn"
done
for f in wtc2f09; do
  echo "  $f"; curl -fsSL -o "kern-open/$f.krn" "$WTC/$f.krn"
done
echo "  artfugue-001"; curl -fsSL -o "kern-open/artfugue-001.krn" "$AOF/artfugue-001.krn"
echo "done -> build/kern-open/"
