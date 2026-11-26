#!/usr/bin/env python3
"""lecture_b.py NOM S0 p0 S1 p1 ROT [D] : cherche une entrée de lecture b pour une pièce à 2 états (situations S0, S1 dans le
même repère, périodes p0, p1). Autoroute 104 neuve (germe R-20) arrivant du NE après rotation de la pièce de ROT×90°, sur chaque
voie qui passe à ≤ 12 de la pièce, 4 avancées, TOUTES les phases de S0 et de S1. Pour chaque tir : sortie de la sonde
(direction d'autoroute + voie) et état de la pièce après (S0 / S1 en place, '?' sinon). Écrit data/lecture/NOM_rROT.json.
LECTURE FORTE : une voie où toutes les phases de S0 → (S0, x) et toutes celles de S1 → (S1, y), x ≠ y.
LECTURE FAIBLE : une voie où au moins une phase de S0 → (S0, x) et au moins une de S1 → (S1, y ≠ x) (le circuit fixe la phase).
Calcul : src/fourmi -lot -dump (vérité), T = 25000 pas."""
import sys, json, collections
from lib import *
NOM,S0,p0,S1,p1,ROT=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4],int(sys.argv[5]),int(sys.argv[6])
D=int(sys.argv[7]) if len(sys.argv)>7 else 50; T=int(os.environ.get('TT',25000))
def rot(sit):
    r,A,C=parse(sit)
    for _ in range(ROT): A=[(-y,x,(d+1)%4) for x,y,d in A]; C=[(-y,x) for x,y in C]
    return situ(A,C,r)
S0r,S1r=rot(S0),rot(S1)
def orb_list(sit,p):
    turn,an,no=charge(sit); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],sorted(no))); pas(turn,an,no,range(len(an)))
    return L,vis
E0,V0=orb_list(S0r,p0); E1,V1=orb_list(S1r,p1)
K0={(tuple(a),frozenset(c for c in n if c in V0)) for a,n in E0}; K1={(tuple(a),frozenset(c for c in n if c in V1)) for a,n in E1}
npc=len(E0[0][0])
zone={(x+dx,y+dy) for x,y in V0|V1 for dx in range(-3,4) for dy in range(-3,4)}
lines=[]; meta=[]
for tx in range(-2*D-24,-2*D+25):
    for ty in range(2*D-24,2*D+25):
        if not (4*D<=-tx+ty<4*D+4): continue
        if not any(abs((x+y)-(-tx-ty))<=12 for x,y in zone): continue
        for nom,EE in (('S0',E0),('S1',E1)):
            for s,(A,N) in enumerate(EE):
                cells=[(x-tx,y-ty) for x,y in G]+list(N)
                lines.append(f"RL|{-tx},{-ty},B;"+';'.join(f'{x},{y},{d}' for x,y,d in A)+'|'+';'.join(f'{x},{y}' for x,y in cells)); meta.append((tx,ty,nom,s))
res=collections.defaultdict(list)
for (tx,ty,nom,s),(o,an,ce) in zip(meta,lot(lines,T,'lb')):
    P=tuple(an[1:1+npc]); st='S0' if (P,frozenset(c for c in ce if c in V0)) in K0 else ('S1' if (P,frozenset(c for c in ce if c in V1)) in K1 else '?')
    d=destins(o)[0]; a=an[0]
    sortie=f'{d}@{voie(a[0],a[1],d)}' if d!='-' else '-'
    res[f'{tx},{ty}'].append([nom,s,sortie,st])
os.makedirs('../../data/lecture',exist_ok=True)
json.dump(res,open(f'../../data/lecture/{NOM}_r{ROT}.json','w'))
def meme(x,y):
    if x=='-' or y=='-': return x==y
    (dx,lx),(dy,ly)=x.split('@'),y.split('@'); return dx==dy and abs(int(lx)-int(ly))<=4
forte=faible=0
for k,L in res.items():
    a=[(r[2]) for r in L if r[0]=='S0' and r[3]=='S0' and r[2]!='-']; b=[(r[2]) for r in L if r[0]=='S1' and r[3]=='S1' and r[2]!='-']
    n0=sum(1 for r in L if r[0]=='S0'); n1=sum(1 for r in L if r[0]=='S1')
    if a and b and any(not meme(x,y) for x in a for y in b):
        if len(a)==n0 and len(b)==n1 and all(meme(a[0],x) for x in a) and all(meme(b[0],y) for y in b) and not meme(a[0],b[0]):
            forte+=1; print('LECTURE FORTE',k,collections.Counter(a),collections.Counter(b))
        else:
            faible+=1; print('lecture faible',k,'S0:',dict(collections.Counter(a)),f'({len(a)}/{n0})','S1:',dict(collections.Counter(b)),f'({len(b)}/{n1})')
print(NOM,'r',ROT,':',len(lines),'tirs ;',len(res),'voies ; fortes',forte,'; faibles',faible)
