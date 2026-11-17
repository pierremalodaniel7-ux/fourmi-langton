# regles.py — piste 3 : quelles translations gardent l'additionneur 2 bits juste ? (moteur C, 16 entrées par test)
import add2, portes as Pt, json
from add2 import E, val, run2
d=json.load(open('add2.json')); CELLS=[tuple(c) for c in d['cases']]; SOR={int(k):tuple(v) for k,v in d['sorties'].items()}
BASE={'a0':(0,0),'b0':(64,64),'a1':(128,128),'a1b':(192,192),'b1':(256,256),'b1b':(320,320)}
def build(e,mv=None,glob=(0,0),Pshift=(0,0),cshift=(0,0)):
    mv=mv or {}; a1,a0,b1,b0=e; on={'a0':a0,'b0':b0,'a1':a1,'a1b':a1,'b1':b1,'b1b':b1}
    g=[]
    for k,(x,y) in BASE.items():
        if not on[k]: continue
        dx,dy=mv.get(k,(0,0)); g.append(Pt.germe(x+dx+glob[0],y+dy+glob[1],0))
    w,s=-121,-391; px,py=(w+s)//2,(s-w)//2; g.append(Pt.germe(px+Pshift[0]+glob[0],py+Pshift[1]+glob[1],3))
    return Pt.situ(g,extra=[(x+glob[0]+cshift[0],y+glob[1]+cshift[1]) for x,y in CELLS])
def test(nom,T=150000,expect_shift=(0,0,0),**kw):
    r=run2([build(e,**kw) for e in E],T); ok=0
    for e,o in zip(E,r):
        if o=='BORD' or o[-1] is None: continue
        s=SOR[val(e)]; want=(s[0],s[1],s[2]+expect_shift[0] if (s[0],s[1])==(-2,2) else s[2]+expect_shift[1])
        ok+= o[-1][:3]==want
    print(f'{nom:62s} {ok}/16',flush=True); return ok
R={}
R['translation globale (37,-11)']=test('translation globale (37,-11)',glob=(37,-11),expect_shift=(26,48))
R['translation globale (-100,64)']=test('translation globale (-100,64)',glob=(-100,64),expect_shift=(-36,-164))
for n in (-20,-5,5,20):
    R[f'a0 glissé le long de son axe de {n}×(2,-2)']=test(f'a0 glissé le long de son axe de {n}×(2,-2)',mv={'a0':(2*n,-2*n)})
for n in (5,40):
    R[f'P reculée de {n}×(-2,-2)']=test(f'P reculée de {n}×(-2,-2)',T=150000+104*n,Pshift=(-2*n,-2*n))
for k,lab in ((1,'(1,1)'),(2,'(2,2)'),(8,'(8,8)')):
    R[f'b0 décalé sur le côté de {lab}']=test(f'b0 décalé sur le côté de {lab}',mv={'b0':(k,k)})
R['b0 décalé de (1,0)']=test('b0 décalé de (1,0)',mv={'b0':(1,0)})
R['cases glissées de 3×(2,2) le long de P']=test('cases glissées de 3×(2,2) le long de P',cshift=(6,6),expect_shift=(12,0))
json.dump(R,open('regles.json','w'),ensure_ascii=False,indent=1)
