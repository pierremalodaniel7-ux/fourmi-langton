# Le pas complet en UN germe (8 sorties), moteur C grille 32768, 256 fourmis max.
import compilateur as C, pas_llr as PL, json, time
C.BIN='trapL32b'; C.PAR.update(POFF=200,SP=40,DA=200,OY=0)
plan=C.compile_(PL.S,8,PL.NOMS); T=C.T_of(plan)
print('portes',len(plan['gates']),'+',sum(1 for o in plan['outs'] if o['niv']==2),'; fourmis max',max(C.germe(plan,m)[0].count(',')//2 for m in range(256)),'; T',T,flush=True)
t=time.time(); ok,N,T,res=C.verifie(plan,PL.S,'C')
par={n:sum(r[n]==int(bool(f(m))) for m,r in enumerate(res)) for n,f in PL.S}
print('GERME UNIQUE du pas :',ok,'/',N,f'({time.time()-t:.0f} s) ; par sortie',par)
json.dump(dict(ok=ok,par=par,T=T),open('pas_unique.json','w'))
