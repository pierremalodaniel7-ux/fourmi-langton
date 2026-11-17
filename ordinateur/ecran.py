# ecran.py — Objectif 3 : « écran » = bande horizontale y = 900. Chaque sortie ↙ du demi-additionneur (voie x+y = 337 pour S,
# 369 pour C) traverse la bande en x = voie − 900. Pixel allumé = au moins une case noire dans un carré 13×11 autour de ce point.
import sim, portes_def as D, json
Y=900; PIX={'S':337-Y,'C':369-Y}
res={}
for e,st in D.PORTES['demi-additionneur (S, C) à 1 puissance']['cas'].items():
    _,g,_,_=sim.run(st,90000)
    px={k:int(any(g.get((x,y),0) for x in range(x0-6,x0+7) for y in range(Y-5,Y+6))) for k,x0 in PIX.items()}
    autres=sum(v for (x,y),v in g.items() if Y-5<=y<=Y+5)   # cases noires sur toute la bande (bruit)
    res[str(e)]=px; print(e,'écran S,C =',px['S'],px['C'],' attendu',(e[0]^e[1],e[0]&e[1]))
json.dump(res,open('ecran.json','w'))
