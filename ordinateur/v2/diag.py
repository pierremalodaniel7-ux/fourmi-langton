import sys; sys.path.insert(0,'..')
import banc1, sim
from collections import Counter
banc1.F='../../src/fourmi'
s1='RL|0,0,H;-2,0,B;-2,2,D|-44,-95;-43,-95'
f=banc1.fourmi_lot([s1],600000)[0]; print(f[3:5],f[6][:200])
ants,_=banc1.details(f); u=(-2,-2)
idx=[i for i,a in enumerate(ants) if a and (a[1],a[2])==u]; t0=max(ants[i][3] for i in idx); t1=t0+5*104
_,_,_,pos=sim.run(s1,t1+105,trace=True)
fresh=sorted({(p[i][0]+8*u[0],p[i][1]+8*u[1]) for p in pos[t1:t1+104] for i in idx})
out=banc1.fourmi_lot([s1+';'+f'{x},{y}' for x,y in fresh],600000)
print(Counter((o[3],o[4]) for o in out).most_common(8))
# même test sur le Tandem d'origine pour comparer : dans quel état interne est la paire ?
print('écart des 2 fourmis restantes (pas t1):',[pos[t1][i] for i in idx], 'Tandem:', sim.run('RL|0,0,H;-2,0,B|',2000,trace=True)[3][1999])
