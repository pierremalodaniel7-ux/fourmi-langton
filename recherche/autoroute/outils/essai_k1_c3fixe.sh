#!/bin/bash
# essai_k1_c3fixe.sh FICHIER : lignes ECHEC de rec_k1 ("n J K CE o2x o2y o3x o3y ECHEC") -> récurrence en k1 avec c3 FIXE en base
# (BASE = c3, T0 = certificat de blanc + c3), îlot {c1, c2} ; multi NS=0/1/2 puis contrôle `ant deux`. (S10, analogue de G1 de T6)
R=$(cd $(dirname $0)/../../.. && pwd); A=$R/recherche/autoroute/ant
grep ECHEC "$1" | while read n J K CE a b c d v; do x3=$((J-K+c)); y3=$((K+d))
  T0=$(echo "RL|0,0,H|$x3,$y3" | $R/src/fourmi -T 400000000 -cert -lot | grep -o "CERT [0-9]*" | cut -d' ' -f2)
  r=ECHEC; for P in "0" "1 90" "1 70" "1 50" "1 110" "1 150" "1 190" "1 300" "1 600" "1 900" "2 100 70" "2 120 70" "2 900 600" "2 1200 900"; do
    o=$(BASE="$x3,$y3" T0=$T0 $A multi $J $K $CE $P $a $b 2>/dev/null | tail -1)
    if echo "$o" | grep -q "TOUT OK"; then S=$(echo "$o" | grep -o "s[0-9]=[0-9-]*" | cut -d= -f2 | tr '\n' ' '); NS=${P%% *}
      dd=$(BASE="$x3,$y3" T0=$T0 $A deux $J $K $CE $NS $S $a $b 2>/dev/null | grep -o "COUPLAGE EXACT\|ECART")
      r="OK[$P] $(echo "$o" | grep -o 'regle=[0-9]*') deux:$dd"; break; fi; done
  echo "$n $J $K $CE $a $b c3=$x3,$y3 T0=$T0 $r"; done
