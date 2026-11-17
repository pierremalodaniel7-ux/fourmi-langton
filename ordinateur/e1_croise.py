# E1 : la fourmi P (↘ ou ↖) traverse la trace de A (↙). Voie de P sans A / avec A, pour toutes les classes.
import portes as Pt
from collections import defaultdict
T=40000
for rP in (3,1):
  print('P', '↘' if rP==3 else '↖')
  rows=[]
  for c in range(-124,-116):
    for k in range(4):
      s=-(190+2*k) if rP==3 else (190+2*k)
      if (s-c)%2: s-=1 if rP==3 else -1
      px,py=(c+s)//2,(s-c)//2
      gP=Pt.germe(px,py,rP); gA=Pt.germe(0,0,0)
      rows.append((c,s,gA,gP))
  sit=[]
  for c,s,gA,gP in rows: sit+= [Pt.situ([gP]), Pt.situ([gA,gP])]
  out=Pt.run(sit,T)
  cl=defaultdict(list)
  for i,(c,s,gA,gP) in enumerate(rows):
    seul=out[2*i][0]; a,p=out[2*i+1]
    if seul is None or p is None: res=('sale',)
    else: res=(p[0],p[1],p[2]-seul[2],p[3]-seul[3])  # dir, décalage de voie, retard
    cl[(c%4,(s-c)//2%2 if True else 0)].append(res)  # classe
    print(f' c={c} s={s} A={a} P={res}')
