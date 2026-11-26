#!/usr/bin/env python3
"""rattrapage.py J0 J1 : 2 germes R-20 SANS pièce, le 2e en amont en (2J+sh, −2J−sh+dp) du 1er (J ∈ [J0,J1), sh 0..3,
dp −8..8). RETOUR exact (src/fourmi -retour : la fourmi 1 en R(départ de la fourmi 0)) ? L'autre fourmi est-elle aussi en
R(départ de la 1re), et combien de cases diffèrent du départ (diff) ? → data/lecture/rattrapage_J0_J1.txt"""
import collections, sys
from lib import *
J0,J1=int(sys.argv[1]),int(sys.argv[2])
sits=[];meta=[]
for J in range(J0,J1):
    for sh in range(4):
        for dp in range(-8,9):
            gx,gy=2*J+sh,-2*J-sh+dp
            sits.append(situ([(gx,gy,2),(0,0,2)],G+[(x+gx,y+gy) for x,y in G])); meta.append((J,sh,dp))
R=lot(sits,int(os.environ.get('TT',40000)),'rt','-retour')
with open(f'../../data/lecture/rattrapage_{J0}_{J1}.txt','w') as f:
    for (J,sh,dp),(o,an,ce) in zip(meta,R):
        x=o.split('|')
        if x[3]=='RETOUR':
            d=int(x[6].split('diff=')[1].split()[0]); ok=tuple(an[0])==(0,-1,0)
            f.write(f'{J} {sh} {dp} RETOUR {x[5]} {d} {int(ok)}\n')
        else: f.write(f'{J} {sh} {dp} {x[3]} {" ".join(destins(o))}\n')
