#!/usr/bin/env python3
"""temoin_trace.py honnetes.json i : contrôle. Après la 1re impulsion (pas t1 = 20000, la sonde 1 est partie), on envoie une
2e autoroute sur la même ligne (germe en g1 + (2J+sh, −2J−sh)) : (a) pièce réelle (S1 + trace de la sonde 1) ; (b) même trace,
mais pièce remplacée par S0 (toutes les phases) ; (c) pièce S1 propre (orbite seule, à toutes les phases), sans trace.
Compte (état final, sortie de la sonde 2). src/fourmi."""
import sys, json, collections
from lib import *
hb=json.load(open(sys.argv[1]))[int(sys.argv[2])]; b=Bascule(hb)
r,A,C=parse(hb['situation']); g1=A[1]; P=A[2:]; G1=C[:11]; Cp=C[11:-11]
sit1=situ([g1]+P,G1+Cp); t1=20000
(o,an,ce),=lot([sit1],t1,'tt'); probe=an[0]; Pc=an[1:]
V=b.V0|b.V1; zone={(x+dx,y+dy) for x,y in V for dx in (-1,0,1) for dy in (-1,0,1)}
trace=[c for c in ce if c not in zone]
L0,_,_=None,None,None
def orbit_list(A,C,p):
    turn,a2,no=charge(situ(A,C)); L=[]
    for _ in range(p): L.append(([tuple(x) for x in a2],sorted(no))); pas(turn,a2,no,range(len(a2)))
    return L
S0L=orbit_list(b.A0,b.C0,b.p0)
e1=S1C[hb['hit']['S1']]; _,A1,C1=parse(e1['situation']); S1L=orbit_list(A1,C1,e1['periode'])
cas={'a':[(Pc,[c for c in ce if c in zone])], 'b':S0L, 'c':S1L}
for nom,etats in cas.items():
    sits=[];meta=[]
    for J in range(8,40):
        for sh in range(4):
            gx,gy=g1[0]+2*J+sh,g1[1]-2*J-sh; G2=[(x-0+gx-g1[0],y+gy-g1[1]) for x,y in G1]
            for s,(Ap,Cz) in enumerate(etats):
                tr=trace if nom!='c' else []
                sits.append(situ([(gx,gy,2)]+[tuple(x) for x in Ap],G2+tr+list(Cz))); meta.append((J,sh,s))
    R=lot(sits,40000,'tt'+nom); c=collections.Counter()
    for (J,sh,s),(o2,a2,c2) in zip(meta,R):
        st=b.etat(a2,c2); c[(st,destins(o2)[0])]+=1
    print(nom,len(sits),'tirs :',dict(c.most_common(8)))
