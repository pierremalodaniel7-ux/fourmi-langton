# Croisement lecteur ↘ / rayon ↗ (voie 0, clé (0,0)) : issue par classe (A mod 4, L mod 4) du lecteur.
import fourmis as F
rc,ra=F.germe(-400,400,2)
vus={}
for x0 in range(0,8):
  for y0 in range(0,8):
    x=x0-1300; y=y0-1300          # lecteur ↘ loin en haut à gauche
    lc,la=F.germe(x,y,3)
    n,dh,xs,ys,fr=F.simule(lc,[la],30*104); h0=F.autoroute(dh,xs,ys)
    cl=(h0[2][0]%4,h0[2][1])
    if cl in vus: continue
    n,dh,xs,ys,fr=F.simule(rc+lc,[ra,la],250000,w=1); h=F.autoroute(dh,xs,ys)
    vus[cl]=1
    if h: print("classe",cl,"A0",h0[2][0],"->",F.FL[h[1]],h[2],"fin chaos",h[0])
    else: print("classe",cl,"-> rien")
