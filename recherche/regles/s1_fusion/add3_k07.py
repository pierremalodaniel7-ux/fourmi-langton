#!/usr/bin/env python3
"""S1 / R-410 Les 66 fusions V0/V7 à 1 constant (R-408, fus07.json) posées dans le VRAI circuit (étages 0 + 1 de R-405), à chaque rang
de jeu : 16 cas propres ? les cas c1 = V0 et c1 = V7 ont-ils une sortie commune absente des cas c1 = 0 ? (l'« ombre » est tolérée ici :
on regarde d'abord si les sorties s1, voisines à 1 voie, survivent). Écrit s1_fusion/add3_k07.json.
Usage : python3 s1_fusion/add3_k07.py T3"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from add2_perm import build
from circuit import Circuit
from fa_lib import decode, lotdump, back
T3 = int(sys.argv[1])
ST1 = build('A', 0, 20)
F = json.load(open(os.path.join(HERE, 'fus07.json')))
def route(e):
    c0 = e['a0'] & e['b0']
    if c0 and e['b1']: return 'V2'
    if c0 and e['a1']: return 'V0'
    if e['a1'] and e['b1']: return 'V7'
    return '-'
seen = set(); jobs = []
for fi, f in enumerate(F):
    key = (tuple(f['K'][0]), tuple(map(tuple, f['K'][1])))
    if key in seen: continue
    seen.add(key)
    Kp = back((tuple(f['K'][0]), [tuple(c) for c in f['K'][1]]), 1095)   # temps 0 du circuit = 9 000 − 240 − 8 760
    for rank in range(len(ST1.pieces) + 1):
        jobs.append((fi, rank, Circuit(ST1.pieces[:rank] + [('K7', Kp, None)] + ST1.pieces[rank:])))
cs = ST1.cases()
R = lotdump([C.sit(e) for _, _, C in jobs for e in cs], T3)
res = []; best = []
for j, (fi, rank, C) in enumerate(jobs):
    out = {}
    for i, e in enumerate(cs):
        d = decode(*R[j * 16 + i]); out[''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1'))] = (route(e), None if d is None else [tuple(x) for x in d])
    sale = [k for k, v in out.items() if v[1] is None]
    byr = collections.defaultdict(list)
    for k, (rt, d) in out.items():
        if d is not None: byr[rt].append(set(d))
    zero = set.union(*byr['-']) if byr['-'] else set()
    com = (set.intersection(*(byr['V0'] + byr['V7'])) - zero) if byr['V0'] and byr['V7'] else set()
    res.append(dict(f=fi, rank=rank, sales=sale, commun07=sorted(com), out=out))
    best.append((len(sale), fi, rank, len(com)))
json.dump(res, open(os.path.join(HERE, 'add3_k07.json'), 'w'))
best.sort(); print(len(jobs), 'montages ; meilleurs (cas sales, fusion, rang, sorties communes V0/V7) :', best[:12])
print('répartition des cas sales :', sorted(collections.Counter(b[0] for b in best).items()))
