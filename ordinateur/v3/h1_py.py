import compilateur as C, pas_llr as PL, random, json, time, sys
C.PAR.update(POFF=200,SP=40,DA=200,OY=0)
nom,f=PL.S[6]; plan=C.compile_([(nom,f)],8,PL.NOMS)
random.seed(1); sample=sorted(random.sample(range(256),64))
import sim
T=C.T_of(plan); ok=0; t=time.time(); bad=[]
for m in sample:
    s,lect=C.germe(plan,m); _,_,_,pos=sim.run(s,T,trace=True); i,d,l=lect[nom]
    dd=(pos[-1][i][0]-pos[-19][i][0],pos[-1][i][1]-pos[-19][i][1]); v=min(p[i][0]+p[i][1] for p in pos[-18:])
    r=int(dd==d and abs(v-l)<=4); ok+= r==int(bool(f(m)))
    if r!=int(bool(f(m))): bad.append(m)
    print(m,r,int(bool(f(m))),flush=True)
print('h1\' (paramètres larges, Python) :',ok,'/ 64',f'({time.time()-t:.0f} s) ; T={T} ; faux',bad)
json.dump(dict(ok=ok,bad=bad,T=T),open('h1_py.json','w'))
