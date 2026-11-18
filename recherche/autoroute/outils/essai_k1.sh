#!/bin/bash
# essai_k1.sh FICHIER.cert : pour chaque configuration {c1 ; c2}, teste les conditions de la récurrence en k1
# (îlot {c1,c2} déplacé en bloc le long de d) avec `ant multi` : NS=0, puis NS=1 (p*), puis NS=2.
A=$(dirname $0)/../ant
python3 -c "
import re,sys
for l in open('$1'):
    f=l.split('|'); c1,c2=f[2].split(';'); x1,y1=map(int,c1.split(',')); x2,y2=map(int,c2.split(','))
    print(x1+y1, y1, re.search(r'CERT (\d+)',l).group(1), x2-x1, y2-y1)" | while read J K CE ex ey; do v=""
  if $A multi $J $K $CE 0 $ex $ey 2>/dev/null | grep -q "TOUT OK"; then v="NS0"; fi
  if [ -z "$v" ]; then for p in 90 70 50 110 150 190 300; do $A multi $J $K $CE 1 $p $ex $ey 2>/dev/null | grep -q "TOUT OK" && { v="NS1 p=$p"; break; }; done; fi
  if [ -z "$v" ]; then for pp in "100 70" "100 40" "120 70" "100 120"; do $A multi $J $K $CE 2 $pp $ex $ey 2>/dev/null | grep -q "TOUT OK" && { v="NS2 $pp"; break; }; done; fi
  echo "$J $K $CE $ex $ey ${v:-ECHEC}"; done
