# add3.py — additionneur 3 bits en un germe, cases PRÉDITES par la règle (pas de recherche). Poids 1,2,4 = 1, 2, 4 germes parallèles.
import sys; sys.path.insert(0,'..')
import portes as Pt, sim, itertools, json, time
from concurrent.futures import ProcessPoolExecutor
E=list(itertools.product((0,1),repeat=6))   # (a2,a1,a0,b2,b1,b0)
def gin(e):
    a2,a1,a0,b2,b1,b0=e; slots=[a0]+[b0]+[a1]*2+[b1]*2+[a2]*4+[b2]*4
    return [Pt.germe(64*i,64*i,0) for i,on in enumerate(slots) if on]
val=lambda e: (e[2]+e[5])+2*(e[1]+e[4])+4*(e[0]+e[3])
m=256; CELLS=[(341+2*m+78*v,460+2*m+82*v) for v in range(14)]
P=Pt.germe((-121-391)//2,(-391+121)//2,3)
T=300000
def one(e):
    _,_,_,pos=sim.run('RL|'+Pt.situ(gin(e)+[P],extra=CELLS),T,trace=True)
    i=len(pos[0])-1; d=(pos[-1][i][0]-pos[-105][i][0],pos[-1][i][1]-pos[-105][i][1])
    st=all((pos[-1-k][i][0]-pos[-105-k][i][0],pos[-1-k][i][1]-pos[-105-k][i][1])==d for k in range(0,1500,7))
    lane=min((p[i][0]+p[i][1]) if d[0]*d[1]<0 else (p[i][0]-p[i][1]) for p in pos[-104:])
    return e,val(e),d if st else None,lane
if __name__=='__main__':
    t=time.time()
    with ProcessPoolExecutor(2) as ex: res=list(ex.map(one,E))
    byv={}
    for e,v,d,l in res: byv.setdefault(v,set()).add((d,l))
    ok=all(len(s)==1 for s in byv.values()) and len({list(s)[0] for s in byv.values()})==len(byv)
    for v in sorted(byv): print(v,byv[v])
    print('64 entrées :', 'TOUTES LES VALEURS DISTINCTES ET COHÉRENTES' if ok else 'ÉCHEC', f'({time.time()-t:.0f} s)')
    json.dump(dict(ok=ok,byv={str(k):[list(map(str,x)) for x in v] for k,v in byv.items()},cases=CELLS),open('add3.json','w'))
