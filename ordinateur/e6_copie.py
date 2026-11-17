# E6 : COPIE (P tourne ↙ ssi a=1, A continue) et MIROIR COLLECTEUR (voies L et L-4 -> même sortie, 1 ou 2 cases).
import portes as Pt, sim, json, itertools
c,s=-121,-391; T=90000
def g(a): return ([Pt.germe(0,0,0)] if a else [])+[Pt.germe((c+s)//2,(s-c)//2,3)]
paths=[]
for a in (0,1):
    _,_,_,pos=sim.run('RL|'+Pt.situ(g(a)),40000,trace=True)
    paths.append(sorted({p[-1] for p in pos if 400<=p[-1][0]+p[-1][1]<=416}))
def outs(cells):
    r=Pt.run([Pt.situ(g(a),extra=cells) for a in (0,1)],T)
    return [None if (o=='BORD' or any(x is None for x in o)) else o[-1][:3] for o in r]
base=outs([])
# COPIE : cases du chemin a=1 absentes du chemin a=0
copie=[]
for cl in sorted(set(paths[1])-set(paths[0])):
    o=outs([cl])
    if o[0]==base[0] and o[1] and (o[1][0],o[1][1])==(-2,2): copie.append((cl,o[1]))
print('COPIE',len(copie),copie[:5])
# collecteur 1 case puis 2 cases
U=sorted(set(paths[0])|set(paths[1]))
col=[]
for k in (1,2):
    combos=list(itertools.combinations(U,k))
    sit=[Pt.situ(g(a),extra=list(cb)) for cb in combos for a in (0,1)]
    r=Pt.run(sit,T)
    for i,cb in enumerate(combos):
        o0,o1=r[2*i],r[2*i+1]
        if 'BORD' in (o0,o1) or any(x is None for x in o0+o1): continue
        a0,a1=o0[-1],o1[-1]
        if (a0[0],a0[1])!=(2,2) and a0[:3]==a1[:3]: col.append((cb,a0[:3]))
    print('collecteur',k,'cases :',len(col),col[:5],flush=True)
    if col: break
json.dump(dict(copie=copie,collecteur=col),open('e6.json','w'))
