# R-73 lemme d'autoroute GÉNÉRIQUE (toute règle carrée, groupe de fourmis voyageant ensemble, aucune autre fourmi) :
# au temps t, les fourmis (dans l'ordre) lisent pendant P tours une fenêtre W ; si au temps t+P (a) positions = positions(t)+v,
# mêmes caps, (b) motif sur W+v à t+P = motif sur W à t, (c) toutes les cases non blanches à t hors de W sont « derrière »
# (jamais dans un W+kv, k ≥ 1), alors le groupe se répète pour toujours (récurrence : ne lit que W+kv, déjà blanc).
import sys; sys.path.insert(0,'..'); import sim
DX,DY=sim.DX,sim.DY
def step(r,ants,g,reads=None):
    K=[sim.TURN[c] for c in r]; q=len(r)
    for a in ants:
        k=(a[0],a[1]); c=g.get(k,0)
        if reads is not None: reads.add(k)
        a[2]=(a[2]+K[c])&3; g[k]=(c+1)%q; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]
def preuve(s,t,P):
    r,ants,g=sim.parse(s)
    for _ in range(t): step(r,ants,g)
    A0=[tuple(a) for a in ants]; g0=dict(g); W=set()
    for _ in range(P): step(r,ants,g,W)
    A1=[tuple(a) for a in ants]; v=(A1[0][0]-A0[0][0],A1[0][1]-A0[0][1])
    if v==(0,0) or any((b[0]-a[0],b[1]-a[1],b[2])!=(v[0],v[1],a[2]) for a,b in zip(A0,A1)): return False,'pas de translation commune'
    if any(g.get((x+v[0],y+v[1]),0)!=g0.get((x,y),0) for x,y in W): return False,'motif différent'
    # tube : ∪_{k≥1}(W+kv) hors de W doit être BLANC au temps t (les cases neuves de chaque période sont blanches)
    al=lambda c:c[0]*v[0]+c[1]*v[1]
    nz=[c for c,col in g0.items() if col]+[(a[0],a[1]) for a in A0]
    far=max(al(c) for c in nz)
    K=1
    while min(al((x+K*v[0],y+K*v[1])) for x,y in W)<=far: K+=1
    tube={(x+k*v[0],y+k*v[1]) for k in range(1,K+1) for x,y in W}-W
    bad=[c for c in tube if g0.get(c,0)]
    if bad: return False,f'{len(bad)} cases non blanches dans le tube'
    return True,f'v={v} P={P} |W|={len(W)} : pour toujours'
if __name__=="__main__":
    for s,t,P in [("LLR|3,1,H;1,2,H|",2000,6),("LLR|0,0,H||",2000,18),("RL|0,0,H||",12000,104),("RL|0,0,H||",9000,104),
                  ("LLR|0,1,G;0,-3,G;-1,-2,H;3,-2,H|",4000,6)]:
        print(s,t,P,preuve(s,t,P))
