# R-71 application : R-17 (fourmi 0,0,H + 1 case noire dans [-5,5]², 120 cas) et un échantillon de 2 cases (R-17/R-24),
# chaque cas : simuler jusqu'à ce que le lemme 104 s'applique (test tous les 1 000 pas, max 300 000) ⇒ VÉRIFIÉ pour toujours.
import sys, random, json; sys.path.insert(0,'..'); import sim
from lemme104 import verifie
DX,DY=sim.DX,sim.DY
def cas(cells,Tmax=300000):
    g={c:1 for c in cells}; a=[0,0,0]
    for t in range(1,Tmax+1):
        k=(a[0],a[1]); c=g.get(k,0); a[2]=(a[2]+(1 if c==0 else 3))&3; g[k]=1-c; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]
        if t%1000==0 and t>=9000:
            ok,_=verifie(g,[tuple(a)])
            if ok: return t
    return None
P=[(x,y) for x in range(-5,6) for y in range(-5,6) if (x,y)!=(0,0)]
r1=[cas([p]) for p in P]
print('1 case :',sum(t is not None for t in r1),'/',len(P),'; lemme atteint au plus tard au pas',max(t for t in r1 if t),flush=True)
random.seed(18); S=random.sample([(p,q) for i,p in enumerate(P) for q in P[i+1:]],int(sys.argv[1]) if len(sys.argv)>1 else 100)
r2=[cas(list(s)) for s in S]
print('2 cases (échantillon) :',sum(t is not None for t in r2),'/',len(S),'; max',max([t for t in r2 if t] or [0]),flush=True)
json.dump(dict(un=dict(zip(map(str,P),r1)),deux=dict(zip(map(str,S),r2))),open('lemme_r17.json','w'))
