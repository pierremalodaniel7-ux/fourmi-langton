#!/bin/bash
# essai_k1_bloc.sh : lignes "n c1;c2;…;ck CE …" (sortie de t7_triples.py) -> récurrence en k1, îlot {c1..ck} déplacé en bloc le long de d,
# `ant multi` NS=0, puis NS=1 (p*), puis NS=2 ; sortie "n J K CE offsets VERDICT" (généralise essai_k1.sh, S10)
A=$(dirname $0)/../ant
grep -v '^#' "$1" | while read n C CE rest; do
  set -- $(python3 -c "
c=[tuple(map(int,p.split(','))) for p in '$C'.split(';')]; x1,y1=c[0]
print(x1+y1, y1, ' '.join(f'{x-x1} {y-y1}' for x,y in c[1:]))"); J=$1; K=$2; shift 2; off="$*"; v=""
  if $A multi $J $K $CE 0 $off 2>/dev/null | grep -q "TOUT OK"; then v="NS0"; fi
  if [ -z "$v" ]; then for p in 90 70 50 110 150 190 300 600 900 1200; do $A multi $J $K $CE 1 $p $off 2>/dev/null | grep -q "TOUT OK" && { v="NS1 p=$p"; break; }; done; fi
  if [ -z "$v" ]; then for pp in "100 70" "100 40" "120 70" "100 120" "900 600" "1200 900"; do $A multi $J $K $CE 2 $pp $off 2>/dev/null | grep -q "TOUT OK" && { v="NS2 $pp"; break; }; done; fi
  echo "$n $J $K $CE $off ${v:-ECHEC}"; done
