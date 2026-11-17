# pas.py — Étape 1 : circuit logique d'UN pas de la fourmi RL sur le tore 2×2 (8 bits), vérifié contre la vraie simulation.
# État : cases c00 c10 c01 c11 (case (x,y)), position x y, cap h1 h0 (0=H 1=D 2=B 3=G, y vers le bas).
import itertools, json
DX=[0,1,0,-1]; DY=[-1,0,1,0]
def vrai_pas(s):
    c,x,y,h=dict(s['c']),s['x'],s['y'],s['h']
    col=c[(x,y)]; h=(h+(3 if col else 1))%4; c[(x,y)]=1-col
    return dict(c=c,x=(x+DX[h])%2,y=(y+DY[h])%2,h=h)
# --- le circuit (liste de portes, ordre topologique) ---
NET=[('nx','NON','x'),('ny','NON','y'),('nh0','NON','h0'),
     ('s00','ET','nx','ny'),('s10','ET','x','ny'),('s01','ET','nx','y'),('s11','ET','x','y'),      # décodeur 2→4
     ('m00','ET','c00','s00'),('m10','ET','c10','s10'),('m01','ET','c01','s01'),('m11','ET','c11','s11'),
     ('o1','OU','m00','m10'),('o2','OU','m01','m11'),('c','OU','o1','o2'),                          # multiplexeur : couleur lue
     ('t','XOR','h1','h0'),("h1'",'XOR','t','c'),("h0'",'COPIE','nh0'),                               # cap ± 1
     ("x'",'XOR','x','nh0'),("y'",'XOR','y','h0'),                                                    # avancer sur le tore
     ("c00'",'XOR','c00','s00'),("c10'",'XOR','c10','s10'),("c01'",'XOR','c01','s01'),("c11'",'XOR','c11','s11')]
OPS={'NON':lambda a:1-a,'ET':lambda a,b:a&b,'OU':lambda a,b:a|b,'XOR':lambda a,b:a^b,'COPIE':lambda a:a,'NOR':lambda a,b:1-(a|b)}
def evalue(v):
    v=dict(v)
    for g in NET: v[g[0]]=OPS[g[1]](*[v[i] for i in g[2:]])
    return v
ok=0
for bits in itertools.product((0,1),repeat=8):
    c00,c10,c01,c11,x,y,h1,h0=bits
    s=dict(c={(0,0):c00,(1,0):c10,(0,1):c01,(1,1):c11},x=x,y=y,h=2*h1+h0)
    t=vrai_pas(s); v=evalue(dict(c00=c00,c10=c10,c01=c01,c11=c11,x=x,y=y,h1=h1,h0=h0))
    got=(v["c00'"],v["c10'"],v["c01'"],v["c11'"],v["x'"],v["y'"],v["h1'"],v["h0'"])
    want=(t['c'][(0,0)],t['c'][(1,0)],t['c'][(0,1)],t['c'][(1,1)],t['x'],t['y'],t['h']>>1,t['h']&1)
    ok+=got==want
from collections import Counter
uses=Counter(i for g in NET for i in g[2:]); copies=sum(n-1 for n in uses.values() if n>1)
cnt=Counter(g[1] for g in NET if g[1]!='COPIE')
print('circuit d\'un pas :',ok,'/ 256 états justes')
print('portes :',dict(cnt),'total',sum(cnt.values()),'; copies (sorties utilisées plusieurs fois) :',copies, dict((k,n) for k,n in uses.items() if n>1))
json.dump(dict(net=NET,ok=ok,portes=dict(cnt),copies=copies),open('pas.json','w'),ensure_ascii=False)
