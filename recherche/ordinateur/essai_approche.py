# Approche : germe ↙ sur la voie L=l, case de virage -> ↘ ; puis croisement du rayon ↗ (voie 0).
import fourmis as F, construit as C, sys
P=F.P
l=int(sys.argv[1]); Aturn=int(sys.argv[2])
ray_c, ray_a = F.germe(-400,400,2)      # rayon ↗ voie x+y=0, part de A=-800
Aseed=Aturn+2000
for dA in range(4):
  A=Aseed+dA; x=(l+A)//2; y=l-x
  sc,sa=F.germe(x,y,0)
  T=60000
  # virage : chercher les cases qui donnent ↘ quand l'approche arrive vers Aturn
  sp=(2000//4)-25
  h,cand=C.candidats(sc,[sa],0,T,0,sp)
  for (cx,cy,u) in cand:
    h2,_=C.hw(sc+[(cx,cy)],[sa],0,T,tmin=u+2)
    if not h2 or h2[1]!=3: continue
    # croisement avec le rayon (sans le rayon / avec)
    T2=150000
    h0,_=C.hw(sc+[(cx,cy)],[sa],0,T2,tmin=u+2)
    h1,_=C.hw(sc+[(cx,cy)]+ray_c,[sa,ray_a],0,T2,tmin=u+2)
    print(dA,(cx,cy),"chaos virage",h2[0]-u,"cle0",h0[2] if h0 else None,"| avec rayon:",(F.FL[h1[1]],h1[2],h1[0]-h0[0]) if h1 else None)
