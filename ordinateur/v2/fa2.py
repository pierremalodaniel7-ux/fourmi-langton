import fa, portes as Pt, sim, json
from fa import E, gin, P
T=90000; W0,W1=520,600
def paths(w):
    out={}
    for e in E:
        _,_,_,pos=sim.run('RL|'+Pt.situ(gin(e)+[P(w)]),45000,trace=True)
        out[e]={p[-1] for p in pos if W0<=p[-1][0]+p[-1][1]<=W1}
    return out
def cells_for(w,k,target):
    pa=paths(w); mine=set.intersection(*[pa[e] for e in E if sum(e)==k]); others=set().union(*[pa[e] for e in E if sum(e)!=k])
    cand=sorted(mine|set())  # on teste toutes les cases du chemin de la voie k
    base=Pt.run([Pt.situ(gin(e)+[P(w)]) for e in E],T)
    r=Pt.run([Pt.situ(gin(e)+[P(w)],extra=[c]) for c in cand for e in E],T); good=[]
    for i,c in enumerate(cand):
        ok=True
        for j,e in enumerate(E):
            o=r[8*i+j]
            if o=='BORD' or o[-1] is None: ok=False; break
            if sum(e)==k: ok&=(o[-1][0],o[-1][1])==target
            else: ok&=o[-1][:3]==base[j][-1][:3]
        if ok: good.append((c,[r[8*i+j][-1][2] for j,e in enumerate(E) if sum(e)==k]))
    return good
if __name__=='__main__':
  res={}
  for nom,w,k,tg in [('S1',-281,1,(-2,2)),('S3',-281,3,(-2,2)),('C2',-121,2,(2,-2)),('C3',-121,3,(2,-2))]:
    g=cells_for(w,k,tg); res[nom]=g; print(nom,len(g),g[:4],flush=True)
  json.dump({k:[[list(c),l] for c,l in v] for k,v in res.items()},open('fa_cells.json','w'))
