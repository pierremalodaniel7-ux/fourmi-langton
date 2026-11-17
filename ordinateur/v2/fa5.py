import sys; sys.path.insert(0,'..')
import portes as Pt, sim, json
from fa import E, gin, P
T=110000; C1=(130,254)
st=lambda e,cells: Pt.situ(gin(e)+[P(-121)],extra=[C1]+cells)
_,_,_,p3=sim.run('RL|'+st((1,1,1),[]),60000,trace=True); _,_,_,p0=sim.run('RL|'+st((0,0,0),[]),60000,trace=True)
A=sorted({p[-1] for p in p3 if 600<=p[-1][0]+p[-1][1]<=660}-{p[-1] for p in p0})
print(len(A),'candidates')
base=Pt.run([st(e,[]) for e in E],T)
r=Pt.run([st(e,[c]) for c in A for e in E],T); good=[]
for i,c in enumerate(A):
    o=r[8*i:8*i+8]
    if any(x=='BORD' or x[-1] is None for x in o): continue
    if all(o[j][-1][:3]==base[j][-1][:3] for j,e in enumerate(E) if e!=(1,1,1)) and (o[7][-1][0],o[7][-1][1]) in ((2,-2),(-2,2)):
        good.append((c,o[7][-1][:3]))
print(len(good),good[:6]); json.dump([[list(c),l] for c,l in good],open('fa5.json','w'))
