#!/usr/bin/env python3
"""balayage_delai.py honnetes.json i J0 J1 : bascule honnête i, 2e germe reculé de J ∈ [J0,J1) périodes de plus (avancée 0..3) :
état final de la pièce et directions de sortie des 2 sondes (src/fourmi, un lot)."""
import sys, json, collections
from lib import *
hb=json.load(open(sys.argv[1]))[int(sys.argv[2])]; J0,J1=int(sys.argv[3]),int(sys.argv[4])
b=Bascule(hb); r,A,C=parse(hb['situation']); g2=A[0]; sits=[]; meta=[]
for J in range(J0,J1):
    for sh in range(4):
        dx,dy=2*J+sh,-2*J-sh                   # avancée : +sh le long de la ligne (sous-période)
        if J==0 and sh==0: pass
        A2=[(g2[0]+dx,g2[1]+dy,g2[2])]+A[1:]; C2=C[:-11]+[(x+dx,y+dy) for x,y in C[-11:]]
        sits.append(situ(A2,C2)); meta.append((J,sh))
T=hb['T']+104*J1*2+40000
R=lot(sits,T,'bd'); c=collections.Counter()
for (J,sh),(o,an,ce) in zip(meta,R):
    ds=destins(o); st=b.etat(an,ce); c[(st,ds[0],ds[1])]+=1
    print(J,sh,st,ds[:2])
print(c)
