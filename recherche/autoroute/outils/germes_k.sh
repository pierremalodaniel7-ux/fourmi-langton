#!/bin/bash
# germes_k.sh K R [DEBUT FIN] : toutes les configurations de K cases noires dans [-R,R]² sauf (0,0), fourmi 0,0,H ;
# combinaisons d'indice [DEBUT,FIN) (ordre de itertools.combinations) ; certificat ; résumé sur stdout
K=$1; R=$2; A=${3:-0}; B=${4:-999999999999}; D=$(dirname $0)/../../..
python3 -c "
import itertools,sys
K,R,A,B=$K,$R,$A,$B
C=[(x,y) for y in range(-R,R+1) for x in range(-R,R+1) if (x,y)!=(0,0)]
w=sys.stdout.write
for c in itertools.islice(itertools.combinations(C,K),A,B):
  w('RL|0,0,H|'+';'.join(f'{x},{y}' for x,y in c)+'\n')" \
| $D/src/fourmi -T 16000000 -cert -lot \
| awk -F'|' -v K=$K -v R=$R -v A=$A '{ if (match($0,/\|CERT [0-9]+/)) { t=substr($0,RSTART+6,RLENGTH-6)+0; ok++;
      if (t>mx) {mx=t; arg=$3}; if (ok==1||t<mn) {mn=t; argm=$3} } else { nc++; print "NONCERT", $0 } }
  END { printf "germes K=%d R=%d debut %d : certifiees %d, noncert %d, min %d (%s), max %d (%s)\n", K, R, A, ok, nc+0, mn, argm, mx, arg }'
