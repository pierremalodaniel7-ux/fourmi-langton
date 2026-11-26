#!/usr/bin/env python3
"""delai.py honnetes.json i J... : bascule honnête i (2 impulsions sur la ligne a), 2e germe reculé de J périodes de plus
(délai ≈ 104·J pas). Le 2e tir rattrape-t-il le 1er (aller-retour exact) ? État de la pièce, destins (src/fourmi + moteur2)."""
import sys, json
from lib import *
hb=json.load(open(sys.argv[1]))[int(sys.argv[2])]
for J in map(int,sys.argv[3:]):
    r,A,C=parse(hb['situation']); g2=A[0]; dx,dy=2*J,-2*J
    A2=[(g2[0]+dx,g2[1]+dy,g2[2])]+A[1:]; C2=[(x+dx,y+dy) for x,y in C[-11:]]; C2=C[:-11]+C2
    sit=situ(A2,C2); T=hb['T']+104*J*3+60000
    (o,an,ce),=lot([sit],T,'dl','-retour'); f=o.split('|')
    b=Bascule({'hit':hb['hit'],'situation':sit,'T':T})
    print(f'J=+{J} : {f[3]} {f[4]} au pas {f[5]} ; {f[6][:80]} ; pièce {b.etat(an,ce)}')
    (o2,an2,ce2),=lot([sit],T,'dl'); A3,N3=py_final(sit,int(o2.split('|')[5]))
    print('    sans -retour :',o2.split('|')[3],o2.split('|')[6][:70],'; pièce',b.etat(an2,ce2),'; moteur2','identique' if A3==an2 and N3==ce2 else 'DIFFÉRENT')
