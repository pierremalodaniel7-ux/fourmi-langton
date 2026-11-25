#!/usr/bin/env python3
"""dev.py F_dev.res : cas « la sonde repart en autoroute, la pièce reste dans la boîte ». Rejoue (src/fourmi, 20 000 pas),
état résiduel S1 (fourmis de la pièce + cases de la boîte), cycle exact ? même orbite que S0 ? → JSON lignes.
(La sonde = fourmi 0 ; elle est exclue du résidu.)"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bascule import *
import recherche_lib as RL
for l in open(sys.argv[1]):
    f=l.split('|'); ic,s,tx,ty=map(int,f[0].split(','))
    det=f[4].split(' boite')[0].split()[0].split(',')
    A0,C0,p0=RL.piece0(ic,s); gx,gy=-tx,-ty; sit=germe_sit(gx,gy,A0,C0)
    out,ants,cells=tir(sit,20000)
    germ={(x+gx,y+gy) for x,y in G}
    A1=[a for a in ants[1:] if dans(a[0],a[1])]; C1=sorted(c for c in cells if dans(*c) and c not in germ)
    r={'id':[ic,s,tx,ty],'sortie':det[1:3],'debut':det[3] if len(det)>3 else '','S1':situ_piece(A1,C1)}
    if len(A1)<len(ants)-1: r['classe']='pièce partie'
    else:
        cy=cycle(A1,C1,200000); r['S1_cycle']=cy
        if not cy.startswith('CYCLE'): r['classe']='S1 non cyclique'
        else:
            p1=int(cy.split()[1]); same=(p1==p0 and orbite(A1,C1,p1)==orbite(A0,C0,p0))
            r['classe']='même orbite' if same else 'CHANGÉE'; r['p0']=p0; r['p1']=p1
            if p1<=2000:                                   # taille de la zone vraiment visitée par S1
                turn,an,no=charge(situ_piece(A1,C1)); vis=set()
                for _ in range(p1):
                    for a in an: vis.add((a[0],a[1]))
                    pas(turn,an,no,range(len(an)))
                r['zone']=[min(x for x,y in vis),min(y for x,y in vis),max(x for x,y in vis),max(y for x,y in vis)]
    print(json.dumps(r,ensure_ascii=False),flush=True)
