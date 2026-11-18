# fenêtre lue par l'autoroute 104 (RL) en une période, relative à la fourmi au début de la période
import sys; sys.path.insert(0,'..'); import sim
DX=sim.DX; DY=sim.DY
g={}; a=[0,0,0]; P=[]
for t in range(12000+104*4):
    k=(a[0],a[1]); c=g.get(k,0); a[2]=(a[2]+(1 if c==0 else 3))&3; g[k]=1-c; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]; P.append((t+1,a[0],a[1],a[2]))
# chercher t0 tel que la position à t0+104 = position t0 + v, même cap
t0=12000; x0,y0,d0=P[t0-1][1:]; x1,y1,d1=P[t0+104-1][1:]; v=(x1-x0,y1-y0); print('v',v,'cap',d0,d1)
# rejouer une période en notant les cases lues (case sous la fourmi avant chaque pas)
W=set(); px,py=x0,y0
for t in range(t0,t0+104):
    W.add((px-x0,py-y0)); px,py=P[t][1],P[t][2]
u=[x-y for x,y in W]; s=[x+y for x,y in W]
print('cases lues/periode',len(W),'x-y dans',min(u),max(u),'x+y dans',min(s),max(s))
# motif de reference sur W et W+v
Wv={(x+v[0],y+v[1]) for x,y in W}; new=Wv-W
print('cases nouvelles (W+v)\\W :',len(new),'couleurs ref:',set(g.get((x0+x,y0+y),0) for x,y in new) if False else '')
# couleurs de reference : g est l'etat a la fin (t0+4*104) ; recalculer a t0 et t0+104
def etat(T):
    g={}; a=[0,0,0]
    for t in range(T):
        k=(a[0],a[1]); c=g.get(k,0); a[2]=(a[2]+(1 if c==0 else 3))&3; g[k]=1-c; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]
    return g,a
g0,a0=etat(t0); g1,a1=etat(t0+104)
R0={w:g0.get((a0[0]+w[0],a0[1]+w[1]),0) for w in W}; R1={w:g1.get((a1[0]+w[0],a1[1]+w[1]),0) for w in W}
print('periodique (motif sur W identique a t0 et t0+104):',R0==R1, 'cap',a0[2],a1[2])
print('cases nouvelles blanches a t0+104 :',all(g1.get((a1[0]+w[0],a1[1]+w[1]),0)==0 for w in W if (w[0]+v[0],w[1]+v[1]) not in W), 'nb', sum(1 for w in W if (w[0]+v[0],w[1]+v[1]) not in W))
# demi-bande devant : jamais touchee avant t0 ? toutes les cases (x,y) avec x+y dans bande et x-y < min deja vu
touched=[k for k in g0 if (k[0]+k[1]-(a0[0]+a0[1])) in range(-4,7) and (k[0]-k[1])-(a0[0]-a0[1])<-5]
print('cases touchees devant la fenetre a t0 :',len(touched))
print('motif R0 (noires) :',sorted(w for w in W if R0[w]))
