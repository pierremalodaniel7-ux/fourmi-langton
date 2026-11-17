# Ordinateur en UN germe : additionneur 2 bits (a1a0 + b1b0) + écran. Vérification 2 moteurs.
import add2, portes as Pt, sim, json
from add2 import E, gin, val, P, run2
d=json.load(open('add2.json')); CELLS=[tuple(c) for c in d['cases']]; SOR={int(k):tuple(v) for k,v in d['sorties'].items()}
Y=1100; T=150000
xb=lambda o: (o[2]-Y) if (o[0],o[1])==(-2,2) else (o[2]+Y)
PIX={v:xb(o) for v,o in SOR.items()}
def ecran(g):
    return {v:int(any(g.get((x,y),0) for x in range(px-5,px+6) for y in range(Y-4,Y+5))) for v,px in PIX.items()}
res={}; okp=0
for e in E:
    _,g,_,_=sim.run('RL|'+Pt.situ(gin(e)+[P()],extra=CELLS),T)
    lit=ecran(g); v=val(e); vs=[k for k,x in lit.items() if x]
    bits=None if len(vs)!=1 else (vs[0]>>2&1,vs[0]>>1&1,vs[0]&1)
    ok = vs==[v]; okp+=ok; res[str(e)]=dict(v=v,pixels=lit,bits=bits)
    print(f'a={e[0]}{e[1]} b={e[2]}{e[3]} : {e[0]*2+e[1]}+{e[2]*2+e[3]}={v} ; pixel allumé {vs} -> binaire {bits} {"OK" if ok else "FAUX"}')
r=run2([Pt.situ(gin(e)+[P()],extra=CELLS) for e in E],T)
okc=sum(1 for e,o in zip(E,r) if o!='BORD' and o[-1] and o[-1][:3]==SOR[val(e)])
print('écran (moteur Python) :',okp,'/16 ; sortie (moteur C) :',okc,'/16 ; pixels',PIX)
json.dump(dict(res=res,py=okp,c=okc,pix=PIX,cases=CELLS),open('add2_ecran.json','w'))
