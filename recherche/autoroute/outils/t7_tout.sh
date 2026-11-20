#!/bin/bash
# t7_tout.sh : chaîne T7 complète sur les bases finies (data/t7/b_<n>.txt) : triplets, récurrences k1 et m (bloc puis c3 fixe,
# chaque preuve recoupée par `ant deux`), directions, transport à deux étages, bilan. (S10 ; R-123 à R-127)
set -e; cd $(dirname $0)/../../..; O=recherche/autoroute/outils; W=data/t7
python3 $O/t7_triples.py > $W/triples.txt 2> $W/triples.err
$O/essai_k1_bloc.sh $W/triples.txt > $W/rec_k1.txt
awk '$NF!="ECHEC"' $W/rec_k1.txt | awk '{v=$NF; if(v=="NS0") print "multi",$2,$3,$4,0,$5,$6,$7,$8; else if($(NF-1)=="NS1"){split(v,a,"="); print "multi",$2,$3,$4,1,a[2],$5,$6,$7,$8} else print "multi",$2,$3,$4,2,$(NF-1),$NF,$5,$6,$7,$8}' > $W/audit_k1.in
$O/deux_mondes.sh < $W/audit_k1.in > $W/audit_k1.out 2>/dev/null
$O/essai_k1_c3fixe.sh $W/rec_k1.txt > $W/rec_k1_c3fixe.txt
python3 $O/essai_m_bloc.py $W/triples.txt > $W/rec_m.txt
python3 $O/essai_m_c3fixe.py $W/rec_m.txt $W/triples.txt > $W/rec_m_c3fixe.txt
python3 - > $W/directions.txt 2> $W/directions.err <<'P'
import subprocess,re,sys
from collections import Counter
T=[l.split() for l in open('data/t7/triples.txt') if not l.startswith('#')]; cfg=[]
for n,C,CE,*r in T: c=C.split(';'); cfg+=[f'RL|0,0,H|{c[0]}\n',f'RL|0,0,H|{c[0]};{c[1]}\n',f'RL|0,0,H|{C}\n']
o=subprocess.run(['src/fourmi','-T','400000000','-cert','-lot'],input=''.join(cfg),capture_output=True,text=True).stdout.splitlines()
d=lambda l:tuple(map(int,re.search(r' 104,(-?\d+),(-?\d+),',l).groups()))
rel=lambda a,b:'M' if a[0]*b[0]+a[1]*b[1]>0 else ('X' if a[0]*b[0]+a[1]*b[1]<0 else 'P')
cnt=Counter()
for i,(n,C,CE,*r) in enumerate(T):
    d2,d3,d4=d(o[3*i]),d(o[3*i+1]),d(o[3*i+2]); k=rel((-2,2),d2)+rel(d2,d3)+rel(d3,d4); cnt[k]+=1; print(n,C,k,d2,d3,d4)
print(dict(cnt),file=sys.stderr)
P
python3 $O/transport7.py > $W/transport7.bilan
echo "triplets : $(tail -1 $W/triples.err)"
echo "k1 bloc : $(grep -vc ECHEC $W/rec_k1.txt) OK (deux exacts $(grep -c 'COUPLAGE EXACT' $W/audit_k1.out)) ; c3 fixe : $(grep -c 'deux:COUPLAGE EXACT' $W/rec_k1_c3fixe.txt) OK exacts, $(grep -c ' ECHEC$' $W/rec_k1_c3fixe.txt) ECHEC"
echo "m bloc : $(grep -c 'deux:EXACT' $W/rec_m.txt) OK exacts, $(grep -c ' ECHEC$' $W/rec_m.txt) ECHEC ; c3 fixe : $(grep -c 'deux:EXACT' $W/rec_m_c3fixe.txt) OK exacts"
echo "transport : $(cat $W/transport7.bilan | tr '\n' ' ')"
