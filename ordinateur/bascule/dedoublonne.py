#!/usr/bin/env python3
"""dedoublonne.py cycles2.json → cycles2u.json : une entrée par orbite réelle (cases inertes retirées : orbite restreinte
aux cases visitées, à translation près)."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bascule import orbite, situ_piece
from moteur2 import charge, pas
C=json.load(open(sys.argv[1])); vus={}
for c in C:
    r,a,cc=c['situation'].split('|')
    A=[tuple(int(v) if v.lstrip('-').isdigit() else 'HDBG'.index(v) for v in x.split(',')) for x in a.split(';')]
    cells=[tuple(map(int,x.split(','))) for x in cc.split(';') if x]
    turn,an,no=charge(situ_piece(A,cells)); vis=set()
    for _ in range(c['periode']):
        for q in an: vis.add((q[0],q[1]))
        pas(turn,an,no,range(len(an)))
    cells=[p for p in cells if p in vis]                     # cases jamais visitées = inertes
    k=orbite(A,cells,c['periode'])
    if k not in vus: vus[k]={'situation':situ_piece(A,cells),'periode':c['periode'],'boite':c['boite']}
out=list(vus.values()); json.dump(out,open(sys.argv[2],'w'))
print(len(C),'→',len(out),'orbites réelles')
