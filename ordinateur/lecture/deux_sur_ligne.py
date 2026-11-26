#!/usr/bin/env python3
"""deux_sur_ligne.py : 2 germes R-20 SANS pièce ; le 2e en amont, en (2J+sh, −2J−sh+dp) du 1er (dp = décalage de voie).
Le 2e rattrape-t-il le 1er (RETOUR exact : une sonde en R(départ de l'autre)) ? Sinon, directions finales. src/fourmi."""
import collections, sys
from lib import *
J0,J1=(int(a) for a in sys.argv[1:3]) if len(sys.argv)>2 else (20,140)
sits=[];meta=[]
for J in range(J0,J1):
    for sh in range(4):
        for dp in range(-8,9):
            gx,gy=2*J+sh,-2*J-sh+dp
            sits.append(situ([(gx,gy,2),(0,0,2)],G+[(x+gx,y+gy) for x,y in G])); meta.append((J,sh,dp))
R=lot(sits,40000,'dl','-retour'); c=collections.Counter(); ex=collections.defaultdict(list)
for (J,sh,dp),(o,an,ce) in zip(meta,R):
    f=o.split('|'); k=('RETOUR',f[6].split()[1]) if f[3]=='RETOUR' else tuple(destins(o)); c[k]+=1; ex[k].append((J,sh,dp,f[5]))
for k,v in c.most_common(): print(v,k,ex[k][:5])
