import compilateur as C, pas_llr as PL, time
C.PAR.update(POFF=200,SP=40,DA=200,OY=0); tot=0; N=0
for k,(nom,f) in enumerate(PL.S):
    if nom=="h1'": continue
    plan=C.compile_([(nom,f)],8,PL.NOMS); t=time.time(); ok,n,T,_=C.verifie(plan,[(nom,f)],'Py'); tot+=ok; N+=n
    print(f'{nom} : {ok}/{n} (moteur Python, {time.time()-t:.0f} s)',flush=True)
print('TOTAL Python 7 modules :',tot,'/',N)
