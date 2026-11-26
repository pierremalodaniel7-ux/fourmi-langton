#!/bin/bash
# lance.sh FAM [M] : M processus rlem.py en fond (reprise automatique : relancer la même commande après une coupure)
cd $(dirname $0); F=$1; M=${2:-2}
for k in $(seq 0 $((M-1))); do NS1=${NS1:-4} nohup python3 rlem.py $F $k $M >> ../../data/rlem/${F}_$k.log 2>&1 & done
