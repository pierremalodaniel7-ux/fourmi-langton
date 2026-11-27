#!/bin/bash
# flux.sh NOM I0 I1 T [BOITE] : orbites I0..I1−1 de cycles2.json, 4 flux parallèles gen_cycles → fourmi -retour, sortie compacte
# (ligne : idx orbite,phase,tx,ty | issue | dans/hors | détails fourmi 0) dans data/bascule/NOM.res
N=$1; I0=$2; I1=$3; T=$4; B=${5:--8,-8,14,14}; D=$(cd $(dirname $0); pwd); O=$D/../../data/bascule; E=$D/../../src/fourmi
step=$(( (I1-I0+3)/4 ))
for k in 0 1 2 3; do a=$((I0+k*step)); b=$((a+step)); [ $b -gt $I1 ] && b=$I1
  ( python3 $D/gen_cycles.py 50 $a $b $O/$N.$k.idx ${CY:-cycles2.json} | $E -T $T -retour -boite $B -lot \
    | awk -F'|' '{print $4"|"$5"|"$6"|"$8}' | cut -c1-160 > $O/$N.$k.tmp; paste -d'|' $O/$N.$k.idx $O/$N.$k.tmp > $O/$N.$k.res; rm $O/$N.$k.tmp ) &
done; wait; cat $O/$N.[0-3].res > $O/$N.res; rm $O/$N.[0-3].res $O/$N.[0-3].idx
