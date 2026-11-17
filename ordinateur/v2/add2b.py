import add2, portes as Pt, sim, json
from add2 import E, gin, val, P, run2
T=150000; cells=[]; sortie={}
def outs(extra):
    r=run2([Pt.situ(gin(e)+[P()],extra=extra) for e in E],T)
    return [None if o=='BORD' or o[-1] is None else o[-1][:3] for o in r]
cur=outs([])
for v in range(6):
    lo=800+160*v; hi=lo+60
    combos=[e for e in E if val(e)==v]
    sets=[]
    for e in combos:
        _,_,_,pos=sim.run('RL|'+Pt.situ(gin(e)+[P()],extra=cells),int(T*0.6),trace=True)
        sets.append({p[-1] for p in pos if lo<=p[-1][0]+p[-1][1]<=hi})
    cand=sorted(set.intersection(*sets)); found=None
    for i in range(0,len(cand),20):
        chunk=cand[i:i+20]
        r=run2([Pt.situ(gin(e)+[P()],extra=cells+[c]) for c in chunk for e in E],T)
        for j,c in enumerate(chunk):
            o=[None if x=='BORD' or x[-1] is None else x[-1][:3] for x in r[16*j:16*j+16]]
            new=[o[k] for k,e in enumerate(E) if val(e)==v]
            if None in o: continue
            if all(o[k]==cur[k] for k,e in enumerate(E) if val(e)!=v) and len(set(new))==1 and new[0][:2]!=(2,2):
                found=(c,new[0]); break
        if found: break
    if not found: print('v =',v,': pas de case (',len(cand),'candidates)'); break
    cells.append(found[0]); cur=outs(cells); sortie[v]=found[1]
    print(f'v = {v} : case {found[0]} -> sortie {found[1]} ({len(cand)} candidates)',flush=True)
sortie[6]=cur[E.index((1,1,1,1))]
print('sorties par valeur :',sortie)
json.dump(dict(cases=[list(c) for c in cells],sorties={str(k):v for k,v in sortie.items()}),open('add2.json','w'))
