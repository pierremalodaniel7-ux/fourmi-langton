#!/bin/bash
# audit_t7c.sh N0 N1 : pour les bases T7 n° N0..N1-1 finies, recoupe chaque preuve `multi` de relatif.py par `ant deux`
# (BASE, T0, H0 de la base) ; sortie : "n J K verdict_deux" (S10)
R=$(cd $(dirname $0)/../../.. && pwd)
sed -n "$(($1+1)),$2p" $R/resultats/relatif/t7_bases.txt | { n=$1; while read B T0 CAP ORIG; do f=$R/data/t7/b_$n.txt
  if [ -s $f ]; then H0=$(expr index HDBG $CAP); H0=$((H0-1))
    grep '^OK' $f | sed 's/^OK/multi/' | BASE="$B" T0=$T0 H0=$H0 $R/recherche/autoroute/outils/deux_mondes.sh 2>/dev/null | sed "s/^/$n /"; fi
  n=$((n+1)); done; }
