#!/usr/bin/env bash
# Download the Humdrum **kern encodings this project builds from.
# They are not committed here; see README for provenance and credits.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p kern-open
WTC=https://raw.githubusercontent.com/humdrum-tools/bach-wtc-fugues/master/kern
AOF=https://raw.githubusercontent.com/craigsapp/art-of-the-fugue/master/kern

# both books of the Well-Tempered Clavier, all 48 fugues
for book in 1 2; do
  for n in $(seq -w 1 24); do
    f="wtc${book}f${n}"
    echo "  $f"; curl -fsSL -o "kern-open/$f.krn" "$WTC/$f.krn"
  done
done
# the fugues of The Art of Fugue (the canons are not fugues and are not shipped)
for n in 001 002 003 004 005 008 009 010 011 019; do
  echo "  artfugue-$n"; curl -fsSL -o "kern-open/artfugue-$n.krn" "$AOF/artfugue-$n.krn"
done
echo "done -> build/kern-open/"
