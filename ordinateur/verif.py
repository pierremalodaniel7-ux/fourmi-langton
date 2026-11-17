# verif.py — 2e programme indépendant (moteur Python sim.py) : rejoue toutes les tables de vérité de portes_def.py.
import sim, portes_def as D, json, sys
FL={(-2,2):'↙',(2,2):'↘',(-2,-2):'↖',(2,-2):'↗'}
def lit(st,T):
    _,_,_,pos=sim.run(st,T,trace=True); n=len(pos[0]); res=[]
    for i in range(n):
        d=(pos[-1][i][0]-pos[-105][i][0],pos[-1][i][1]-pos[-105][i][1])
        ok=all((pos[-1-k][i][0]-pos[-105-k][i][0],pos[-1-k][i][1]-pos[-105-k][i][1])==d for k in range(0,800,7))
        lane=min((p[i][0]+p[i][1]) if d[0]*d[1]<0 else (p[i][0]-p[i][1]) for p in pos[-104:])
        res.append((FL.get(d,'?') if ok else 'X',lane))
    return res
bilan={}
for nom,p in D.PORTES.items():
    juste=0
    for e,st in p['cas'].items():
        r=lit(st,p['T']); want=p['table'][e]
        if p['lire']=='tout': got=sorted(x[0] for x in r if x[0]=='↙')+(['↘'] if want==['↘'] and r[-1][0]=='↘' else [])
        elif p['lire']=='voie': got=r[-1][0] if r[-1][0]!='↙' else f"↙ voie {r[-1][1]} ({'S' if r[-1][1]==337 else 'C'})"
        else: got=r[p['lire']][0]
        w=sorted(want) if isinstance(want,list) else want
        ok= (got==w); juste+=ok
        print(f"{nom} {e}: attendu {want} obtenu {got} {'OK' if ok else 'FAUX'}  {r}",flush=True)
    bilan[nom]=f"{juste}/{len(p['cas'])}"
print(bilan); json.dump(bilan,open('verif_bilan.json','w'),ensure_ascii=False)
