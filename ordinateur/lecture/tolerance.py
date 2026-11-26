#!/usr/bin/env python3
"""tolerance.py honnetes.json i : la PAIRE ON/OFF (2 germes, géométrie de la bascule honnête i) translatée en bloc de (u + dp, −u)
(u = recul le long de la ligne, dp = décalage de voie x+y) : RETOUR exact (les 2 sondes en R(départ de l'autre)) avec la pièce
revenue exactement à son état du pas 0 ? src/fourmi -retour -dump."""
import sys, json, collections
from lib import *
hb=json.load(open(sys.argv[1]))[int(sys.argv[2])]; b=Bascule(hb)
r,A,C=parse(hb['situation']); Pa=A[2:]; Cp=C[11:-11]; G1,G2=C[:11],C[-11:]
sits=[];meta=[]
U0,U1=int(os.environ.get('U0',-6)),int(os.environ.get('U1',60))
for u in range(U0,U1):
    for dp in range(-12,13):
        tx,ty=u+dp,-u
        A2=[(A[0][0]+tx,A[0][1]+ty,2),(A[1][0]+tx,A[1][1]+ty,2)]+Pa
        sits.append(situ(A2,[(x+tx,y+ty) for x,y in G1]+Cp+[(x+tx,y+ty) for x,y in G2])); meta.append((u,dp))
R=lot(sits,40000,'tl','-retour'); ok=collections.defaultdict(list); c=collections.Counter()
for (u,dp),(o,an,ce) in zip(meta,R):
    f=o.split('|')
    if f[3]!='RETOUR': c['pas de retour']+=1; continue
    d=int(f[6].split('diff=')[1].split()[0]); P=tuple(tuple(a) for a in an[2:])
    if P==tuple(tuple(a) for a in Pa) and d==56: c['RETOUR exact, pièce = pas 0, diff 56']+=1; ok[dp].append(u)
    else: c[f'RETOUR, diff {d if d<100 else ">100"}, pièce {"= pas 0" if P==tuple(tuple(a) for a in Pa) else "autre"}']+=1
print(dict(c))
for dp in sorted(ok): print('  voie',dp,': reculs u =',ok[dp])
