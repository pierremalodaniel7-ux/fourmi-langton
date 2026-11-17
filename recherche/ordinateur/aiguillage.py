# Aiguillage des feuilles ↗ de K vers UNE même autoroute (même voie, même phase) : 2 cases par feuille.
import module as Mo, construit as C, fourmis as F, json, sys, collections
P=F.P; T=Mo.T
M=json.load(open('module.json'))
FEUILLES={(1,1):(1,1,0),(1,0,1):(1,0,1),(0,1,1):(0,1,1)}
def options(br,e):
    cells,ants=Mo.config(M,e); w=Mo.idx(M,e,'K')
    X=Mo.interdit(M,'K',br)
    res={}
    for sp1 in (6,10,14):
        h,cand=C.candidats(cells,ants,w,T,0,sp1)
        for (x1,y1,u1) in cand or []:
            if (x1,y1) in X: continue
            h1,_=C.hw(cells+[(x1,y1)],ants,w,T,tmin=u1+2)
            if not h1 or h1[1]!=3: continue
            for sp2 in (6,9,12):
                h1b,cand2=C.candidats(cells+[(x1,y1)],ants,w,T,u1+2,sp2)
                for (x2,y2,u2) in cand2 or []:
                    if (x2,y2) in X: continue
                    h2,_=C.hw(cells+[(x1,y1),(x2,y2)],ants,w,T,tmin=u2+2)
                    if not h2 or h2[1]!=2: continue
                    cl=(h2[2][0]%4,h2[2][1])
                    ch=(h1[0]-u1)+(h2[0]-u2)
                    if ch>20000: continue
                    # ramener à un point de référence : L2 - 4*(nb de périodes du 2e virage après le 1er)
                    if cl not in res or ch<res[cl][3]:
                        res[cl]=(h2[2][0],(x1,y1),(x2,y2),ch,h2[0],h1[2],u2)
    return res
R={}
for br,e in FEUILLES.items():
    R[br]=options(br,e); print(br,{k:(v[0],v[3]) for k,v in R[br].items()},flush=True)
com=set.intersection(*[set(r) for r in R.values()])
print("classes communes",com)
json.dump({str(k):{str(c):v for c,v in r.items()} for k,r in R.items()},open('aiguillage_options.json','w'))
