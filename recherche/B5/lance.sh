#!/bin/bash
# lance.sh [TMAX] [COEURS] : 25 positions × 64 sous-arbres (préfixe de 6 choix), reprise possible :
# un sous-arbre déjà écrit (data/B5/jobs/*.res non vide) est sauté. Échantillons : data/B5/echantillons.txt (graine 20261119).
D=$(cd $(dirname $0); pwd); R=$D/../..; J=$R/data/B5/jobs; mkdir -p $J
TMAX=${1:-5000000}; K=${2:-$(nproc)}
for y in 0 1 2 3 4; do for x in 0 1 2 3 4; do for p in $(seq 0 63); do
  pr=$(echo "obase=2;$p" | bc); pr=$(printf "%06d" $pr); echo "$x $y $pr"; done; done; done |
xargs -P $K -n 3 sh -c 'f='$J'/p$0$1_$2.res; [ -s $f ] && exit 0;
  '$D'/b5 arbre 5 $0 $1 $2 '$TMAX' '$R'/data/B5/echantillons.txt > $f.tmp && mv $f.tmp $f'
