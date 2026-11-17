# E3 : cases « aiguillage » : touchées par P sur une seule voie (0, -4 ou -8) et qui la font tourner proprement.
import portes as Pt, sim, sys, json
c,s,dB=-121,-391,64
def germes(a,b):
    g=[]
    if a: g.append(Pt.germe(0,0,0))
    if b: g.append(Pt.germe(dB,dB,0))
    g.append(Pt.germe((c+s)//2,(s-c)//2,3)); return g
E=[(0,0),(0,1),(1,0),(1,1)]
paths=[]
for a,b in E:
    st=Pt.situ(germes(a,b)); _,_,_,pos=sim.run('RL|'+st,40000,trace=True)
    vis={p[-1] for p in pos if 400<=p[-1][0]+p[-1][1]<=460}   # cases visitées par P dans la fenêtre
    paths.append(vis)
lane_of={0:[0],-4:[1,2],-8:[3]}
cands={}
for k,idx in lane_of.items():
    others=set().union(*[paths[i] for i in range(4) if i not in idx])
    mine=set.intersection(*[paths[i] for i in idx])
    cands[k]=sorted(mine-others)
    print('voie',k,len(cands[k]),'cases candidates')
tests=[];meta=[]
for k,cl in cands.items():
    for cell in cl:
        for a,b in E:
            tests.append(Pt.situ(germes(a,b),extra=[cell])); meta.append((k,cell,a,b))
r=Pt.run(tests,90000)
base=Pt.run([Pt.situ(germes(a,b)) for a,b in E],90000)
good=[]
from collections import defaultdict
byc=defaultdict(dict)
for (k,cell,a,b),o in zip(meta,r): byc[(k,cell)][(a,b)]=o
for (k,cell),d in byc.items():
    ok=True; desc=[]
    for i,(a,b) in enumerate(E):
        o=d[(a,b)]; bs=base[i]
        if o=='BORD' or o[-1] is None or any(x is None for x in o): ok=False; desc.append('sale'); continue
        p=o[-1]; inlane = i in lane_of[k]
        if inlane: ok&= (p[0],p[1])!=(2,2); desc.append((p[0],p[1],p[2]))
        else: ok&= p[:3]==bs[-1][:3]; desc.append('=')
    if ok: good.append((k,cell,desc))
for gd in good: print(gd)
json.dump([(k,list(cell),[str(x) for x in d]) for k,cell,d in good],open('e3_demux.json','w'))
