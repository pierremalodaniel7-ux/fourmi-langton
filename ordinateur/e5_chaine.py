# E5 : enchaînement automatique. Porte 1 = NOR(a,b) (case (141,260)) -> sortie O1 ↙.
# Porte 2 = puissance P2 ↘ qui croise la trace de O1, + case d'aiguillage => NON(O1) = OU(a,b).
import portes as Pt, sim, json, sys
c,s,dB=-121,-391,64; CELL1=(141,260)
E=[(0,0),(0,1),(1,0),(1,1)]
def g1(a,b):
    g=[]
    if a: g.append(Pt.germe(0,0,0))
    if b: g.append(Pt.germe(dB,dB,0))
    g.append(Pt.germe((c+s)//2,(s-c)//2,3)); return g
T=110000
found=None
for c2 in range(-304,-296):
  for s2 in (1901,1903,1905,1907):
    if (s2-c2)%2: continue
    P2=Pt.germe((c2+s2)//2,(s2-c2)//2,1)
    r=Pt.run([Pt.situ(g1(a,b)+[P2],extra=[CELL1]) for a,b in E],T)
    if any(o=='BORD' or o[-1] is None for o in r): print(c2,s2,'sale/bord'); continue
    lanes=[o[-1][2] if (o[-1][0],o[-1][1])==(-2,-2) else None for o in r]
    print(c2,s2,'voies P2',lanes)
    if None not in lanes and lanes[0]!=lanes[1] and lanes[1]==lanes[2]==lanes[3] and found is None: found=(c2,s2,lanes)

res={}
for c2 in range(-304,-296):
  for s2 in (1901,1903,1905,1907):
    if (s2-c2)%2: continue
    P2=Pt.germe((c2+s2)//2,(s2-c2)//2,1)
    paths=[]
    for a,b in [(0,0),(1,1)]:
        st=Pt.situ(g1(a,b)+[P2],extra=[CELL1]); _,_,_,pos=sim.run('RL|'+st,T,trace=True)
        paths.append({p[-1] for p in pos if 220<=p[-1][0]+p[-1][1]<=300})
    cand=sorted(paths[1]-paths[0])
    tests=[Pt.situ(g1(a,b)+[P2],extra=[CELL1,cl]) for cl in cand for a,b in E]
    r=Pt.run(tests,T); good=[]
    for i,cl in enumerate(cand):
        t=[]
        for j in range(4):
            o=r[4*i+j]
            t.append('?' if o=='BORD' or o[-1] is None else int((o[-1][0],o[-1][1]) in ((-2,2),(2,-2))))
        if t==[0,1,1,1]: good.append((cl,[(r[4*i+j][-1][0],r[4*i+j][-1][1]) for j in range(4)]))
    print(c2,s2,len(cand),'candidates ; OU justes :',good[:4],flush=True)
    if good: res[f'{c2},{s2}']=[g[0] for g in good]
json.dump(res,open('e5_ou.json','w'))
