#!/usr/bin/env python3
"""2e moteur (indépendant de src/fourmi), règle RL seulement (ou LR) : n fourmis jouées l'une après l'autre.
Situation : 'RL|x,y,D;...|x,y;...'. Caps 0=H 1=D 2=B 3=G, y vers le bas, blanc -> droite.
Fonctions : charge(s), pas(etat, ordre), gomme(etat) = (x - e_h, h+2) pour chaque fourmi."""
import sys
DX=[(0,-1),(1,0),(0,1),(-1,0)]
CAP={'H':0,'D':1,'B':2,'G':3}
def charge(s):
    r,a,c=(s.strip().split('|')+['',''])[:3]
    tr={'R':1,'L':3}; turn=[tr[ch] for ch in r]
    ants=[]
    for f in a.split(';'):
        if not f.strip(): continue
        x,y,d=f.split(','); d=d.strip(); ants.append([int(x),int(y),CAP[d] if d in CAP else int(d)])
    noir={}
    for f in c.split(';'):
        if not f.strip(): continue
        p=f.split(','); col=int(p[2]) if len(p)>2 else 1
        if col%2: noir[(int(p[0]),int(p[1]))]=1
    return turn,ants,set(noir)
def pas(turn,ants,noir,ordre):
    for i in ordre:
        a=ants[i]; k=(a[0],a[1])
        if k in noir: noir.discard(k); a[2]=(a[2]+turn[1])%4
        else: noir.add(k); a[2]=(a[2]+turn[0])%4
        a[0]+=DX[a[2]][0]; a[1]+=DX[a[2]][1]
def gomme(ants):
    for a in ants: a[0]-=DX[a[2]][0]; a[1]-=DX[a[2]][1]; a[2]=(a[2]+2)%4
if __name__=='__main__':      # test de la gomme : moteur2.py "situation" t [inverse_ordre=1]
    s=sys.argv[1]; t=int(sys.argv[2]); inv=int(sys.argv[3]) if len(sys.argv)>3 else 1
    turn,ants,noir=charge(s); n=len(ants); n0=set(noir); a0=[list(a) for a in ants]
    for _ in range(t): pas(turn,ants,noir,range(n))
    print('après',t,'pas :',len(noir),'cases noires', end=' ; ')
    gomme(ants)
    for _ in range(t): pas(turn,ants,noir,range(n-1,-1,-1) if inv else range(n))
    gomme(ants)
    print('après gomme et',t,'pas :', 'grille = départ' if noir==n0 else f'{len(noir^n0)} cases différentes', ';',
          'fourmis = départ' if ants==a0 else 'fourmis ailleurs')
