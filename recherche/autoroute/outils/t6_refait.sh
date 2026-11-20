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
echo "R-94 : $(diff dbl22.res recurrence_k1.txt | grep -c '^[<>]') ligne(s) différente(s) (attendu 0 avant R-122 ; depuis : 72 pour R-94 et 36 pour R-95, tous de c1 = -119,100 « bloc » → ECHEC, traités par l'étape 6)"
# 4) transport (R-95)
python3 $R/recherche/autoroute/outils/transport.py > transport.log
echo "R-95 : $(diff transport.res transport.txt | grep -c '^[<>]') ligne(s) différente(s) (attendu 0 avant R-122 ; depuis : 72 pour R-94 et 36 pour R-95, tous de c1 = -119,100 « bloc » → ECHEC, traités par l'étape 6)"
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
# 6) R-94 / G1 : c1 = classe demi-tour (-119,100) : c2 FIXE en base (base = blanc + c2, îlot c1 seul, NS = 1), contrôle `ant deux`
#    (le paramétrage « bloc » de l'étape 5 n'est PAS valable pour cette classe : R-122)
grep '^-19 100 ' recurrence_k1.txt | while read J K CE ex ey v rest; do x2=$((J-K+ex)); y2=$((K+ey)); r=ECHEC
  for p in 90 70 50 110 150 190 300; do o=$(BASE="$x2,$y2" T0=9977 $R/recherche/autoroute/ant multi $J $K $CE 1 $p 2>/dev/null | tail -1)
    if echo "$o" | grep -q 'TOUT OK'; then s1=$(echo "$o" | grep -o 's1=[0-9]*' | cut -d= -f2)
      d=$(BASE="$x2,$y2" T0=9977 $R/recherche/autoroute/ant deux $J $K $CE 1 $s1 2>/dev/null | grep -o 'COUPLAGE EXACT\|ECART')
      r="OK $(echo "$o" | grep -o 'regle=[0-9]*') $d"; break; fi; done; echo "$J $K c2=$x2,$y2 $r"; done > g1_fixe.txt
echo "R-96 : G1 (c1 = -119,100, c2 fixe) sans règle $(grep -c 'OK regle=0 COUPLAGE EXACT' g1_fixe.txt)/44 vérifications, avec règle $(grep -c 'OK regle=[1-9].*COUPLAGE EXACT' g1_fixe.txt) ;" \
     "G2 (d2 = d) sans règle $(grep -v '^-119,100' r96.txt | grep -c 'OK regle=0$')/8 (attendu : 42/44, 2, 7/8)"
