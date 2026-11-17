# E7 : CROISEMENT. X (↙) passe d'abord ; Y (↘) traverse sa trace (décalé de -4 si x=1) puis le collecteur 2 cases
# le renvoie ↙ sur une voie fixe. Test : la trace de sortie de Y est-elle IDENTIQUE (case par case) pour x=0 et x=1 ?
import portes as Pt, sim, json
c,s=-121,-391; T=60000
col=json.load(open('e6.json'))['collecteur']
res=[]
for cb,_ in col:
    cb=[tuple(x) for x in cb]; tr=[]
    for x in (0,1):
        g=([Pt.germe(0,0,0)] if x else [])+[Pt.germe((c+s)//2,(s-c)//2,3)]
        _,grid,_,pos=sim.run('RL|'+Pt.situ(g,extra=cb),T,trace=True)
        # trace de Y dans une fenêtre loin en aval de la sortie ↙ : cases noires (x-y entre -700 et -600)
        tr.append(frozenset(k for k,v in grid.items() if v and -700<=k[0]-k[1]<=-600 and abs(k[0]+k[1]-400)<40))
    res.append((cb,tr[0]==tr[1],len(tr[0]),len(tr[1])))
ok=[r for r in res if r[1] and r[2]>0]
print(len(ok),'/',len(res),'collecteurs donnent une trace de sortie identique ; exemples :',ok[:3])
json.dump([(r[0],r[1]) for r in res],open('e7.json','w'))
