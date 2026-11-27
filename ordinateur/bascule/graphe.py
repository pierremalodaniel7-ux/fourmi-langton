#!/usr/bin/env python3
"""graphe.py d2.json : graphe des transitions entre petits cycles à 2 fourmis (cycles2.json) provoquées par UNE autoroute 104
(voie/phase = id du tir, sortie = direction de la sonde). Cherche les allers-retours a → b → a (bascules idéalisées)."""
import sys, json, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bascule import orbite, situ_piece
from moteur2 import charge
C=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cycles2.json')))
key2i={}; i2k={}
for i,c in enumerate(C):
    r,a,cc=c['situation'].split('|')
    A=[tuple(int(v) if v.lstrip('-').isdigit() else 'HDBG'.index(v) for v in x.split(',')) for x in a.split(';')]
    cells=[tuple(map(int,x.split(','))) for x in cc.split(';') if x]
    k=orbite(A,cells,c['periode']); i2k[i]=k; key2i.setdefault(k,i)
E=collections.defaultdict(list)
for l in open(sys.argv[1]):
    d=json.loads(l)
    if d['classe'] not in ('CHANGÉE','même orbite') or 'p1' not in d or d['p1']>104: continue
    r,a,cc=d['S1'].split('|'); A=[tuple(map(int,x.split(','))) for x in a.split(';')]
    cells=[tuple(map(int,x.split(','))) for x in cc.split(';') if x]
    k=orbite(A,cells,d['p1'])
    if k in key2i: E[(key2i[i2k[d['id'][0]]],key2i[k])].append(d['id']+d['sortie'])
print('arêtes',len(E),'dont boucles a→a',sum(1 for a,b in E if a==b))
deux=[(a,b) for a,b in E if a<b and (b,a) in E]
print('allers-retours a↔b :',len(deux))
json.dump({'aretes':{f'{a}>{b}':v for (a,b),v in E.items()},'allers_retours':deux},open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'graphe2.json'),'w'))
for a,b in deux[:20]: print(a,b,C[a]['periode'],C[b]['periode'],E[(a,b)][:2],E[(b,a)][:2])
