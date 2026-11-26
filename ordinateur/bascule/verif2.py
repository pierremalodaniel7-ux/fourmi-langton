#!/usr/bin/env python3
"""verif2.py fichier.res N [CY] : rejoue N gommes (fenêtre effacée) avec le 2e moteur (moteur2.py, Python) jusqu'au pas
indiqué par src/fourmi ; vérifie que la fenêtre x∈[35,75], y∈[−75,−35] est redevenue blanche et compare les positions finales."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
from bascule import germe_sit
import recherche_lib as RL
n=int(sys.argv[2]); ok=0; k=0
for l in open(sys.argv[1]):
    f=l.split('|')
    if not f[1].startswith('dans=0 '): continue
    k+=1
    if k>n: break
    ic,s,tx,ty=map(int,f[0].split(',')); T=int(f[3][1:]) if f[2]=='RETOUR' else 20000
    A0,C0,p0=RL.piece0(ic,s); sit=germe_sit(-tx,-ty,A0,C0)
    turn,ants,noir=charge(sit); ini=set(noir)
    for _ in range(T): pas(turn,ants,noir,range(len(ants)))
    W=[(x,y) for x in range(35,76) for y in range(-75,-34)]
    propre=all(((c in noir)==(c in ini)) for c in W)
    fin=f[4] if False else l.split(' fin ')[1].split()
    pos=[f'{a[0]},{a[1]}' for a in ants]
    same=all(p.startswith(q) or q.startswith(p) for p,q in zip([','.join(x.split(',')[:2]) for x in fin],pos))
    ok+=propre and same; print(f[0],'T',T,'fenêtre blanche' if propre else 'FENÊTRE SALE','positions =' if same else 'positions ≠',flush=True)
print(ok,'/',min(k,n),'confirmés')
