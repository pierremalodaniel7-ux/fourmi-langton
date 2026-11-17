import compilateur as C, pas_llr as PL, random, time, json, sys
sys.path.insert(0,'..'); import sim
C.PAR.update(POFF=200,SP=40,DA=200,OY=0)
plan=C.compile_(PL.S,8,PL.NOMS); T=C.T_of(plan)
random.seed(23); sample=random.sample(range(256),16); ok=0; t=time.time()
for m in sample:
    s,lect=C.germe(plan,m); _,_,_,pos=sim.run(s,T,trace=True); good=True
    for nom,f in PL.S:
        i,d,l=lect[nom]; dd=(pos[-1][i][0]-pos[-19][i][0],pos[-1][i][1]-pos[-19][i][1])
        v=min(((p[i][0]+p[i][1]) if d==(-1,1) else (p[i][0]-p[i][1])) for p in pos[-18:])
        good&= int(dd==d and abs(v-l)<=4)==int(bool(f(m)))
    ok+=good; print(m,'8 sorties justes' if good else 'FAUX',f'{time.time()-t:.0f} s',flush=True)
print('GERME UNIQUE (Python) :',ok,'/ 16 états tirés au hasard ; T =',T)
json.dump(dict(ok=ok,sample=sample,T=T),open('pas_unique_py_23.json','w'))
