# Croisement : lecteur ↘ traverse la trace d'une autoroute ↗ (voie x+y=0) posée avant lui.
import fourmis as F, collections
res=collections.Counter(); ex={}
rc,ra=F.germe(-600,600,2)          # rayon ↗ sur la voie x+y=0, part de A=-1200
for a in range(-16,16):            # voie du lecteur : x-y = a (approx)
  for ph in range(4):
    # lecteur ↘ partant de L = -2400-ph (loin : arrive après le rayon)
    Ls=-2400-ph; x=(Ls+a)//2; y=Ls-x
    lc,la=F.germe(x,y,3)
    n,dh,xs,ys,fr=F.simule(rc+lc,[ra,la],200000,w=1)
    h=F.autoroute(dh,xs,ys)
    k=(h[1] if h else None)
    ref=None
    res[k]+=1
    if h: ex.setdefault(k,[]).append((a,ph,h[0],h[2]))
print(res)
for k,v in ex.items(): print(F.FL[k], v[:6])
