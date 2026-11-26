#!/usr/bin/env python3
"""familles.py : pièces pour rlem.py (nuit 26/11), dédoublonnées par rotation (les tirs couvrent déjà les 4 directions).
 f2c : cycle de base d'une bascule connue (185/186, 572, 1020 sans leur case) + 2 cases isolées : la case connue + 1 case à
       distance 1..3 (Tchebychev) des cases visitées, jamais visitée.   → data/rlem/f2c_pieces.json
 f4  : cycles de 4 fourmis (cycles4.json), sans case, les N plus petits (période, boîte).        → data/rlem/f4_pieces.json
 f4c : les mêmes + 1 case isolée à distance 1..2 (échantillon régulier).                        → data/rlem/f4c_pieces.json"""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lecture'))
from lib import charge, pas, situ, parse
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../bascule'); O=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../data/rlem')
def orb(A,C,p):
    turn,an,no=charge(situ(A,C)); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],sorted(no))); pas(turn,an,no,range(len(an)))
    return L,vis
def canon(A,C,p):
    """forme canonique à rotation, translation et phase près (cases noires comprises, toutes)"""
    best=None
    for r in range(4):
        Ar,Cr=A,C
        for _ in range(r): Ar=[(-y,x,(d+1)%4) for x,y,d in Ar]; Cr=[(-y,x) for x,y in Cr]
        L,vis=orb(Ar,Cr,p)
        for an,no in L:
            pts=[(a[0],a[1]) for a in an]+list(no); mx=min(x for x,y in pts); my=min(y for x,y in pts)
            k=(tuple(sorted((a[0]-mx,a[1]-my,a[2]) for a in an)),tuple(sorted((x-mx,y-my) for x,y in no)))
            if best is None or k<best: best=k
    return best
def avec_cases(base,p,extra,dmin,dmax,fixe=()):
    _,A,C=parse(base); L,vis=orb(A,C,p)
    ring=[(x+dx,y+dy) for x,y in vis for dx in range(-dmax,dmax+1) for dy in range(-dmax,dmax+1)]
    ring=sorted({c for c in ring if c not in vis and min(max(abs(c[0]-x),abs(c[1]-y)) for x,y in vis)>=dmin} - set(fixe))
    return [(A,list(C)+list(fixe)+[c]) for c in ring]
def ecrit(nom,pieces):
    vus={}; 
    for A,C,p in pieces:
        k=canon(A,C,p)
        if k not in vus: vus[k]={'nom':f'{nom}{len(vus)}','situation':situ(A,C),'periode':p}
    json.dump(list(vus.values()),open(f'{O}/{nom}_pieces.json','w')); print(nom,len(pieces),'→',len(vus),'pièces (rotations)')
os.makedirs(O,exist_ok=True)
C2=json.load(open(f'{B}/cycles2.json'))
if 'f2c' in sys.argv:
    P=[]
    for ic in (185,186,572,1020):
        sit=C2[ic]['situation']; p=C2[ic]['periode']; r,A,C=parse(sit)
        L,vis=orb(A,[],p); known=[c for c in C if c not in vis]; base=situ(A,[c for c in C if c in vis])
        for A2,C2b in avec_cases(base,p,1,1,3,fixe=known): P.append((A2,C2b,p))
    ecrit('f2c',P)
if 'f4' in sys.argv:
    N=int(os.environ.get('N4',120)); C4=json.load(open(f'{B}/cycles4.json'))
    def taille(e): w,h=map(int,e['boite'].split('x')); return (e['periode'],w*h)
    C4=sorted(C4,key=taille); P=[]
    for e in C4:
        r,A,C=parse(e['situation']); P.append((A,C,e['periode']))
        if len(P)>=4*N: break
    vus=set(); Q=[]
    for A,C,p in P:
        k=canon(A,C,p)
        if k in vus: continue
        vus.add(k); Q.append((A,C,p))
        if len(Q)>=N: break
    ecrit('f4',Q)
    if 'f4c' in sys.argv:
        R=[]
        for A,C,p in Q[:int(os.environ.get('N4C',30))]:
            V=avec_cases(situ(A,C),p,1,1,2); R+=[(a,c,p) for a,c in V[::max(1,len(V)//8)]]
        ecrit('f4c',R)
