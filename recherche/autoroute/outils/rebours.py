#!/usr/bin/env python3
"""rebours.py : dynamique inverse de la fourmi RL (y vers le bas, caps 0 H 1 D 2 B 3 G ; blanc -> droite).
Pas direct : lire c en a, h += (c ? -1 : +1), inverser a, avancer. Pas inverse : a_prec = a - dir(h), inverser a_prec,
c = couleur après inversion (= couleur lue au pas direct), h_prec = h - (c ? -1 : +1).
Usage : rebours.py "cases" CAP PAS  -> détecte une autoroute à rebours (trace périodique 104, dérive non nulle)."""
import sys
DX=[0,1,0,-1]; DY=[-1,0,1,0]
def direct(g,s):
    x,y,h=s; c=(x,y) in g; h=(h+(3 if c else 1))%4; g^={(x,y)}; return (x+DX[h],y+DY[h],h), c
def inverse(g,s):
    x,y,h=s; px,py=x-DX[h],y-DY[h]; g^={(px,py)}; c=(px,py) in g; hp=(h-(3 if c else 1))%4; return (px,py,hp), c
def autoroute(tr,pos):
    # plus petit t0 tel que la trace soit périodique 104 de t0 à la fin, avec au moins 20 périodes
    n=len(tr); k=n-1
    while k-104>=0 and tr[k]==tr[k-104]: k-=1
    t0=k+1
    if n-t0>=104*20:
        dx=pos[-1][0]-pos[-1-104][0]; dy=pos[-1][1]-pos[-1-104][1]
        if (dx,dy)!=(0,0): return t0,(dx,dy)
    return None
if __name__=='__main__':
    cells={tuple(map(int,c.split(','))) for c in sys.argv[1].split(';') if c}; h0='HDBG'.index(sys.argv[2]); T=int(sys.argv[3])
    g=set(cells); s=(0,0,h0)
    # contrôle : 2000 pas directs puis 2000 inverses redonnent l'état initial
    g2=set(cells); s2=s
    for _ in range(2000): s2,_=direct(g2,s2)
    for _ in range(2000): s2,_=inverse(g2,s2)
    assert s2==s and g2==cells, 'aller-retour faux'
    tr=[];pos=[]
    for t in range(T):
        s,c=inverse(g,s); tr.append(c); pos.append(s[:2])
    print('rebours :', autoroute(tr,pos))
