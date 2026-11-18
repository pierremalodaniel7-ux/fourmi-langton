#!/bin/bash
# repreuve_ns1.sh : lignes "J K CE offsets" ; essaie p* avec `ant multi NS=1` ; affiche OK/ECHEC
A=$(dirname $0)/../ant
while read J K CE off; do ok=0
  for p in 90 70 50 110 130 150 170 190 210 300 400; do
    if $A multi $J $K $CE 1 $p $off 2>/dev/null | grep -q "TOUT OK"; then echo "OK $J $K $CE 1 $p $off"; ok=1; break; fi
  done; [ $ok = 0 ] && echo "ECHEC $J $K $CE $off"; done
