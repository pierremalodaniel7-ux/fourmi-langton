import json, subprocess
from banc import launcher, sit, rotv
from outils_r import lot, parse
R='H:R2L2'; G=json.load(open('data/germes_regles.json'))[R]; P,D=8,(1,-1)
B=((0,0,4),{(1,0):1}); A=((29,-56,0),{(28,-55):1})
def tracks(l,n):
    d=parse(l); return [((a[1],a[2]), a[1]*d['fin'][i][1]-a[2]*d['fin'][i][0]) if a else None for i,a in enumerate(d['ants'][:n])]
sA=tracks(lot([sit(R,[A[0]],A[1])],1<<16)[0],1)[0]; print('cible U',sA)
def st(n):
    out=subprocess.run(['./fourmi_r','-T',str(n*P),'-x','-dump','-lot'],input=sit(R,[B[0]],B[1])+'\n',capture_output=True,text=True).stdout
    return tuple(map(int,[l for l in out.splitlines() if l.startswith('DUMP')][0].split('|')[1].split(',')[:2]))
shown=0
for r in range(6):
  DK=rotv(R,D,r)
  if DK in (D,(-D[0],-D[1])): continue
  for i in range(-3,4):
   for j in range(-3,4):
    res=[]
    for n in range(40,48):
        Y=st(n); m=20
        s0=(Y[0]+m*D[0]-(n+m)*DK[0]+i, Y[1]+m*D[1]-(n+m)*DK[1]+j)
        K=launcher(G,r,s0); t=tracks(lot([sit(R,[B[0],K[0]],{**B[1],**K[1]})],1<<17,ncpu=1)[0],2)
        res.append(t[0][1] if t[0] and t[0][0]==sA[0] else None)
    if sum(x is not None for x in res)>=4: print(r,i,j,res, flush=True); shown+=1
    if shown>=6: raise SystemExit
