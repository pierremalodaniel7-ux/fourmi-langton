#!/usr/bin/env python3
"""destin2.py chaine.json honnetes.json i : pour chaque préfixe (m impulsions sur la ligne a) : destin de chaque sonde =
direction de son autoroute finale ET point de départ de cette autoroute (près de la pièce, ou près de la source de la sonde k),
temps de départ ; RETOUR exact (une sonde en R(départ d'une autre)) ; état final de la pièce ; cases noires sur la ligne.
src/fourmi pour les destins (début d'autoroute), moteur2.py pour les positions et la comparaison de l'état final."""
import sys, json
from lib import *
H=json.load(open(sys.argv[1])); hb=json.load(open(sys.argv[2]))[int(sys.argv[3])]; EX=int(os.environ.get('EXTRA',40000))
for h in H:
    m=h['impulsions']; T=h['T']+EX
    (o,an,ce),=lot([h['situation']],T,'d2'); Tf=int(o.split('|')[5]); det=o.split('|')[-1].split(' boite')[0].split()
    b=Bascule({'hit':hb['hit'],'situation':h['situation'],'T':h['T']})
    r,A,C=parse(h['situation']); src=[(a[0],a[1]) for a in A[:m]]          # sources : fourmi 0 = dernière impulsion
    R0={(x-[0,1,0,-1][d],y-[-1,0,1,0][d],(d+2)%4):k for k,(x,y,d) in enumerate(A[:m])}   # R(départ) de chaque sonde
    debs={k:int(t.split(',')[3]) for k,t in enumerate(det[:m]) if t!='-'}
    turn,ants,noir=charge(h['situation']); pos={}; ret=[]
    for t in range(Tf+1):
        for k in range(m):
            if debs.get(k)==t: pos[k]=(ants[k][0],ants[k][1])
            st=tuple(ants[k])
            if st in R0 and R0[st]!=k and not any(x[0]==k for x in ret): ret.append((k,R0[st],t))
        if t<Tf: pas(turn,ants,noir,range(len(ants)))
    same=[tuple(a) for a in ants]==an and noir==ce
    print(f'== {m} impulsions (fin {Tf}) : pièce {b.etat(an,ce)} ; moteur2 {"identique" if same else "DIFFÉRENT"} ; cases noires {len(ce)}')
    for k,k2,t in ret: print(f'   RETOUR : sonde {m-k} est en R(départ de la sonde {m-k2}) au pas {t}')
    for k in range(m):
        i=m-k; d=destins(o)[k]
        if d=='-': print(f'   sonde {i} : pas d\'autoroute (fin {an[k][:2]})'); continue
        p=pos.get(k); dist=lambda q:max(abs(p[0]-q[0]),abs(p[1]-q[1]))
        lieu='pièce' if dist((2,2))<40 else min(((dist(s),f'source {m-j}') for j,s in enumerate(src)))[1]
        print(f'   sonde {i} : autoroute {d} partie de {p} ({lieu}) au pas {debs[k]}')
