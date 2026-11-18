#!/bin/bash
# cherche_triple.sh LISTE : lignes "pente J K CE offsets..." ; essaie (P1,P2) ; garde le premier tout-OK
D=$(dirname $0)
while read sl J K CE rest; do ok=0
  for P1 in 100 120 80 140; do for P2 in 40 70 100; do
    r=$($D/../ant triple2 $J $K $CE $P1 0 $P2 0 $P1 $rest)
    if echo "$r" | grep -q "C1 OK C2 OK C3 OK C4 OK(-1) C5 OK C7 OK(-1) Z OK"; then echo "OK pente=$sl triple2 $J $K $CE $P1 0 $P2 0 $P1 $rest"; ok=1; break 2; fi
  done; done; [ $ok = 0 ] && echo "ECHEC pente=$sl $J $K $CE $rest :: $r"
done < $1
