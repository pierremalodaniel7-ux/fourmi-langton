#!/usr/bin/env python3
"""fonctionnel.py FAM : pour chaque candidat de rlem.py (S1 avec lecture ou effacement), tests fonctionnels (fils idéalisés,
voir funcseq.py) : 'bbb' (3 lectures de S0), 'abbb' (écriture puis 3 lectures de S1), 'acacac' (3 écritures/effacements),
'babcb' (lecture, écriture, lecture, effacement, lecture). Une suite réussit si chaque opération donne l'état attendu et
(pour b) la même sortie que la 1re fois dans le même état. → data/rlem/FAM_fonctionnel.json"""
import sys, json, glob
from funcseq import run
FAM=sys.argv[1]
R=[json.loads(l) for f in sorted(glob.glob(f'../../data/rlem/{FAM}_[0-9]*.jsonl')) for l in open(f)]
attendu={'a':('S0','S1'),'c':('S1','S0'),'b':None}
def score(seq,out):
    sorties={}; n=0
    for o in out:
        if len(o)<5: break
        op,st,_,st2,d=o
        if op=='b':
            if st2!=st: break
            if st in sorties and sorties[st]!=d: break
            sorties.setdefault(st,d)
        elif (st,st2)!=attendu[op]: break
        n+=1
    return n
res=[]
for r in R:
    for i,s in enumerate(r['S1']):
        seqs=[]
        if s['lectures']: seqs+=['bbb','abbb']
        if s['n_retours']: seqs+=['acacac']
        if s['lectures'] and s['n_retours']: seqs+=['babcb']
        for q in seqs:
            try: out,_=run(FAM,r['nom'],i,q)
            except Exception as e: out=[('erreur',str(e))]
            n=score(q,out); res.append({'nom':r['nom'],'S1':i,'suite':q,'reussi':n,'detail':[list(map(str,o)) for o in out]})
            print(r['nom'],i,q,f'{n}/{len(q)}',' | '.join(' '.join(map(str,o[:5])) for o in out),flush=True)
json.dump(res,open(f'../../data/rlem/{FAM}_fonctionnel.json','w'))
import collections
c=collections.Counter((x['suite'],x['reussi']==len(x['suite'])) for x in res); print(dict(c))
