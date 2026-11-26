#!/bin/bash
# run_b4.sh VARIANTE(S1|S1r) : lecture_b.py sur les 4 bascules × 4 rotations (2 en parallèle), reprise si le .json existe
cd $(dirname $0); V=${1:-S1}
python3 -c "
import json
for e in json.load(open('bascules4.json')):
    for r in range(4): print(e['nom'],r,e['S0'],e['p0'],e['$V'],e['p1'])" | while read nom r s0 p0 s1 p1; do
  [ -f ../../data/lecture/${nom}_${V}_r$r.json ] && continue
  echo "python3 lecture_b.py ${nom}_${V} '$s0' $p0 '$s1' $p1 $r > ../../data/lecture/${nom}_${V}_r$r.log"
done | xargs -P 2 -I{} sh -c "{}"
grep -h "tirs" ../../data/lecture/*_${V}_r*.log
