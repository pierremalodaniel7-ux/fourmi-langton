import compilateur as C, json
tests={'demi-additionneur (a,b) → S, C':(2,['a','b'],[('S',lambda m:(m&1)^(m>>1&1)),('C',lambda m:(m&1)&(m>>1&1))]),
       'module cap ± 1 : (h0,h1,c) → h1\', h0\'':(3,['h0','h1','c'],[("h1'",lambda m:(m&1)^(m>>1&1)^(m>>2&1)),("h0'",lambda m:1-(m&1))])}
R={}
for nom,(n,noms,s) in tests.items():
    p=C.compile_(s,n,noms); okc,N,T,_=C.verifie(p,s,'C'); okp,_,_,_=C.verifie(p,s,'Py')
    nb=len(p['gates']); print(f'{nom} : {nb} portes niv.1, {sum(1 for o in p["outs"] if o["niv"]==2)} niv.2 ; T={T} ; moteur C {okc}/{N}, Python {okp}/{N}')
    R[nom]=dict(plan=p,okC=okc,okPy=okp,N=N,T=T)
json.dump(R,open('test_comp.json','w'),ensure_ascii=False,indent=1,default=str)
