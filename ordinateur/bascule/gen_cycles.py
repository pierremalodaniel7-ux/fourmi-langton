#!/usr/bin/env python3
"""Réflecteurs à fourmis (25/11) : germe R-20 (autoroute 104 vers (−2,+2)) + une pièce = petit cycle à 2 fourmis (cycles2.json),
à toutes les phases s, translations utiles (la bande de l'autoroute libre touche la boîte de l'orbite ; avancée réduite mod 4).
Fourmi 0 = la sonde (jouée en premier). Usage : gen_cycles.py D i0 i1 [fichier.idx] (orbites i0..i1−1) > lignes pour fourmi -retour."""
import sys, json
sys.path.insert(0, sys.path[0]); from moteur2 import charge, pas
G=[(0,1),(1,2),(2,3),(2,2),(2,1),(2,0),(3,0),(3,-1),(2,-2),(1,-2),(-2,-1)]
D=int(sys.argv[1]); C=json.load(open(sys.path[0]+'/cycles2.json'))
i0=int(sys.argv[2]) if len(sys.argv)>2 else 0; i1=int(sys.argv[3]) if len(sys.argv)>3 else len(C)
turn,ants,noir=charge("RL|0,0,B|"+';'.join(f'{x},{y}' for x,y in G)); V=set()
for t in range(104*(D+6)):
    if t>=104*(D-6): V.add((ants[0][0],ants[0][1]))
    pas(turn,ants,noir,[0])
idx=open(sys.argv[4] if len(sys.argv)>4 else '/dev/null','w'); n=0
for ic in range(i0,i1):
    c=C[ic]; turn,ants,noir=charge(c['situation']); p=c['periode']; etats=[]; vis=set()
    for s in range(p):
        etats.append(([list(a) for a in ants],set(noir)))
        for a in ants: vis.add((a[0],a[1]))
        pas(turn,ants,noir,range(len(ants)))
    mx=min(x for x,y in vis); my=min(y for x,y in vis)
    zone={(x-mx+dx,y-my+dy) for x,y in vis for dx in (-1,0,1) for dy in (-1,0,1)}
    for tx in range(-2*D-20,-2*D+21):
        for ty in range(2*D-20,2*D+21):
            if not (4*D<=-tx+ty<4*D+4): continue
            if not any((x+tx,y+ty) in V for x,y in zone): continue
            for s,(A,N) in enumerate(etats):
                fa=';'.join(f'{a[0]-mx},{a[1]-my},{a[2]}' for a in A)
                cases=[(x-tx,y-ty) for x,y in G]+[(x-mx,y-my) for x,y in N]
                print(f"RL|{-tx},{-ty},B;{fa}|"+';'.join(f'{x},{y}' for x,y in cases)); idx.write(f"{ic},{s},{tx},{ty}\n"); n+=1
sys.stderr.write(f"{n} situations\n")
