#!/bin/bash
# deux_mondes.sh : lit des lignes "multi J K CE NS P1..PNS offsets", récupère s1..sNS par `ant multi`,
# puis contrôle directement le couplage X_k / X_{k+2} avec `ant deux`.
A=$(dirname $0)/../ant
while read m J K CE NS rest; do set -- $rest; P=""; for ((i=0;i<NS;i++)); do P="$P $1"; shift; done; off="$*"
  out=$($A multi $J $K $CE $NS $P $off); S=$(echo "$out" | grep -o "s[0-9]=[0-9-]*" | cut -d= -f2 | tr '\n' ' ')
  v=$(echo "$out" | grep -o "TOUT OK\|=> ECHEC"); echo "$J $K NS=$NS multi:$v :: $($A deux $J $K $CE $NS $S $off)"
done
