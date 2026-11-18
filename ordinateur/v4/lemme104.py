# R-71 Lemme de l'autoroute 104 (RL), version vérifiable : si chaque fourmi lit le motif 104 sur sa fenêtre W (43 cases)
# et que son tube devant (∪_{k≥1} W+kv) est blanc, et que les demi-bandes (11 diagonales) des fourmis sont deux à deux
# disjointes, alors toutes restent en autoroute POUR TOUJOURS (récurrence sur les périodes, voir journal R-71).
import sys; sys.path.insert(0,'..'); import sim
DX,DY=sim.DX,sim.DY
def ref():
    g={}; a=[0,0,0]; st=[]
    for t in range(12000+2*104):
        if t>=12000 and t<12000+104: st.append((dict(g),tuple(a)))
        k=(a[0],a[1]); c=g.get(k,0); a[2]=(a[2]+(1 if c==0 else 3))&3; g[k]=1-c; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]
    # pour chaque phase p : fenêtre W_p (cases lues pendant les 104 pas suivants), motif, cap, v
    out=[]
    full=[]; a=[0,0,0]; g={}
    for t in range(12000+2*104+1):
        full.append((a[0],a[1],a[2]))
        k=(a[0],a[1]); c=g.get(k,0); a[2]=(a[2]+(1 if c==0 else 3))&3; g[k]=1-c; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]
    for p in range(104):
        G,A=st[p]; t=12000+p; x0,y0,d0=full[t]
        W={(full[s][0]-x0,full[s][1]-y0) for s in range(t,t+104)}
        R={w:G.get((x0+w[0],y0+w[1]),0) for w in W}
        v=(full[t+104][0]-x0,full[t+104][1]-y0)
        out.append((d0,W,R,v))
    return out
REF=ref()
ROT=lambda w,r: [(w[0],w[1]),(-w[1],w[0]),(-w[0],-w[1]),(w[1],-w[0])][r]   # rotation de r quarts de tour (sens horaire, y vers le bas)
PATS=[]
for r in range(4):
    for d0,W,R,v in REF:
        PATS.append(((d0+r)&3,{ROT(w,r):R[w] for w in W},ROT(v,r)))
def tube(x,y,W,v,K):
    return {(x+w[0]+k*v[0],y+w[1]+k*v[1]) for k in range(1,K) for w in W}
def bande(x,y,W,v):
    # demi-bande : perp = coordonnée constante le long de v ; along croissant dans le sens de v
    pe=(lambda c:c[0]+c[1]) if v[0]*v[1]<0 else (lambda c:c[0]-c[1])
    al=lambda c:(c[0]*v[0]+c[1]*v[1])
    P=[pe((x+w[0],y+w[1])) for w in W]; A=[al((x+w[0],y+w[1])) for w in W]
    return (v[0]*v[1]<0, min(P),max(P), min(A), pe, al)
def verifie(g,ants):
    """g : dict des cases (0 blanc), ants : liste (x,y,cap). Renvoie (ok, raison)."""
    nz=[k for k,c in g.items() if c]; info=[]
    for i,(x,y,d) in enumerate(ants):
        m=None
        for dd,R,v in PATS:
            if dd==d and all(g.get((x+w[0],y+w[1]),0)==c for w,c in R.items()): m=(R,v); break
        if m is None: return False,f'fourmi {i} : pas de motif 104'
        R,v=m; W=set(R); B=bande(x,y,W,v); info.append((x,y,W,v,B))
    for i,(x,y,W,v,B) in enumerate(info):
        diag,a,b,amin,pe,al=B
        # tube devant blanc : seules les cases non blanches et les autres fourmis comptent
        far=max([al(c) for c in nz]+[al((xx,yy)) for xx,yy,_ in ants]+[0])
        K=2; 
        while min(al((x+w[0]+K*v[0],y+w[1]+K*v[1])) for w in W) <= far: K+=1
        T=tube(x,y,W,v,K+1)-{(x+w[0],y+w[1]) for w in W}
        bad=[c for c in T if g.get(c,0)]
        if bad: return False,f'fourmi {i} : {len(bad)} case(s) non blanche(s) dans le tube'
        for j,(xx,yy,_) in enumerate(ants):
            if j!=i and ((xx,yy) in T or (xx-x-0,yy-y) in W and False): return False,f'fourmi {j} dans le tube de {i}'
    # demi-bandes deux à deux disjointes (sur-approximation : bande de perp ∈ [a,b], along ≥ amin)
    for i in range(len(info)):
        for j in range(i+1,len(info)):
            if not disjointes(info[i],info[j]): return False,f'demi-bandes {i} et {j} se coupent'
    return True,'toutes en autoroute 104 pour toujours'
def disjointes(I,J):
    # test par cases : les deux demi-bandes, coupées loin ; si directions non parallèles l'intersection est bornée
    (x,y,W,v,B),(xx,yy,WW,vv,BB)=I,J
    d1,a1,b1,m1,pe1,al1=B; d2,a2,b2,m2,pe2,al2=BB
    if d1==d2:   # même axe perp : parallèles ou opposées
        if b1<a2 or b2<a1: return True
        if v==vv: return False
        return m1+m2>0   # opposées (al2 = -al1) : disjointes ssi chacune est derrière l'autre
    # axes perpendiculaires : intersection = rectangle en (perp1, perp2) ; non vide ssi perp2 ∈ [a2,b2] compatible avec along1 ≥ m1
    for s in range(a1,b1+1):
        for u in range(a2,b2+1):
            if (s-u)%2: continue
            c=((s+u)//2,(s-u)//2) if d1 else ((s+u)//2,(u-s)//2)
            if pe1(c)==s and pe2(c)==u and al1(c)>=m1 and al2(c)>=m2: return False
            c=((u+s)//2,(u-s)//2) if d1 else ((u+s)//2,(s-u)//2)
            if pe1(c)==s and pe2(c)==u and al1(c)>=m1 and al2(c)>=m2: return False
    return True
if __name__=="__main__":
    for s,T in [("RL|0,0,H||",12000),("RL|0,0,H||",9000),("RL|0,0,H;40,0,G||",20000)]:
        ants,g,_,_=sim.run(s,T); print(s,T,verifie(g,[tuple(a) for a in ants]))
