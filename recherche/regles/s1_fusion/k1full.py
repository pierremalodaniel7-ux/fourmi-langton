#!/usr/bin/env python3
"""S1 / R-411 étape A' : K1 de côté cherché DIRECTEMENT dans le vrai circuit (étages 0 + 1 de R-405) : K1 de direction 1, 2, 4, 5, point de
référence dans un disque de rayon R autour de V0 au temps 9 000, 8 phases, 9 rangs de jeu. Cas témoins : 1110 (c1 = V0), 0011 (V7),
0000, 0010 (s1 voisin), 1101 (V2), 1111. On garde : 6 cas propres ; K1 transparent (sorties = étages seuls + K1 libre) dans 0000, 0010,
1101, 1111 ; V0 et V7 touchés. Écrit s1_fusion/k1full.json. Usage : python3 s1_fusion/k1full.py R T3"""
import sys, os, json, collections, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from add2_perm import build
from circuit import Circuit
from fa_lib import decode, lotdump, back, kship, sit
from hx import rot
from exp_osc import hd
R, T3 = int(sys.argv[1]), int(sys.argv[2]); ST1 = build('A', 0, 20)
g0 = rot(((19 + 2187) // 2, (19 - 2187) // 2), 0)
W = {'1110': 'V0', '0011': 'V7', '0000': '-', '0010': '-', '1101': 'V2', '1111': 'V2'}
cs = [e for e in ST1.cases() if ''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1')) in W]
key = lambda e: ''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1'))
base = {key(e): set(map(tuple, decode(*r))) for e, r in zip(cs, lotdump([ST1.sit(e) for e in cs], T3))}
Ks = []
for rK in (1, 2, 4, 5):
    for ox in range(-R, R + 1):
        for oy in range(-R, R + 1):
            if hd(ox, oy) > R: continue
            for tau in range(8): Ks.append((rK, ox, oy, tau, back(kship(rK, (g0[0] + ox, g0[1] + oy), tau), 1125)))
free = [set(map(tuple, decode(*r))) for r in lotdump([sit([k[4]]) for k in Ks], T3)]
n0 = len(ST1.pieces); jobs = [(ki, rk) for ki in range(len(Ks)) for rk in range(n0 + 1)]
lines = []
for ki, rk in jobs:
    C = Circuit(ST1.pieces[:rk] + [('K1', Ks[ki][4], None)] + ST1.pieces[rk:]); lines += [C.sit(e) for e in cs]
t0 = time.time(); RR = lotdump(lines, T3); st = collections.Counter(); res = []
for j, (ki, rk) in enumerate(jobs):
    d = {key(e): decode(*RR[j * len(cs) + i]) for i, e in enumerate(cs)}
    if any(v is None for v in d.values()): st['sale'] += 1; continue
    d = {k: set(map(tuple, v)) for k, v in d.items()}
    if any(d[k] != base[k] | free[ki] for k in W if W[k] in '-V2'): st['K1 pas transparent hors V0/V7'] += 1; continue
    if d['1110'] == base['1110'] | free[ki] or d['0011'] == base['0011'] | free[ki]: st['V0 ou V7 pas touché'] += 1; continue
    n0_, n7_ = d['1110'] - base['1110'] - free[ki], d['0011'] - base['0011'] - free[ki]
    st['OK'] += 1
    res.append(dict(K=Ks[ki][4], k=Ks[ki][:4], rank=rk, new0=sorted(n0_), new7=sorted(n7_), lost0=sorted((base['1110'] | free[ki]) - d['1110']),
                    lost7=sorted((base['0011'] | free[ki]) - d['0011'])))
json.dump(res, open(os.path.join(HERE, 'k1full.json'), 'w'))
print(len(jobs), 'montages', dict(st), round(time.time() - t0), 's')
print(collections.Counter((len(r['new0']), len(r['new7']), len(set(map(tuple, r['new0'])) & set(map(tuple, r['new7'])))) for r in res).most_common(8))
