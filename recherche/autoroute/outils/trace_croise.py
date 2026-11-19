#!/usr/bin/env python3
"""É7 « autoroute × trace » (S9). Trace = germe R-20 (0,0,B) déroulé P périodes (cases noires seulement, sans fourmi),
tournée de 90° et décalée de (a,b). Fourmi : germe R-20 d'origine en (0,0,B). Écrit des lignes pour `fourmi -cert -lot`.
Usage : trace_croise.py P A0 A1 B0 B1 [rot]   (pas de calcul de vérité ici : seul `src/fourmi` juge)"""
import sys
G=[(0,1),(1,2),(2,3),(2,2),(2,1),(2,0),(3,0),(3,-1),(2,-2),(1,-2),(-2,-1)]
DX=[(0,-1),(1,0),(0,1),(-1,0)]  # H D B G, y vers le bas
def deroule(P):
    noir=set(G); x,y,h=0,0,2
    for _ in range(104*P):
        if (x,y) in noir: noir.remove((x,y)); h=(h+3)%4   # noir -> gauche (RL : blanc -> droite)
        else: noir.add((x,y)); h=(h+1)%4
        x+=DX[h][0]; y+=DX[h][1]
    return noir
P,a0,a1,b0,b1=map(int,sys.argv[1:6]); rot=int(sys.argv[6]) if len(sys.argv)>6 else 1
T=deroule(P)
for _ in range(rot): T={(-y,x) for x,y in T}
base=';'.join(f'{x},{y}' for x,y in G)
for a in range(a0,a1):
    for b in range(b0,b1):
        S=set(G)^{(x+a,y+b) for x,y in T}
        if (0,0) in S: continue
        sys.stderr.write(f'{a},{b}\n'); print(f'RL|0,0,B|'+';'.join(f'{x},{y}' for x,y in sorted(S)))
