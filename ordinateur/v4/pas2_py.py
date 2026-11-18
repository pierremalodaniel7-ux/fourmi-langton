# R-70 contre-vérification Python (moteur léger de pas256_py.py) du germe « deux pas »
import sys, json, time
sys.argv=[sys.argv[0]]+sys.argv[1:]
k,K=int(sys.argv[1]),int(sys.argv[2])
src=open('pas2_creux.py').read().split("lines=[];L=[]")[0]
ns={'__name__':'x'}; exec(src,ns)
from pas256_py import run
C,plan,T,S2=ns['C'],ns['plan'],ns['T'],ns['S2']; res={}
for m in range(k,256,K):
    s,lect=C.germe(plan,m); t0=time.time(); h=run(s,T); good=True
    for nom,f in S2:
        i,d,l=lect[nom]; dd=(h[-1][i][0]-h[0][i][0],h[-1][i][1]-h[0][i][1])
        v=min((p[i][0]+p[i][1]) if d==(-1,1) else (p[i][0]-p[i][1]) for p in h[1:])
        good&= int(dd==d and abs(v-l)<=4)==int(bool(f(m)))
    res[m]=good; print(m,'OK' if good else 'FAUX',round(time.time()-t0),'s',flush=True)
    json.dump(dict(T=T,res=res),open(f'pas2_py_{k}.json','w'))
