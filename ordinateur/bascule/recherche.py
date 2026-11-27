#!/usr/bin/env python3
"""recherche.py fen.res [max] : pour chaque gomme (fenêtre effacée, dans=0) : état résiduel S1, classe
(pièce partie / identique / changée / non cyclique), puis 2e tir sur S1 (décalages s = 0..15) → JSON lignes sur stdout."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bascule import *
C2=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.environ.get('CY','cycles2.json'))))
def piece0(ic,s):
    c=C2[ic]; turn,ants,noir=charge(c['situation']); p=c['periode']; vis=set(); et=None
    for t in range(p):
        if t==s: et=([tuple(a) for a in ants],sorted(noir))
        for a in ants: vis.add((a[0],a[1]))
        pas(turn,ants,noir,range(len(ants)))
    mx=min(x for x,y in vis); my=min(y for x,y in vis)
    return [(x-mx,y-my,d) for x,y,d in et[0]],[(x-mx,y-my) for x,y in et[1]],p
mx=int(sys.argv[2]) if len(sys.argv)>2 else 10**9; n=0
for l in open(sys.argv[1]):
    if ' dans=0 ' not in ' '+l.split('|')[1]+' ': continue
    n+=1
    if n>mx: break
    ic,s,tx,ty=map(int,l.split('|')[0].split(','))
    A0,Cc0,p0=piece0(ic,s); gx,gy=-tx,-ty
    sit=germe_sit(gx,gy,A0,Cc0)
    out,ants,cells=tir(sit,20000)
    if not fenetre_propre(out): print(json.dumps({'id':[ic,s,tx,ty],'erreur':'fenetre non propre au rejeu'})); continue
    A1,C1,parties=residu(ants,[c for c in cells if c not in {(x+gx,y+gy) for x,y in G}])
    r={'id':[ic,s,tx,ty],'sit':sit,'t':out.split('|')[6],'parties':parties,'S1':situ_piece(A1,C1)}
    if parties>1 or not A1:
        r['classe']='pièce partie (fourmi(s) sortie(s))' if parties>1 else 'pièce vide'; print(json.dumps(r,ensure_ascii=False),flush=True); continue
    cy=cycle(A1,C1); r['S1_cycle']=cy
    if not cy.startswith('CYCLE'): r['classe']='S1 non cyclique'
    else:
        p1=int(cy.split()[1]); same=(p1==p0 and orbite(A1,C1,p1)==orbite(A0,Cc0,p0))
        r['classe']='identique (miroir)' if same else 'CHANGÉE (candidat)'
        res=[]
        for s2 in range(min(16,p1)):
            A2,C2b=avance(A1,C1,s2); o2,an2,ce2=tir(germe_sit(gx,gy,A2,C2b),20000)
            if fenetre_propre(o2):
                A3,C3,par3=residu(an2,[c for c in ce2 if c not in {(x+gx,y+gy) for x,y in G}])
                cy3=cycle(A3,C3) if par3<=1 else 'partie'
                ret0 = cy3.startswith('CYCLE') and int(cy3.split()[1])==p0 and orbite(A3,C3,p0)==orbite(A0,Cc0,p0)
                res.append([s2,'gomme',cy3,'RETOUR S0' if ret0 else ''])
            else: res.append([s2,o2.split('|')[4],o2.split('|')[5]])
        r['tir2']=res
    print(json.dumps(r,ensure_ascii=False),flush=True)
