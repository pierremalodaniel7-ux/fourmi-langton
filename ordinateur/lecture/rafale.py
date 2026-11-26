#!/usr/bin/env python3
"""rafale.py honnetes.json i N J SH : bascule honnête i ; on garde le 1er germe et on place N germes sur la même ligne, chacun
reculé de J périodes (+ SH le long de la ligne) par rapport au précédent (impulsions espacées de ≈ 104·J pas).
Chronologie de la pièce (moteur2, toutes les 100 pas) et sortie de chaque sonde (src/fourmi)."""
import sys, json
from lib import *
hb=json.load(open(sys.argv[1]))[int(sys.argv[2])]; N,J,SH=map(int,sys.argv[3:6])
b=Bascule(hb); r,A,C=parse(hb['situation']); g1=A[1]; P=A[2:]; Cp=C[11:-11]; G1=C[:11]
ants=[]; cells=list(G1)+list(Cp)
for k in range(1,N):
    dx,dy=(2*J+SH)*k,-(2*J+SH)*k; ants.append((g1[0]+dx,g1[1]+dy,g1[2])); cells+= [(x+dx,y+dy) for x,y in G1]
ants=ants[::-1]+[g1]+P          # fourmi 0 = dernière impulsion (comme chaine.py)
sit=situ(ants,cells); T=104*J*N+30000
(o,an,ce),=lot([sit],T,'rf'); ds=destins(o)
turn,a2,no=charge(sit); prev=None; log=[]
for t in range(T+1):
    if t%100==0:
        st=b.etat([tuple(a) for a in a2],no)
        if st!=prev: log.append((t,st)); prev=st
    if t<T: pas(turn,a2,no,range(len(a2)))
print('N',N,'J',J,'SH',SH,': chronologie',log)
print('   sorties (sonde 1 … N) :',ds[:N][::-1], '; moteur2', 'identique' if [tuple(a) for a in a2]==an and no==ce else 'DIFFÉRENT')
json.dump({'situation':sit,'T':T,'chronologie':log,'sorties':ds[:N][::-1]},open(f'../../data/lecture/rafale_{sys.argv[2]}_{N}_{J}_{SH}.json','w'))
