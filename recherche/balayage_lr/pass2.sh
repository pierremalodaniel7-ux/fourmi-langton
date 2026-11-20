#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f "balaye 2000000" >/dev/null; do sleep 5; done
date > p2_debut.txt
cat part_a?.csv | awk -F, '$3!="V" && $3!="B" && $2<=9 {print $1}' > l2a.txt
cat part_a?.csv | awk -F, '$3!="V" && $3!="B" && $2>=10 && $2<=12 {print $1}' > l2b.txt
# longues d'abord : 1e8 réparties sur 4 cœurs, puis 2e7
split -n r/4 l2a.txt l2a_; split -n r/4 l2b.txt l2b_
for s in aa ab ac ad; do ( ../../src/balaye 100000000 < l2a_$s > p2_a$s.csv; ../../src/balaye 20000000 < l2b_$s > p3_b$s.csv ) & done
wait; date > p2_fin.txt
