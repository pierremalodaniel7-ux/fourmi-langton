#!/bin/bash
# t6_refait.sh : refait depuis zéro les étapes R-94 (récurrence en k1) et R-95 (transport) de T6 et compare aux résultats gardés.
# Entrées gardées : resultats/relatif/{bases9,bases13,rel_*,rel13_*,recurrence_k1}.txt. Sortie : data/t6refait/. (S9, 19-11)
set -e; R=$(cd $(dirname $0)/../../.. && pwd); W=$R/data/t6refait; mkdir -p $W; cd $W; cp $R/resultats/relatif/*.txt .
# 1) gap.cert : les 22 classes de c1 (k = 100/101), certifiées
python3 -c "
c=[l.split()[0] for l in open('bases9.txt')]+[l.split()[3] for l in open('bases13.txt')]
open('gap.in','w').write(''.join(f'RL|0,0,H|{x}\n' for x in c))"
$R/src/fourmi -T 8000000 -cert -lot < gap.in > gap.cert
# 2) les 968 configurations {c1 ; c2} (22 × 22 × 2 écarts), lues dans recurrence_k1.txt (J K CE ex ey), recalculées
awk '{x1=$1-$2; y1=$2; printf "RL|0,0,H|%d,%d;%d,%d\n", x1, y1, x1+$4, y1+$5}' recurrence_k1.txt > dbl.in
$R/src/fourmi -T 30000000 -cert -lot < dbl.in > dbl.cert
# 3) récurrence en k1 (R-94) refaite avec ant multi
$R/recherche/autoroute/outils/essai_k1.sh dbl.cert > dbl22.res 2>/dev/null
echo "R-94 : $(diff dbl22.res recurrence_k1.txt | grep -c '^[<>]') ligne(s) différente(s) (attendu 0)"
# 4) transport (R-95)
python3 $R/recherche/autoroute/outils/transport.py > transport.log
echo "R-95 : $(diff transport.res transport.txt | grep -c '^[<>]') ligne(s) différente(s) (attendu 0)"
