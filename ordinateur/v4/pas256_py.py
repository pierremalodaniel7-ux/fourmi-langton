# R-69 contre-vérification : moteur Python léger (dict, ne garde que les 19 dernières positions), écrit indépendamment de creux.c.
import sys, json, time
sys.path.insert(0,'../v3'); sys.path.insert(0,'..')
import compilateur as C, pas_llr as PL
C.PAR.update(POFF=200,SP=40,DA=200,OY=0)
plan=C.compile_(PL.S,8,PL.NOMS); T=C.T_of(plan)
DX=(0,1,0,-1); DY=(-1,0,1,0)
def run(s,T):
    r,a,_=s.split('|'); K=[1 if ch=='R' else 3 for ch in r]; q=len(r)
    A=[[int(x),int(y),'HDBG'.index(c)] for x,y,c in (t.split(',') for t in a.split(';') if t)]
    g={}; hist=[]
    for t in range(T):
        for a_ in A:
            k=(a_[0],a_[1]); c=g.get(k,0); d=(a_[2]+K[c])&3; a_[2]=d; g[k]=(c+1)%q; a_[0]+=DX[d]; a_[1]+=DY[d]
        if t>=T-19: hist.append([(a_[0],a_[1]) for a_ in A])
    return hist
if __name__=="__main__":
    k,K=int(sys.argv[1]),int(sys.argv[2]); res={}
    for m in range(k,256,K):
        s,lect=C.germe(plan,m); t0=time.time(); h=run(s,T); good=True
        for nom,f in PL.S:
            i,d,l=lect[nom]; dd=(h[-1][i][0]-h[0][i][0],h[-1][i][1]-h[0][i][1])
            v=min((p[i][0]+p[i][1]) if d==(-1,1) else (p[i][0]-p[i][1]) for p in h[1:])
            good&= int(dd==d and abs(v-l)<=4)==int(bool(f(m)))
        res[m]=good; print(m,'OK' if good else 'FAUX',round(time.time()-t0),'s',flush=True)
        json.dump(dict(T=T,res=res),open(f'pas256_py_{k}.json','w'))
