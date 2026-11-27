#!/usr/bin/env python3
"""Petits cycles à 2 fourmis (+0 ou 1 case) dont la boîte reste ≤ 7×7 : candidats « pièce à fourmis ».
Étape 1 : écrit les situations (fourmi A en 0,0 ; B et la case dans [−3,3]²) ; étape 2 (arg 'lit') : lit la sortie de
src/fourmi -T 3000 et garde les CYCLE de boîte ≤ 7×7, dédoublonnés par orbite (toutes phases, translations)."""
import sys, itertools, json
sys.path.insert(0, sys.path[0]); from moteur2 import charge, pas
CAPS='HDBG'
if sys.argv[1]=='gen':
    R=range(-3,4)
    for da in range(4):
        for bx,by,db in itertools.product(R,R,range(4)):
            if (bx,by)==(0,0): continue
            if (0+(da%2==0))%2 == (bx+by+(db%2==0))%2: continue     # même classe ⇒ pas de cycle (R-09)
            print(f"RL|0,0,{CAPS[da]};{bx},{by},{CAPS[db]}|")
            for cx,cy in itertools.product(R,R): print(f"RL|0,0,{CAPS[da]};{bx},{by},{CAPS[db]}|{cx},{cy}")
else:
    vus={}; 
    for l in open(sys.argv[2]):
        f=l.split('|')
        if f[3]!='CYCLE': continue
        w,h=map(int,f[6].split('boite ')[1].split('x'))
        if w>7 or h>7: continue
        sit='|'.join(f[:3]); p=int(f[5])
        turn,ants,noir=charge(sit); orb=[]
        for t in range(p):
            mx=min([a[0] for a in ants]+[x for x,y in noir]); my=min([a[1] for a in ants]+[y for x,y in noir])
            orb.append((tuple(sorted((a[0]-mx,a[1]-my,a[2]) for a in ants)),tuple(sorted((x-mx,y-my) for x,y in noir))))
            pas(turn,ants,noir,[0,1])
        key=min(orb)
        if key not in vus: vus[key]=(sit,p,w,h)
    out=[{'situation':v[0],'periode':v[1],'boite':f'{v[2]}x{v[3]}'} for v in vus.values()]
    out.sort(key=lambda d:d['periode']); json.dump(out,open('cycles2.json','w'),indent=0)
    print(len(out),'orbites ; périodes',sorted(set(d['periode'] for d in out)))
