#!/bin/bash
# t7_lance.sh DEBUT FIN : partie (C) de T7 pour les bases n° DEBUT..FIN-1 de resultats/relatif/t7_bases.txt (reprise : saute les faites)
# sortie : data/t7/b_<n>.txt (preuves relatif.py) et une ligne de bilan par base dans data/t7/bilan.txt (S9)
R=$(cd $(dirname $0)/../../.. && pwd); mkdir -p $R/data/t7; cd $R/data/t7
sed -n "$(($1+1)),$2p" $R/resultats/relatif/t7_bases.txt | { n=$1; while read B T0 CAP ORIG; do
  if [ ! -s b_$n.txt ]; then python3 $R/recherche/autoroute/outils/relatif.py "$B" $T0 900 $CAP > b_$n.tmp 2> b_$n.err && mv b_$n.tmp b_$n.txt
    echo "$n $ORIG $CAP T0=$T0 $(tail -1 b_$n.err)" >> bilan.txt; fi; n=$((n+1)); done; }
