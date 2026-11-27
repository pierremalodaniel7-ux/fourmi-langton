#!/usr/bin/env python3
"""Réflecteurs « gomme » (25/11) : germe R-20 (autoroute 104 vers (−2,+2)) placé de sorte que la pièce soit autour de
l'origine (boîte [0,6]²) ; la pièce = k cases noires dans une boîte ≤ 7×7 (forme normalisée), toutes les translations
utiles (les cases de la pièce touchent la bande de l'autoroute libre ; avancée le long de l'autoroute réduite mod 4).
Usage : gen_pieces.py K D [W]  → lignes « situation » pour `src/fourmi -retour -boite -8,-8,14,14 -lot`."""
import sys, itertools
sys.path.insert(0, sys.path[0]); from moteur2 import charge, pas
G=[(0,1),(1,2),(2,3),(2,2),(2,1),(2,0),(3,0),(3,-1),(2,-2),(1,-2),(-2,-1)]
K=int(sys.argv[1]); D=int(sys.argv[2]); W=int(sys.argv[3]) if len(sys.argv)>3 else 7
turn,ants,noir=charge("RL|0,0,B|"+';'.join(f'{x},{y}' for x,y in G))
V=set()
for t in range(104*(D+6)):
    if t>=104*(D-6): V.add((ants[0][0],ants[0][1]))
    pas(turn,ants,noir,[0])
def formes(k):
    vus=set()
    for c in itertools.combinations([(x,y) for x in range(W) for y in range(W)],k):
        mx=min(x for x,y in c); my=min(y for x,y in c)
        f=tuple(sorted((x-mx,y-my) for x,y in c))
        if f not in vus: vus.add(f); yield f
n=0
for f in formes(K):
    for tx in range(-2*D-20,-2*D+21):
        for ty in range(2*D-20,2*D+21):
            a=-tx+ty
            if not (4*D<=a<4*D+4): continue
            S=[(x+tx,y+ty) for x,y in f]
            if not any(c in V for c in S): continue
            # translation : pièce en f (près de l'origine), germe en −t
            cases=[(x-tx,y-ty) for x,y in G]+list(f)
            print(f"RL|{-tx},{-ty},B|"+';'.join(f'{x},{y}' for x,y in cases)); n+=1
sys.stderr.write(f"{n} situations\n")
