# Le pas complet = 8 modules compilés séparément (un par bit de sortie), chacun vérifié sur les 256 états (moteur C).
import compilateur as C, pas_llr as PL, json, time
C.BIN='trapL32'; C.PAR.update(POFF=200,SP=40,DA=200)
R={}
for nom,f in PL.S:
    plan=C.compile_([(nom,f)],8,PL.NOMS); T=C.T_of(plan)
    ymin=min(g['ls']-g['a'] for g in plan['gates'])//2; ymax=max(g['rays'][-1]-g['a'] for g in plan['gates'])//2
    C.PAR['OY']=0
    t=time.time(); ok,N,T,res=C.verifie(plan,[(nom,f)],'C'); s,_=C.germe(plan,255)
    R[nom]=dict(ok=ok,N=N,T=T,portes1=len(plan['gates']),portes2=sum(1 for o in plan['outs'] if o['niv']==2),
                fourmis_max=max(C.germe(plan,m)[0].count(',')//2 for m in range(256)),OY=C.PAR['OY'],plan=plan)
    print(f"{nom:5s} : {ok}/{N} (moteur C, T={T}, {time.time()-t:.0f} s) ; portes {R[nom]['portes1']}+{R[nom]['portes2']} ; fourmis ≤ {R[nom]['fourmis_max']}",flush=True)
json.dump(R,open('pas_modules.json','w'),default=str)
print('TOTAL :',sum(r['ok'] for r in R.values()),'/',sum(r['N'] for r in R.values()))
