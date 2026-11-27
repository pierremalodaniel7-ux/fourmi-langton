#!/usr/bin/env python3
"""S1 / R-411 étape A : un constant K1 qui frappe V0 ou V7 (les deux routes de c1 à UN pas d'écart) DE CÔTÉ (direction ≠ 3, pas de face) :
V0 + K1 et V7 + K1 propres, sorties sans vaisseau commun (s0, s7), K1 seul sans rien. Même cadre que fus07
(V0 = (0,19,2187,0) au temps 9 000 du circuit ; disque de rayon R ; 8 phases ; 2 ordres). Sorties au temps 9 600 du circuit.
Écrit s1_fusion/k1side.json. Usage : python3 s1_fusion/k1side.py R"""
import sys, os, json, time, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from fa_lib import kship, decode, back, sit, lotdump
from hx import rot
from exp_osc import hd
R = int(sys.argv[1]); NB = 30; TT = NB * 8 + 600
def mk(r, L, A, ph): return kship(r, rot(((L + A) // 2, (L - A) // 2), r), ph)
V0 = mk(0, 19, 2187, 0); V7 = mk(0, 19, 2187, 7); g0 = rot(((19 + 2187) // 2, (19 - 2187) // 2), 0)
V0b, V7b = back(V0, NB), back(V7, NB)
cfg = []; lines = []
for rK in (1, 2, 4, 5):
    for ox in range(-R, R + 1):
        for oy in range(-R, R + 1):
            if hd(ox, oy) > R: continue
            for tau in range(8):
                K = back(kship(rK, (g0[0] + ox, g0[1] + oy), tau), NB)
                cfg.append((rK, ox, oy, tau, K))
                for order in (0, 1):
                    for V in (V0b, V7b): lines.append(sit([V, K] if order == 0 else [K, V]))
                lines.append(sit([K]))
fr = lotdump([sit([V0b]), sit([V7b])], TT); f0, f7 = set(map(tuple, decode(*fr[0]))), set(map(tuple, decode(*fr[1])))
t0 = time.time(); out = lotdump(lines, TT); print(len(lines), 'simulations', round(time.time() - t0), 's', flush=True)
res = []; st = collections.Counter()
for c, (rK, ox, oy, tau, K) in enumerate(cfg):
    blk = out[5 * c:5 * c + 5]; dN = decode(*blk[4])
    for order in (0, 1):
        d0, d7 = decode(*blk[2 * order]), decode(*blk[2 * order + 1])
        if d0 is None or d7 is None: st['sale'] += 1; continue
        s0, s7 = set(map(tuple, d0)), set(map(tuple, d7))
        sN = set(map(tuple, dN))
        if s0 == sN | f0 or s7 == sN | f7: st['pas de choc (un des deux cas)'] += 1; continue
        a, b = s0 - s7, s7 - s0
        st[('tailles', len(s0), len(s7), len(s0 & s7))] += 1
        if s0 & s7: continue
        st['OK'] += 1
        res.append(dict(rK=rK, o=(ox, oy), tau=tau, order=order, s0=sorted(s0), s7=sorted(s7), seul=dN, K=K))
json.dump(res, open(os.path.join(HERE, 'k1side.json'), 'w'))
print(dict(st))
