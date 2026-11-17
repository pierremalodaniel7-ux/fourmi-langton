import fa, fa2, portes as Pt, json, itertools
from fa import E, gin, P
T=90000; W=-281
pa=fa2.paths(W); base=Pt.run([Pt.situ(gin(e)+[P(W)]) for e in E],T)
one={}
for e in [x for x in E if sum(x)==1]:
    cand=sorted(pa[e]); r=Pt.run([Pt.situ(gin(f)+[P(W)],extra=[c]) for c in cand for f in E],T); good=[]
    for i,c in enumerate(cand):
        ok=True
        for j,f in enumerate(E):
            o=r[8*i+j]
            if o=='BORD' or o[-1] is None: ok=False; break
            ok &= ((o[-1][0],o[-1][1])==(-2,2)) if f==e else (o[-1][:3]==base[j][-1][:3])
        if ok: good.append(c)
    one[e]=good; print(e,len(good),good[:5],flush=True)
cells=json.load(open('fa_cells.json'))
S3=[tuple(c) for c,_ in cells['S3']][:6]; C2=[tuple(c) for c,_ in cells['C2']][:6]; C3=[tuple(c) for c,_ in cells['C3']][:6]
def table(sc,cc):
    r=Pt.run([Pt.situ(gin(e)+[P(-281),P(-121)],extra=list(sc)+list(cc)) for e in E],T); out=[]
    for e,o in zip(E,r):
        if o=='BORD' or o[-2] is None or o[-1] is None: out.append(None); continue
        S=int((o[-2][0],o[-2][1])==(-2,2)); C=int((o[-1][0],o[-1][1])==(2,-2)); out.append((S,C))
    return out
want=[(sum(e)%2,int(sum(e)>=2)) for e in E]
found=None
for c1 in itertools.product(*[one[e][:3] for e in sorted(one)]):
    for s3 in S3[:3]:
        for c2 in C2[:3]:
            for c3 in C3[:3]:
                t=table(list(c1)+[s3],[c2,c3])
                if t==want: found=dict(S=[list(x) for x in list(c1)+[s3]],C=[list(c2),list(c3)]); break
            if found: break
        if found: break
    if found: break
print('additionneur complet :',found)
json.dump(found,open('fa_final.json','w'))
