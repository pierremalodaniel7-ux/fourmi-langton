# Construit le module additionneur complet (S et K) et l'enregistre dans module.json
import module as Mo, fourmis as F, json, sys, time
t0=time.time()
M={}
for r,(lane,At) in (('S',(-200,0)),('K',(-120,600))):
    b=Mo.approche(lane,At,(1,3))
    M[r]={'seed':[b[1][0],b[1][1]],'nodes':[{'cell':b[2],'cond':{},'br':[]}]}
def ok(x,msg):
    if not x: print("ECHEC",msg); json.dump(M,open('module_partiel.json','w')); sys.exit(1)
    print(msg,"case",x[0],"->",F.FL[x[1][1]],x[1][2],"chaos",x[2],flush=True)
# croisement : vérifier que c=1 donne ↘ décalé pour S et K
for r in 'SK':
    h0,_=Mo.sim(M,(0,0,0),r); h1,_=Mo.sim(M,(1,0,0),r)
    print(r,"c=0",F.FL[h0[1]],h0[2],"c=1",F.FL[h1[1]],h1[2])
# S : P (c=1 -> ↙), puis a, puis b ; bascule ↘<->↙
ok(Mo.place_noeud(M,'S',(1,),{},0),"S P")
for c in (0,1):
    ok(Mo.place_noeud(M,'S',(c,),{'a':1},3 if c==1 else 0),f"S a|c={c}")
for c in (0,1):
    for a in (0,1):
        cur=(c+a)%2   # 0 -> ↘, 1 -> ↙
        ok(Mo.place_noeud(M,'S',(c,a),{'b':1},3 if cur else 0),f"S b|c={c},a={a}")
# K : a (↘->↗) sur c=0 et c=1 ; b sur (1,0) (b=1 : ↘->↗) et (0,1) (b=0 : ↗->↘)
for c in (0,1):
    ok(Mo.place_noeud(M,'K',(c,),{'a':1},2),f"K a|c={c}")
ok(Mo.place_noeud(M,'K',(1,0),{'b':1},2),"K b|c=1,a=0")
ok(Mo.place_noeud(M,'K',(0,1),{'b':0},3),"K b|c=0,a=1 (case si b=0)")
json.dump(M,open('module.json','w'))
print("temps %.0f s"%(time.time()-t0))
