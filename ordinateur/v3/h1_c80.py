import compilateur as C, pas_llr as PL, time, json
C.BIN='trapL32'; C.PAR.update(POFF=300,SP=80,DA=300,OY=0)
nom,f=PL.S[6]; plan=C.compile_([(nom,f)],8,PL.NOMS)
t=time.time(); ok,N,T,res=C.verifie(plan,[(nom,f)],'C')
bad=[m for m,r in enumerate(res) if r[nom]!=int(bool(f(m)))]
print("h1' très larges (SP=80), C grille 32768 :",ok,'/',N,f'{time.time()-t:.0f} s ; T={T} ; faux {bad[:20]}')
json.dump(dict(ok=ok,bad=bad,T=T),open('h1_c80.json','w'))
