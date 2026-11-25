#!/bin/bash
# lance.sh FICHIER T [BOITE] : src/fourmi -retour sur 4 cœurs → FICHIER.out (ordre conservé)
F=$1; T=$2; B=${3:--8,-8,14,14}; E=$(dirname $0)/../../src/fourmi
split -n l/4 -d $F $F.part
for p in $F.part0?; do $E -T $T -retour -boite $B -lot < $p > $p.out & done; wait
cat $F.part0?.out > $F.out; rm $F.part0?*
