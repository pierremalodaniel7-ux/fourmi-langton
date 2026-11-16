#!/bin/bash
# Campagne sur les 2 cœurs : génère les situations, lance ./fourmi en parallèle, trie.
# Usage : outils/campagne.sh NOM PAS [options de gen.py]
#   ex. outils/campagne.sh trois_fourmis 400000 --nb 100000 --fourmis 3 --rayon 6
# Résultats bruts : data/NOM.out (ignoré par git). Résumé : affiché (tri.py).
set -e
cd "$(dirname "$0")/.."
NOM=$1; PAS=$2; shift 2
mkdir -p data; make -s -C src fourmi
NC=$(nproc)
python3 outils/gen.py "$@" > data/$NOM.in
echo "$(wc -l < data/$NOM.in) situations, $NC cœurs, $PAS pas max — début $(date +%H:%M:%S)"
split -n r/$NC -d data/$NOM.in data/$NOM.part.
for f in data/$NOM.part.*; do src/fourmi -T $PAS -lot < $f > $f.out & done; wait
cat data/$NOM.part.*.out > data/$NOM.out; rm -f data/$NOM.part.*
echo "fin $(date +%H:%M:%S)"
python3 outils/tri.py data/$NOM.out
