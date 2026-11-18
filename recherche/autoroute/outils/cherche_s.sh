#!/bin/bash
# cherche_s.sh FICHIER.cert LISTE_uturn : pour chaque classe, essaie p* = 90 70 50 110 130 150 170 190 210 ; garde le premier OK
D=$(dirname $0); C=$1
while read a J K ps CE rest; do ok=0
  for p in 90 70 50 110 130 150 170 190 210; do l="uturn $J $K $p $CE $rest"
    if echo "$l :: $($D/../ant $l | tr '\n' ' ')" | python3 $D/juge_uturn.py $C | grep -q "^# uturn OK 1 "; then echo "OK $l"; ok=1; break; fi
  done; [ $ok = 0 ] && echo "ECHEC uturn $J $K * $CE $rest"
done < $2
