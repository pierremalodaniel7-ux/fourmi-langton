#!/usr/bin/env python3
"""passe.py honnetes.json i A0 A1 DP : après la paire 1 (honnête), UNE impulsion de plus (germe en p1 + (a+dp, −a)) :
atteint-elle la pièce et l'écrit-elle (S0 → S1) ? État au pas (a+101)·52 + 4000 et sortie de la sonde. src/fourmi."""
import sys, json, collections
from lib import *
hb=json.load(open(sys.argv[1]))[int(sys.argv[2])]; b=Bascule(hb); A0,A1,DP=map(int,sys.argv[3:6])
r,A,C=parse(hb['situation']); p1=A[1]
res=collections.defaultdict(dict)
for a in range(A0,A1):
    sits=[];meta=[]
    for dp in range(-DP,DP+1):
        q=(p1[0]+a+dp,p1[1]-a); sits.append(situ([(q[0],q[1],2)]+A,C+[(x+q[0],y+q[1]) for x,y in G])); meta.append(dp)
    T=(a+101)*52+6000
    for dp,(o,an,ce) in zip(meta,lot(sits,T,'ps')): res[dp][a]=b.etat(an,ce)[1] if b.etat(an,ce)!='…' else '.'
for dp in sorted(res): print(f'{dp:4d}',''.join(res[dp][a] for a in range(A0,A1)))
n1=sum(v=='1' for d in res.values() for v in d.values()); n0=sum(v=='0' for d in res.values() for v in d.values())
print('BILAN : essais',sum(len(d) for d in res.values()),'; S1 (écrite)',n1,'; S0 (pièce intacte, pas atteinte)',n0,'; abîmée',sum(len(d) for d in res.values())-n0-n1)
