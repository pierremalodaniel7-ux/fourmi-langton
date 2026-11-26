#!/usr/bin/env python3
"""bilan.py FAM : résumé des data/rlem/FAM_*.jsonl : pièces, écritures, effacements (retours S1→S0), lectures (fortes/faibles,
hors simples décalages de voie ≤ 4), candidats RLEM (écriture + effacement + lecture sur le même S1)."""
import sys, json, glob, collections
F=sys.argv[1]; R=[json.loads(l) for f in sorted(glob.glob(f'/home/claude/fourmi-langton/data/rlem/{F}_[0-9]*.jsonl')) for l in open(f)]
c=collections.Counter(); cand=[]
for r in R:
    c['pièces']+=1; c['tirs']+=r['tirs1']+sum(s['tirs2'] for s in r['S1'])
    if r['nS1']: c['avec écriture']+=1
    if any(s['n_retours'] for s in r['S1']): c['avec effacement']+=1
    if any(s['lectures'] for s in r['S1']): c['avec lecture']+=1
    for s in r['S1']:
        if s['lectures']: c['lectures fortes']+=sum(x['forte'] for x in s['lectures']); c['lectures']+=len(s['lectures'])
        if s['lectures'] and s['n_retours']: cand.append((r['nom'],s['situation'],s['periode'],len(s['lectures']),s['n_retours']))
print(F,dict(c)); print('candidats RLEM (écriture + effacement + lecture) :',len(cand))
for x in cand[:20]: print('  ',x)
