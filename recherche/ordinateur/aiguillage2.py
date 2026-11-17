# Aiguillage incrémental des feuilles ↗ de K vers la clé (L*, A mod 4) ; 2 cases par feuille.
import module as Mo, construit as C, fourmis as F, json, sys
P=F.P; T=Mo.T
M=json.load(open('module_sans_aig.json'))
Lstar=int(sys.argv[1]); amod=int(sys.argv[2])
FEUILLES=[((1,1),(1,1,0)),((1,0,1),(1,0,1)),((0,1,1),(0,1,1))]
def essaie(br,e):
    cells,ants=Mo.config(M,e); w=Mo.idx(M,e,'K')
    hb,_=C.hw(cells,ants,w,T)
    if hb and hb[1]==2 and hb[2]==(Lstar,amod): return []      # déjà bonne (feuille partagée)
    X=Mo.interdit(M,'K',br); L_=[]
    for sp1 in (6,10,14,18):
        h,cand=C.candidats(cells,ants,w,T,0,sp1)
        for (x1,y1,u1) in cand or []:
            if (x1,y1) in X: continue
            h1,_=C.hw(cells+[(x1,y1)],ants,w,T,tmin=u1+2)
            if not h1 or h1[1]!=3: continue
            for sp2 in (6,9,12):
                _,cand2=C.candidats(cells+[(x1,y1)],ants,w,T,u1+2,sp2)
                for (x2,y2,u2) in cand2 or []:
                    if (x2,y2) in X: continue
                    h2,_=C.hw(cells+[(x1,y1),(x2,y2)],ants,w,T,tmin=u2+2)
                    if not h2 or h2[1]!=2 or h2[2][1]!=amod: continue
                    d=Lstar-h2[2][0]
                    if d<0 or d%4: continue
                    j=d//4; c2=(x2+2*j,y2+2*j)
                    if c2 in X: continue
                    ch=(h1[0]-u1)+(h2[0]-u2)
                    L_.append((ch,(x1,y1),c2))
    L_.sort()
    for best in L_[:40]:
        h3,_=C.hw(cells+[best[1],best[2]],ants,w,T)
        if h3 and h3[1]==2 and h3[2]==(Lstar,amod):
            print(br,"cases",best[1],best[2],"chaos",best[0],"t0",h3[0],flush=True)
            return [best[1],best[2]]
    return None
for br,e in FEUILLES:
    r=essaie(br,e)
    if r is None: print("ECHEC",br); sys.exit(1)
    for c in r: M['K']['nodes'].append({'cell':list(c),'cond':{},'br':'aig'+str(br)})
M['ray_out']=[Lstar,amod]
json.dump(M,open('module.json','w'))
