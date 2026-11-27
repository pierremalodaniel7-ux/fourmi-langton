#!/usr/bin/env python3
"""tir3.py honnetes.json i : ajoute un 3e germe (voie décalée dp ∈ [−8,8], avancée mod 4, recul j périodes) à la bascule i ;
après le 3e tir, la pièce est-elle en S1 (en place) ? Fourmis : [sonde 3, sonde 2, sonde 1, pièce]. Calcul : src/fourmi -dump."""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
from bascule import G, E, dans, situ_piece
os.environ['CY']='cycles2.json'
import recherche_lib as RL
S1L=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cyclesS1.json')))
H=json.load(open(sys.argv[1])); h=H[int(sys.argv[2])]; J0,J1=int(sys.argv[3]),int(sys.argv[4])
def etats(sit,p):
    turn,an,no=charge(sit); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],set(no))); pas(turn,an,no,range(len(an)))
    return {(tuple(a),frozenset(c for c in no if c in vis)) for a,no in L}, vis
ic,s=h['hit']['S0'][:2]; A0,C0,p0=RL.piece0(ic,s); O0,V0=etats(situ_piece(A0,C0),p0)
e=S1L[h['hit']['S1']]; O1,V1=etats(e['situation'],e['periode'])
r,a,c=h['situation'].split('|'); ants=a.split(';'); g2=tuple(map(int,ants[0].split(',')[:2]))
lines=[]; meta=[]
for j in range(J0,J1):
    for dp in range(-8,9):
        for sh in range(4):
            # décalage : dp sur x+y, sh sur l'avancée (pas de 1 en x), recul j périodes
            gx=g2[0]+2*j+sh; gy=g2[1]-2*j+dp-sh
            g3=[(x+gx,y+gy) for x,y in G]
            if any(abs(x-g2[0])<8 and abs(y-g2[1])<8 for x,y in g3): continue
            sit=f'RL|{gx},{gy},2;'+a+'|'+c+';'+';'.join(f'{x},{y}' for x,y in g3)
            lines.append(sit); meta.append((j,dp,sh))
T=h['T']+104*(J1+40)
open('/tmp/claude-0/t3.txt','w').write('\n'.join(lines)+'\n')
if os.path.exists('/tmp/claude-0/t3.dump'): os.remove('/tmp/claude-0/t3.dump')
subprocess.run(f"{E} -T {T} -dump /tmp/claude-0/t3.dump -lot < /tmp/claude-0/t3.txt > /dev/null",shell=True)
ok=[]
for (j,dp,sh),l in zip(meta,open('/tmp/claude-0/t3.dump')):
    d=l.strip().split('|'); an=[tuple(map(int,x.split(','))) for x in d[-2].split(';')]
    ce={tuple(map(int,x.split(',')[:2])) for x in d[-1].split(';') if x}
    P=tuple(an[3:])
    if (P,frozenset(x for x in ce if x in V1)) in O1: ok.append((j,dp,sh,'S1'))
    elif (P,frozenset(x for x in ce if x in V0)) in O0: ok.append((j,dp,sh,'S0'))
print(len(lines),'essais ;',len([o for o in ok if o[3]=='S1']),'→ S1 ;',len([o for o in ok if o[3]=='S0']),'→ S0 (inchangé ?)')
print([o for o in ok if o[3]=='S1'][:20])
