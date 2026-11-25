#!/usr/bin/env python3
"""Petits cycles à N fourmis (+0 ou 1 case), boîte ≤ 7×7, au moins 2 fourmis de chaque classe I = x+y+cap mod 2
(nécessaire pour une bascule par échange : voir GOMME.md §2). gen N [ncases] > situations ; lit N fichier.out → cyclesN.json"""
import sys, itertools, json, random
sys.path.insert(0, sys.path[0]); from moteur2 import charge, pas
CAPS='HDBG'; R=range(-3,4)
if sys.argv[1]=='gen':
    N=int(sys.argv[2]); nc=int(sys.argv[3]) if len(sys.argv)>3 else 0
    pos=[(x,y,d) for x in R for y in R for d in range(4) if (x,y)!=(0,0)]
    for da in range(4):
        for autres in itertools.combinations(pos,N-1):
            if len({(x,y) for x,y,d in autres})<N-1: continue
            A=[(0,0,da)]+list(autres); cl=[(x+y+d)%2 for x,y,d in A]
            if min(cl.count(0),cl.count(1))<min(2,N//2) or (N==3 and min(cl.count(0),cl.count(1))<1): continue
            fa=';'.join(f'{x},{y},{CAPS[d]}' for x,y,d in A)
            if nc==0: print(f"RL|{fa}|")
            else:
                for cx,cy in itertools.product(R,R): print(f"RL|{fa}|{cx},{cy}")
else:
    N=int(sys.argv[2]); vus={}
    for l in open(sys.argv[3]):
        f=l.split('|')
        if f[3]!='CYCLE': continue
        w,h=map(int,f[6].split('boite ')[1].split('x'))
        if w>7 or h>7: continue
        sit='|'.join(f[:3]); p=int(f[5]); turn,ants,noir=charge(sit); orb=[]
        for t in range(p):
            mx=min([a[0] for a in ants]+[x for x,y in noir]); my=min([a[1] for a in ants]+[y for x,y in noir])
            orb.append((tuple(sorted((a[0]-mx,a[1]-my,a[2]) for a in ants)),tuple(sorted((x-mx,y-my) for x,y in noir))))
            pas(turn,ants,noir,range(len(ants)))
        key=min(orb)
        if key not in vus: vus[key]=(sit,p,w,h)
    out=[{'situation':v[0],'periode':v[1],'boite':f'{v[2]}x{v[3]}'} for v in vus.values()]
    out.sort(key=lambda d:d['periode']); json.dump(out,open(f'cycles{N}.json','w'),indent=0)
    print(len(out),'orbites ; périodes',sorted(set(d['periode'] for d in out))[:30])
