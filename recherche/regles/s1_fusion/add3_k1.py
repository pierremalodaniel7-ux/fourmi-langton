#!/usr/bin/env python3
"""S1 / R-409 suite : étage 1 + 2 (R-405) + le constant K d'un appariement exact (match3.json), inséré à chaque rang de jeu.
16 cas (a0 b0 a1 b1) : propres ? vaisseaux de sortie par cas ; sortie commune aux cas c1 = 1 ? Écrit s1_fusion/add3_k1.json.
Usage : python3 s1_fusion/add3_k1.py T3"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from add2_perm import build
from circuit import Circuit
from fa_lib import decode, lotdump
T3 = int(sys.argv[1])
ST1 = build('A', 0, 20)
M = json.load(open(os.path.join(HERE, 'match3.json')))
def c1of(e):
    c0 = e['a0'] & e['b0']; return int(c0 + e['a1'] + e['b1'] >= 2)
def route(e):
    c0 = e['a0'] & e['b0']
    if c0 and e['b1']: return 'V2'
    if c0 and e['a1']: return 'V0'
    if e['a1'] and e['b1']: return 'V7'
    return '-'
res = []
for mi, m in enumerate(M):
    Kp = (tuple(m['K'][0]), [tuple(c) for c in m['K'][1]])
    for rank in range(len(ST1.pieces) + 1):
        C = Circuit(ST1.pieces[:rank] + [('Kf', Kp, None)] + ST1.pieces[rank:])
        cs = C.cases(); R = lotdump([C.sit(e) for e in cs], T3)
        out = {}
        for e, r in zip(cs, R):
            d = decode(*r); key = ''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1'))
            out[key] = (route(e), None if d is None else [tuple(x) for x in d])
        sale = [k for k, v in out.items() if v[1] is None]
        byr = collections.defaultdict(list)
        for k, (rt, d) in out.items():
            if d is not None: byr[rt].append(set(d))
        com = {}
        for rt in ('V0', 'V7', 'V2'):
            if byr[rt]: com[rt] = set.intersection(*byr[rt]) - (set.union(*byr['-']) if byr['-'] else set())
        allc = set.intersection(*com.values()) if len(com) == 3 else set()
        line = dict(m=mi, rank=rank, sales=sale, communs={k: sorted(v) for k, v in com.items()}, commun3=sorted(allc), out=out)
        print(mi, rank, 'sales', len(sale), {k: len(v) for k, v in com.items()}, 'commun aux 3 :', sorted(allc), flush=True)
        res.append(line)
json.dump(res, open(os.path.join(HERE, 'add3_k1.json'), 'w'))
