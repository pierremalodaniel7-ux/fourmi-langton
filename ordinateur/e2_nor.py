# E2 : la fourmi P (↘, voie x-y=c) traverse les traces de A et B (↙). Voie finale de P selon (a,b).
import portes as Pt, sys
T=60000
def cas(c,s,ka,kb,dA,dB,a,b):
    g=[]
    if a: g.append(Pt.germe(dA,-dA+ka,0))       # A : ↙ partant de (dA, -dA+ka) : voie x+y = ka
    if b: g.append(Pt.germe(dB,-dB+kb,0))
    px,py=(c+s)//2,(s-c)//2
    g.append(Pt.germe(px,py,3)); return Pt.situ(g)
res={}
rows=[]
for c in (-123,-121,-119,-117):          # classes de voie de P
  for s in (-391,-393,-395,-397):        # phases de P (départ loin derrière => arrive après A et B)
    for dB in (60,64,68):                 # position de B le long de P (B plus loin sur le chemin de P)
      rows.append((c,s,dB))
sit=[cas(c,s,0,dB*2 if False else 0,0,0,0,0) for c,s,dB in rows]
out=[]
for c,s,dB in rows:
    four=[]
    for a in (0,1):
        for b in (0,1):
            four.append(cas(c,s,0,2*dB,0,dB,a,b))   # B : germe en (dB, -dB+2dB)=(dB,dB) voie x+y=2dB
    out.append(four)
flat=[x for f in out for x in f]; r=Pt.run(flat,T)
for i,(c,s,dB) in enumerate(rows):
    lanes=[]
    for j in range(4):
        p=r[4*i+j]
        if p=='BORD': lanes.append('BORD'); continue
        q=p[-1]; lanes.append(None if q is None else (q[0],q[1],q[2]))
    base=lanes[0][2] if lanes[0] else None
    print(c%4, c, s, dB, ['sale' if l is None else (l if l=='BORD' else (l[0],l[1],l[2]-base)) for l in lanes])
