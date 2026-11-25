#!/usr/bin/env python3
"""toggle.py dS1.json : 2e tir (autoroute neuve) sur un état S1 ; le résidu S2 est-il l'orbite S0 d'origine ? (bascule idéalisée)"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bascule import orbite
C2=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cycles2.json')))
S1=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cyclesS1.json')))
def key_of(sit,p):
    r,a,cc=sit.split('|')
    A=[tuple(int(v) if v.lstrip('-').isdigit() else 'HDBG'.index(v) for v in x.split(',')) for x in a.split(';')]
    cells=[tuple(map(int,x.split(','))) for x in cc.split(';') if x]
    return orbite(A,cells,p)
k0={}
n=0; hits=[]
for l in open(sys.argv[1]):
    d=json.loads(l)
    if d['classe'] not in ('CHANGÉE',) or d.get('p1',10**9)>104: continue
    e=S1[d['id'][0]]; k2=key_of(d['S1'],d['p1'])
    for dep in e['depuis']:
        ic=dep[0]
        if ic not in k0: k0[ic]=key_of(C2[ic]['situation'],C2[ic]['periode'])
        if k0[ic]==k2: hits.append({'S0':dep,'S1':d['id'][0],'tir2':d['id']+d['sortie']}); break
    n+=1
print(n,'résidus S2 changés testés ;',len(hits),'retours à S0')
json.dump(hits,open('/tmp/claude-0/toggle_hits.json','w'))
for h in hits[:20]: print(h)
