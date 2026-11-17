# Additionneur complet à 1 puissance + 1 case (130,254) ; lecture sur la bande y = Y (2e moteur : sim.py).
import sys; sys.path.insert(0,'..')
import portes as Pt, sim, json
from fa import E, gin, P
Y=900; T=110000; CELL=(130,254); CELL2=(231,369)
# sortie selon k : (direction, voie) -> point de passage sur la bande
PIX={0:('↘',-126),1:('↙',337),2:('↙',369),3:('↙',597)}
def xb(d,l): return l-Y if d=='↙' else l+Y
res={}; ok=0
for e in E:
    st='RL|'+Pt.situ(gin(e)+[P(-121)],extra=[CELL,CELL2])
    _,g,_,_=sim.run(st,T)
    lit={k:int(any(g.get((x,y),0) for x in range(xb(*PIX[k])-5,xb(*PIX[k])+6) for y in range(Y-4,Y+5))) for k in PIX}
    S=int(lit[1] or lit[3]); C=int(lit[2] or lit[3]); want=(sum(e)%2,int(sum(e)>=2))
    ok+=(S,C)==want and sum(lit.values())==1
    res[str(e)]=dict(pixels=lit,S=S,C=C,attendu=want); print(e,'pixels k0..k3',[lit[k] for k in range(4)],'-> S,C =',S,C,'attendu',want)
r=Pt.run([Pt.situ(gin(e)+[P(-121)],extra=[CELL,CELL2]) for e in E],T)   # 1er moteur (C)
c_ok=sum(1 for e,o in zip(E,r) if o!='BORD' and o[-1] and ({0:((2,2),-126),1:((-2,2),337),2:((-2,2),369),3:((-2,2),597)}[sum(e)]==((o[-1][0],o[-1][1]),o[-1][2])))
print('écran (Python) :',ok,'/ 8 ; sorties (moteur C) :',c_ok,'/ 8')
json.dump(dict(ecran=res,C=c_ok,py=ok),open('fa_ecran.json','w'),ensure_ascii=False)
