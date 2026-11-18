#!/bin/bash
# box5_fond.sh COEUR DEBUT PAS NB : NB tranches de PAS masques, à partir de DEBUT, pour un cœur (reprise : saute les .res existants)
D=$(dirname $0); C=$1; A=$2; S=$3; K=$4
for ((i=0;i<K;i++)); do a=$((A+i*S)); b=$((a+S)); [ -s $D/../../../data/box5_$a.res ] && continue; $D/box_tranche.sh 5 $a $b; done
