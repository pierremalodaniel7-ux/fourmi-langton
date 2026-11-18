# R-69 : le germe UNIQUE du pas complet (R-67/R-68) sur les 256 états avec le moteur creux (C, table de hachage).
# Usage : python3 pas256_creux.py [plan|run k K]  (tranche k sur K)
import sys, os, json, subprocess, time
sys.path.insert(0,'../v3'); sys.path.insert(0,'..')
import compilateur as C, pas_llr as PL
C.PAR.update(POFF=200,SP=40,DA=200,OY=0)
plan=C.compile_(PL.S,8,PL.NOMS); T=C.T_of(plan)
def lit(o,lect):
    t=o.split()[2:]; r={}
    for nom,(i,d,l) in lect.items():
        dx,dy,ms,md=map(int,t[i].split(','))
        v= ms if d==(-1,1) else md
        r[nom]=int((dx,dy)==d and abs(v-l)<=4)
    return r
if __name__=="__main__":
    k,K=int(sys.argv[1]),int(sys.argv[2]); res={}
    for m in range(k,256,K):
        s,lect=C.germe(plan,m); t0=time.time()
        o=subprocess.run(['./creux'],input=f'{s} {T}\n',capture_output=True,text=True).stdout.strip()
        r=lit(o,lect); good=all(r[n]==int(bool(f(m))) for n,f in PL.S)
        res[m]=dict(ok=good,r=r,n=s.count(',')//2,cases=o.split()[0],t=round(time.time()-t0,1))
        print(m,'OK' if good else 'FAUX',res[m]['n'],res[m]['cases'],res[m]['t'],'s',flush=True)
    json.dump(dict(T=T,res=res),open(f'pas256_{k}.json','w'))
