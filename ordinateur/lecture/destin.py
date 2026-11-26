#!/usr/bin/env python3
"""destin.py chaine.json : pour chaque préfixe de la chaîne (2, 3, 4… impulsions sur la ligne a), simulation longue :
destin de chaque sonde (direction d'autoroute, voie, position finale), état final de la pièce, cases noires restantes
(près de la pièce / sur la ligne / ailleurs). 2 moteurs : src/fourmi (-dump) et moteur2.py (état final identique ?)."""
import sys, json
from lib import *
H=json.load(open(sys.argv[1])); h0=json.load(open(sys.argv[2]))[int(sys.argv[3])] if len(sys.argv)>3 else None
EXTRA=int(os.environ.get('EXTRA',40000)); PY=int(os.environ.get('PY',1))
for h in H:
    hb=dict(h0) if h0 else None
    b=Bascule({'hit':hb['hit'],'situation':h['situation'],'T':h['T']}) if hb else None
    T=h['T']+EXTRA; (o,an,ce),=lot([h['situation']],T,'de')
    ds=destins(o); m=h['impulsions']
    st=b.etat(an,ce) if b else '?'
    near=sum(1 for x,y in ce if -10<=x<=15 and -10<=y<=15)
    g1=tuple(map(int,h['situation'].split('|')[1].split(';')[m-1].split(',')[:2]))   # source de la 1re sonde
    line=sum(1 for x,y in ce if abs((x+y)-(g1[0]+g1[1]))<=30 and 15<x<g1[0]+20 and not(-10<=x<=15 and -10<=y<=15))
    print(f'{m} impulsions, T={T} : pièce {st} ; cases noires {len(ce)} (pièce ±12 : {near}, ligne : {line})')
    for k in range(m):
        a=an[k]; d=ds[k]; i=m-k
        print(f'   sonde {i} : fin ({a[0]},{a[1]}) cap {a[2]}  autoroute {d}'+(f' voie {voie(a[0],a[1],d)}' if d!='-' else ''))
    if PY:
        A2,N2=py_final(h['situation'],int(o.split('|')[5])); print('   moteur2 :','identique' if A2==an and N2==ce else 'DIFFÉRENT')
