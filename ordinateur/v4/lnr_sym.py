# R-72 LⁿR pour TOUT n ≥ N0 : simulation symbolique. Une couleur est (a,b) = a·n+b modulo n+1 (a ∈ {0,1}),
# le nombre de pas est (A,B) = A·n+B. Un « tour de carré » (4 virages L qui ramènent la fourmi à sa case et à son cap)
# est répété m fois d'un coup, m symbolique. Chaque décision « couleur == n ? » est tranchée pour tous les n ≥ N0 :
# on note la plus petite borne N0 qui rend toutes les décisions valides.
DX=(0,1,0,-1); DY=(-1,0,1,0)
N0=[1]
def need(k): N0[0]=max(N0[0],k)
def is_n(c):            # c == n ?
    a,b=c
    if a==1: return b==0          # n+b == n ssi b == 0 (b ≤ 0 constant)
    need(b+1); return False       # constante b < n dès que n ≥ b+1
def inc(c):
    a,b=c
    if a==1: return (0,0) if b==0 else (1,b+1)
    need(b+1); return (0,b+1)     # b+1 ≤ n
def reste(c):           # nombre de lectures « L » encore possibles avant de lire n : n - c
    a,b=c; return (1,-b) if a==0 else (0,-b)
def add(c,m):           # c + m (m ≤ n - c), réduit modulo n+1
    a,b=c; p,q=m; s=(a+p,b+q)
    if s[0]==2: s=(1,s[1]-1)
    return s
def smin(ms):
    k=[m for m in ms if m[0]==0]
    if k: return min(k)
    return (1,min(m[1] for m in ms))
def run(Kmax):
    g={}; x=y=0; d=0; t=(0,0); hist=[]
    for _ in range(Kmax):
        hist.append(((x,y,d),t,dict(g)))
        # tour de carré possible ?
        cells=[]; px,py,pd=x,y,d; ok=True
        for i in range(4):
            c=g.get((px,py),(0,0))
            if (px,py) in [p for p,_ in cells] or is_n(c): ok=False; break
            cells.append(((px,py),c)); pd=(pd+3)&3; px+=DX[pd]; py+=DY[pd]
        if ok and (px,py,pd)==(x,y,d):
            m=smin([reste(c) for _,c in cells])
            if m[0]==1:               # nombre de tours symbolique : on les fait d'un coup
                for p,c in cells: g[p]=add(c,m)
                t=(t[0]+4*m[0],t[1]+4*m[1]); continue
        c=g.get((x,y),(0,0)); d=(d+(1 if is_n(c) else 3))&3; g[(x,y)]=inc(c); x+=DX[d]; y+=DY[d]; t=(t[0],t[1]+1)
    return hist
H=run(400)
idx={h[1]:i for i,h in enumerate(H)}
i=idx.get((24,7)); j=idx.get((40,11))
print('etat au pas 24n+7 :',i is not None,' au pas 40n+11 :',j is not None)
(p0,t0,g0),(p1,t1,g1)=H[i],H[j]
v=(p1[0]-p0[0],p1[1]-p0[1]); print('deplacement',v,'caps',p0[2],p1[2])
# fenêtre lue entre i et j (cases sous la fourmi, y compris pendant les tours de carré)
W=set()
for k in range(i,j):
    (x,y,d),_,_=H[k]; W.add((x,y))
    if k+1<len(H) and H[k+1][1][0]>H[k][1][0]:   # tour de carré : 4 cases
        px,py,pd=x,y,d
        for _ in range(4): W.add((px,py)); pd=(pd+3)&3; px+=DX[pd]; py+=DY[pd]
Wr={(a-p0[0],b-p0[1]) for a,b in W}
same=all(g0.get((p0[0]+a,p0[1]+b),(0,0))==g1.get((p1[0]+a,p1[1]+b),(0,0)) for a,b in Wr)
new=[(a,b) for a,b in Wr if (a+v[0],b+v[1]) not in Wr]
white=all(g1.get((p1[0]+a,p1[1]+b),(0,0))==(0,0) for a,b in new)
ahead=[k for k in g0 if k not in W and g0[k]!=(0,0) and any((k[0]-p0[0]-a)*v[0]>0 for a,b in Wr) and False]
# toutes les cases devant (dans la bande, au-delà de la fenêtre) blanches au pas 24n+7 :
band=lambda c:(c[0]+c[1])
lo=min(band((p0[0]+a,p0[1]+b)) for a,b in Wr); hi=max(band((p0[0]+a,p0[1]+b)) for a,b in Wr)
fr=min(c[0]-c[1] for c in [(p0[0]+a,p0[1]+b) for a,b in Wr])
devant=[k for k,c in g0.items() if c!=(0,0) and lo<=band(k)<=hi and (k[0]-k[1])<fr]
print('motif identique sur la fenêtre (',len(Wr),'cases) :',same,'; cases neuves blanches :',white,len(new),'; cases non blanches devant :',len(devant))
print('valable pour tout n >=',N0[0])
# contre-vérification : instancier l'état symbolique au pas 24n+7 et le comparer à la simulation concrète
import lnr
for n in range(3,13):
    lu,pos,g=lnr.run(n,24*n+7)
    gs={k:(a*n+b)%(n+1) for k,(a,b) in g0.items()}
    gc={k:c for k,c in g.items()}
    eq=all(gs.get(k,0)==gc.get(k,0) for k in set(gs)|set(gc)) and (pos[-1][0],pos[-1][1],pos[-1][2])==p0
    print(n,'etat symbolique = simulation concrete :',eq)
# départ au plus tôt : au pas 24n+6 (index i-1, pas un tour de carré) le motif ne se répète pas 16n+4 pas plus tard ?
k=[q for q,h in enumerate(H) if h[1]==(24,6)]; l=[q for q,h in enumerate(H) if h[1]==(40,10)]
if k and l:
    (pa,_,ga),(pb,_,gb)=H[k[0]],H[l[0]]
    print('au pas 24n+6 : meme cap/decalage ?', (pb[0]-pa[0],pb[1]-pa[1])==v and pa[2]==pb[2],
          '; cases lues identiques ?', ga.get(pa[:2],(0,0))==gb.get(pb[:2],(0,0)))
