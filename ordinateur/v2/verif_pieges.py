# 2e moteur : après 200 000 pas, les fourmis piégées + leur boîte reviennent-elles exactement après « période » pas ?
import sys; sys.path.insert(0,'..')
import sim, pieges as Pg, json
v=[x for x in json.load(open('pieges_vrais.json')) if x['type']=='capture']
v=sorted(v,key=lambda x:x['periode'])[:8]+[x for x in v if x['cycle']=='Petit Grain 8' and x['rot']==0 and x['p']==-1 and x['s']==3]
res=[]
for x in v:
    r,ants,g=sim.parse(x['germe']); q=2; K=[1,3]
    def go(n):
        for _ in range(n):
            for a in ants:
                k=(a[0],a[1]); c=g.get(k,0); a[2]=(a[2]+K[c])&3; g[k]=(c+1)%q; a[0]+=sim.DX[a[2]]; a[1]+=sim.DY[a[2]]
    go(200000); st=x['o'].split(); B=[i for i,t in enumerate([t for t in st if t in('B','X') or t.startswith('A')]) if t=='B']
    xs=[ants[i][0] for i in B]; ys=[ants[i][1] for i in B]
    box=(min(xs)-200,max(xs)+200,min(ys)-200,max(ys)+200)
    snap=lambda:( [tuple(ants[i]) for i in B], {k:v for k,v in g.items() if v and box[0]<=k[0]<=box[1] and box[2]<=k[1]<=box[3]} )
    s0=snap(); go(x['periode']); s1=snap()
    ok=s0==s1; res.append(ok)
    print(x['cycle'],'r',x['rot'],'p',x['p'],'s',x['s'],'période',x['periode'],'->','RETOUR EXACT' if ok else 'PAS DE RETOUR')
print(sum(res),'/',len(res))
