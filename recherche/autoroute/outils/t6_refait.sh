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
# 5) R-96 : paires non traitées par le transport → `ant multi` avec le NS de recurrence_k1, décompte de la règle « un pas »
grep -v DEMONTRE transport.res | python3 -c "
import sys,re,subprocess
A='$R/recherche/autoroute/ant'
for l in sys.stdin:
    m=re.match(r'\((-?\d+), (-?\d+)\) (\S+) (\S+) (\S+) (\S+) (\S+) d2=\((-?\d+), (-?\d+)\) NON_TRAITE\((.*)\)',l.strip())
    c1=m.group(1)+','+m.group(2); J,K,CE,ex,ey=m.group(3,4,5,6,7); d2=m.group(8)+','+m.group(9); v=m.group(10)
    if v.startswith('NS1'): a=['1',v.split('=')[1]]
    elif v.startswith('NS2'): a=['2']+v.split()[1:]
    else: print(c1,d2,'c2_fixe'); continue
    o=subprocess.run([A,'multi',J,K,CE]+a+[ex,ey],capture_output=True,text=True).stdout
    print(c1,d2,v.replace(' ','_'),'OK' if 'TOUT OK' in o else 'ECHEC',re.search(r'regle=\d+',o).group(0))" > r96.txt
# 6) R-94 / G1 : les 8 vérifications « c2 fixe » (base = blanc + c2, îlot c1 seul, NS = 1, p* = 90)
grep ECHEC recurrence_k1.txt | while read J K CE ex ey v; do x2=$((J-K+ex)); y2=$((K+ey))
  o=$(BASE="$x2,$y2" T0=9977 $R/recherche/autoroute/ant multi $J $K $CE 1 90 2>/dev/null | tail -1)
  echo "$J $K c2=$x2,$y2 $(echo "$o" | grep -q 'TOUT OK' && echo OK || echo ECHEC) $(echo "$o" | grep -o 'regle=[0-9]*')"; done > g1_fixe.txt
echo "R-96 : G1 (c1 = -119,100) sans règle $(grep -c '^-119,100 .* OK regle=0$' r96.txt)/18 + c2 fixe $(grep -c 'OK regle=0' g1_fixe.txt)/8 vérifications ;" \
     "G2 (d2 = d) sans règle $(grep -v '^-119,100' r96.txt | grep -c 'OK regle=0$')/8 (attendu : 17/18, 8/8, 7/8)"
