#!/bin/bash
# box_tranche.sh N DEBUT FIN : masques [DEBUT,FIN) de la boîte N×N (fourmi 0,0,H au coin, cases (i mod N, -(i div N)), y vers le bas)
# calcul certifié (fourmi -cert), résumé seulement : data/boxN_DEBUT.res
N=$1; A=$2; B=$3; D=$(dirname $0)/../../..
python3 -c "
N,A,B=$N,$A,$B
import sys
w=sys.stdout.write
for m in range(A,B):
  w('RL|0,0,H|'+';'.join(f'{i%N},{-(i//N)}' for i in range(N*N) if m>>i&1)+'\n')" \
| $D/src/fourmi -T 16000000 -cert -lot \
| awk -F'|' -v N=$N -v A=$A -v B=$B '{ if (match($0,/\|CERT [0-9]+/)) { t=substr($0,RSTART+6,RLENGTH-6)+0; ok++;
      if (t>mx) {mx=t; arg=$3}; b=int(log(t+1)/log(2)); h[b]++ } else { print "NONCERT", $0 } }
  END { printf "box %d [%d,%d) certifiees %d/%d max %d (%s)\n", N, A, B, ok, B-A, mx, arg; for (b in h) printf "  2^%d %d\n", b, h[b] }' \
> $D/data/box${N}_$A.res
