# schema.py — placement en couches du circuit d'un pas, minimisation des croisements (barycentres + échanges), image.
import json, random
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
NET=[tuple(g) for g in json.load(open('pas.json'))['net']]
INP=['c00','c10','c01','c11','x','y','h1','h0']
lay={i:0 for i in INP}
for g in NET: lay[g[0]]=1+max(lay[i] for i in g[2:])
edges=[(i,g[0]) for g in NET for i in g[2:]]
# nœuds fictifs pour les arêtes longues
L=max(lay.values()); nodes={k:[n for n in lay if lay[n]==k] for k in range(L+1)}; E=[]
for a,b in edges:
    prev=a
    for k in range(lay[a]+1,lay[b]):
        d=f'·{a}>{b}:{k}'; nodes[k].append(d); lay[d]=k; E.append((prev,d)); prev=d
    E.append((prev,b))
def crossings(order):
    pos={n:i for k in order for i,n in enumerate(order[k])}; c=0
    for k in range(L):
        es=[(pos[a],pos[b]) for a,b in E if lay[a]==k]
        for i in range(len(es)):
            for j in range(i+1,len(es)):
                if (es[i][0]-es[j][0])*(es[i][1]-es[j][1])<0: c+=1
    return c
order={k:list(v) for k,v in nodes.items()}; print('croisements avant :',crossings(order))
best=crossings(order); random.seed(1)
for it in range(60):
    for k in (list(range(1,L+1)) if it%2==0 else list(range(L-1,-1,-1))):
        pos={n:i for kk in order for i,n in enumerate(order[kk])}
        nb={n:[pos[a] for a,b in E if b==n] if it%2==0 else [pos[b] for a,b in E if a==n] for n in order[k]}
        order[k].sort(key=lambda n:sum(nb[n])/len(nb[n]) if nb[n] else pos[n])
    improved=True
    while improved:
        improved=False
        for k in order:
            for i in range(len(order[k])-1):
                o=order[k]; o[i],o[i+1]=o[i+1],o[i]; c=crossings(order)
                if c<best: best=c; improved=True
                else: o[i],o[i+1]=o[i+1],o[i]
print('croisements après minimisation :',best)
pos={n:i for k in order for i,n in enumerate(order[k])}
f,ax=plt.subplots(figsize=(13,8))
for a,b in E: ax.plot([lay[a],lay[b]],[-pos[a],-pos[b]],color='#888',lw=0.8)
typ={g[0]:g[1] for g in NET}; col={'NON':'#e45','ET':'#26a','OU':'#2a6','XOR':'#a5c','COPIE':'#999'}
for n in lay:
    if n.startswith('·'): continue
    t=typ.get(n,'entrée'); ax.scatter(lay[n],-pos[n],s=260,color=col.get(t,'#000'),zorder=3)
    ax.text(lay[n],-pos[n]+0.35,f'{n}' + (f' ({t})' if t!='entrée' else ''),ha='center',fontsize=7)
ax.set_title(f"Circuit d'un pas de la fourmi RL sur le tore 2×2 : 22 portes + 19 copies, {best} croisements (placement en couches) — 256/256",fontsize=10)
ax.axis('off'); f.savefig('schema_pas.png',dpi=110,bbox_inches='tight')
json.dump(dict(croisements=best,couches=L+1),open('schema.json','w'))
