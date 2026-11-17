import fa2, portes as Pt, sim, json
from fa import E, gin, P
T=90000; W=-281
fa2.W0,fa2.W1=380,700
pa=fa2.paths(W); base=Pt.run([Pt.situ(gin(e)+[P(W)]) for e in E],T)
k1=[e for e in E if sum(e)==1]
cand=sorted(set.union(*[pa[e] for e in k1]))
print(len(cand),'cases candidates')
r=Pt.run([Pt.situ(gin(f)+[P(W)],extra=[c]) for c in cand for f in E],T); good=[]
for i,c in enumerate(cand):
    ok=True
    for j,f in enumerate(E):
        o=r[8*i+j]
        if o=='BORD' or o[-1] is None: ok=False; break
        if sum(f)==1: ok&=(o[-1][0],o[-1][1])==(-2,2)
        else: ok&=o[-1][:3]==base[j][-1][:3]
    if ok: good.append(c)
print('S1 (relâché) :',len(good),good[:6])
json.dump([list(c) for c in good],open('fa_s1.json','w'))
