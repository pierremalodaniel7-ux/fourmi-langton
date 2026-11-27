#!/usr/bin/env python3
"""S1 / R-411 étape B'+C' : pour chaque K1 de k1full.json, fusion du catalogue posée EXACTEMENT sur une paire (p0 ∈ nouveaux du cas V0,
p7 ∈ nouveaux du cas V7) (matchlib), puis K2 inséré à tous les rangs dans le vrai circuit (+ K1) : 16 cas propres, sortie commune aux cas
V0/V7 absente des autres, V2 intact. Écrit s1_fusion/k2full.json. Usage : python3 s1_fusion/k2full.py T3"""
import sys, os, json, collections, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from add2_perm import build
from circuit import Circuit
from fa_lib import decode, lotdump
from matchlib import matches
T3 = int(sys.argv[1]); ST1 = build('A', 0, 20); R1 = json.load(open(os.path.join(HERE, 'k1full.json')))
P = lambda p: (tuple(p[0]), [tuple(c) for c in p[1]])
def route(e):
    c0 = e['a0'] & e['b0']
    if c0 and e['b1']: return 'V2'
    if c0 and e['a1']: return 'V0'
    if e['a1'] and e['b1']: return 'V7'
    return '-'
key = lambda e: ''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1'))
cs = ST1.cases(); jobs = []; nm = 0
for i, r in enumerate(R1):
    K1 = P(r['K']); L1 = list(ST1.pieces[:r['rank']]) + [('K1', K1, None)] + list(ST1.pieces[r['rank']:])
    for p, q in itertools.product(r['new0'], r['new7']):
        for X, Y in ((p, q), (q, p)):
            for m in matches(tuple(X), tuple(Y), 9600):
                nm += 1; K2 = P(m['K'])
                for r2 in range(len(L1) + 1): jobs.append((i, X, Y, m['z'], r2, Circuit(L1[:r2] + [('K2', K2, None)] + L1[r2:])))
print(nm, 'appariements ;', len(jobs), 'montages', flush=True)
t0 = time.time(); RR = lotdump([C.sit(e) for *_, C in jobs for e in cs], T3); st = collections.Counter(); res = []
for j, (i, X, Y, z, r2, C) in enumerate(jobs):
    d = {}
    for n, e in enumerate(cs):
        x = decode(*RR[j * 16 + n]); d[key(e)] = (route(e), None if x is None else set(map(tuple, x)))
    nb = sum(v[1] is None for v in d.values())
    if nb: st['sale'] += 1; st[('nb sales', nb)] += 1; continue
    by = collections.defaultdict(list)
    for k, (rt, s) in d.items(): by[rt].append(s)
    com = set.intersection(*(by['V0'] + by['V7'])) - set.union(*(by['-'] + by['V2']))
    if not com: st['pas de sortie commune'] += 1; continue
    v2 = all((2, -30, 2168 + 2 * ((T3 - 9000) // 8), 1) in s for s in by['V2'])
    st['OK' + (' V2 intact' if v2 else ' V2 touché')] += 1
    res.append(dict(k1=i, X=X, Y=Y, z=z, r2=r2, O=sorted(com), v2=v2, pieces=[(n_, p_, v_) for n_, p_, v_ in C.pieces],
                    out={k: sorted(s) for k, (rt, s) in d.items()}))
json.dump(res, open(os.path.join(HERE, 'k2full.json'), 'w'))
print(dict(st), round(time.time() - t0), 's')
