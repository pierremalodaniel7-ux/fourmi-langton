# R-71 application à R-16 : bout d'autoroute de 11 cases (col.c) + 1 case noire sur chacune des 22 cases neuves d'une période,
# 10 périodes devant ; simuler jusqu'à ce que lemme104 s'applique (test tous les 1 000 pas, max 300 000).
import sys; sys.path.insert(0,'..'); import sim
from lemme104 import verifie
TIP=[(0,1),(1,2),(2,3),(2,2),(2,1),(2,0),(3,0),(3,-1),(2,-2),(1,-2),(-2,-1)]
DX,DY=sim.DX,sim.DY
def run(cells,Tmax=300000,collect=False):
    g={c:1 for c in TIP}
    for c in cells: g[c]=1-g.get(c,0)
    a=[0,0,2]; W=set()
    for t in range(1,Tmax+1):
        k=(a[0],a[1]); c=g.get(k,0)
        if collect: W.add(k)
        a[2]=(a[2]+(1 if c==0 else 3))&3; g[k]=1-c; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]
        if not collect and t%1000==0 and verifie(g,[tuple(a)])[0]: return t,a
    return (W,a) if collect else (None,a)
# cases lues pendant la 10e période (sans case ajoutée)
if __name__=="__main__":
    W9,_=run([],104*9,True); W10,_=run([],104*10,True); neuves=sorted(W10-W9)
    print('cases neuves de la 10e période :',len(neuves))
    res=[]
    for c in neuves:
        t,a=run([c]); res.append((c,t)); print(c,'lemme dès le pas',t,flush=True)
    print('R-16 :',sum(t is not None for _,t in res),'/',len(res),'VÉRIFIÉS pour toujours ; max',max(t for _,t in res if t))
    