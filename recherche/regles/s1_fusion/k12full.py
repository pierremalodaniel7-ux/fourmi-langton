#!/usr/bin/env python3
"""S1 / R-411 étape D : les fusions V0/V7 à 2 constants de côté (k12iso.json) posées dans le VRAI circuit (étages 0 + 1 de R-405) :
K1 et K2 insérés à tous les rangs de jeu ; 16 cas propres ? sortie commune aux cas V0 et V7, absente des autres cas ? V2 intact ?
Écrit s1_fusion/k12full.json. Usage : python3 s1_fusion/k12full.py T3 [début fin]"""
import sys, os, json, collections, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from add2_perm import build
from circuit import Circuit
from fa_lib import decode, lotdump, back
T3 = int(sys.argv[1]); ST1 = build('A', 0, 20)
I = json.load(open(os.path.join(HERE, 'k12iso.json'))); M = json.load(open(os.path.join(HERE, 'k1match.json')))
R1 = json.load(open(os.path.join(HERE, 'k1side.json')))
b0, b1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, len(I))
P = lambda p: (tuple(p[0]), [tuple(c) for c in p[1]])
def route(e):
    c0 = e['a0'] & e['b0']
    if c0 and e['b1']: return 'V2'
    if c0 and e['a1']: return 'V0'
    if e['a1'] and e['b1']: return 'V7'
    return '-'
cs = ST1.cases(); n0 = len(ST1.pieces)
jobs = []
for ii in range(b0, min(b1, len(I))):
    m = M[I[ii]['m']]; K1 = back(P(R1[m['i']]['K']), 1095); K2 = P(m['K'])
    for r1 in range(n0 + 1):
        for r2 in range(n0 + 2):
            L = list(ST1.pieces[:r1]) + [('K1', K1, None)] + list(ST1.pieces[r1:])
            L = L[:r2] + [('K2', K2, None)] + L[r2:]
            jobs.append((ii, r1, r2, Circuit(L)))
t0 = time.time(); R = lotdump([C.sit(e) for _, _, _, C in jobs for e in cs], T3)
res = []; st = collections.Counter()
for j, (ii, r1, r2, C) in enumerate(jobs):
    d = {}; bad = 0
    for i, e in enumerate(cs):
        x = decode(*R[j * 16 + i])
        if x is None: bad += 1
        else: d[''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1'))] = (route(e), set(map(tuple, x)))
    if bad:
        st['sale'] += 1; st[('nb sales', bad)] += 1
        for i, e in enumerate(cs):
            if decode(*R[j * 16 + i]) is None: st['sale ' + ''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1'))] += 1
        continue
    by = collections.defaultdict(list)
    for k, (rt, s) in d.items(): by[rt].append(s)
    rest = set.union(*(by['-'] + by['V2']))
    com = set.intersection(*(by['V0'] + by['V7'])) - rest
    if not com: st['pas de sortie commune'] += 1; continue
    v2 = all((2, -30, 2168 + 2 * ((T3 - 9000) // 8), 1) in s for s in by['V2'])
    st['OK' + (' V2 intact' if v2 else ' V2 touché')] += 1
    res.append(dict(iso=ii, r1=r1, r2=r2, O=sorted(com), v2=v2, out={k: sorted(s) for k, (rt, s) in d.items()}))
json.dump(res, open(os.path.join(HERE, 'k12full_%d_%d.json' % (b0, b1)), 'w'))
print(len(jobs), 'montages', dict(st), round(time.time() - t0), 's')
