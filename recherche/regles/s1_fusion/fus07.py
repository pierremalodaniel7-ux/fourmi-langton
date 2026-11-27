#!/usr/bin/env python3
"""S1 / R-408 Regrouper deux routes de la retenue c1 de R-405 qui ne diffèrent que d'UN pas : V0 = (0,19,2187,0), V7 = (0,19,2187,7)
(même voie, même abscisse, phases 0 et 7, temps 9 000). Recherche d'UN vaisseau constant K (direction 0…5, point de référence = celui de V0
+ décalage dans un disque de rayon R, phase 0…7, 2 ordres de jeu) tel que V0 + K et V7 + K soient propres et émettent un MÊME vaisseau O
(même trajectoire exacte), O absent du cas « K seul ». Mesure de l'« ombre » : voie la plus proche d'une sortie parallèle du cas K seul.
Écrit s1_fusion/fus07.json. Usage : python3 s1_fusion/fus07.py R"""
import sys, os, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from fa_lib import kship, decode, back, sit, lotdump
from hx import rot
from exp_osc import hd
R = int(sys.argv[1]); NB = 30; TT = NB * 8 + 600
def mk(r, L, A, ph):
    return kship(r, rot(((L + A) // 2, (L - A) // 2), r), ph)
V0 = mk(0, 19, 2187, 0); V7 = mk(0, 19, 2187, 7); g0 = rot(((19 + 2187) // 2, (19 - 2187) // 2), 0)
V0b, V7b = back(V0, NB), back(V7, NB)
cfg = []; lines = []
for rK in range(6):
    for ox in range(-R, R + 1):
        for oy in range(-R, R + 1):
            if hd(ox, oy) > R: continue
            for tau in range(8):
                K = back(kship(rK, (g0[0] + ox, g0[1] + oy), tau), NB)
                for order in (0, 1):
                    cfg.append((rK, ox, oy, tau, order, K))
                    for V in (V0b, V7b):
                        lines.append(sit([V, K] if order == 0 else [K, V]))
                lines.append(sit([K]))
t0 = time.time(); out = lotdump(lines, TT); print(len(lines), 'simulations', round(time.time() - t0), 's', flush=True)
res = []; i = 0; seen = 0
for c in range(0, len(cfg), 2):
    # 2 ordres par K : lignes [o0 V0, o0 V7, o1 V0, o1 V7, K seul]
    blk = out[i:i + 5]; i += 5
    dN = decode(*blk[4])
    for order in (0, 1):
        d0, d7 = decode(*blk[2 * order]), decode(*blk[2 * order + 1])
        if d0 is None or d7 is None or dN is None: continue
        com = set(map(tuple, d0)) & set(map(tuple, d7)) - set(map(tuple, dN))
        if not com: continue
        for O in com:
            ombre = min([abs(O[1] - s[1]) for s in dN if s[0] == O[0]] or [99])
            rK, ox, oy, tau, _, K = cfg[c]
            res.append(dict(rK=rK, o=(ox, oy), tau=tau, order=order, O=O, ombre=ombre, d0=d0, d7=d7, seul=dN, K=K))
json.dump(res, open(os.path.join(HERE, 'fus07.json'), 'w'))
print(len(res), 'fusions V0/V7 à 1 constant ;', sum(r['ombre'] > 6 for r in res), 'sans ombre (> 6 voies)')
import collections; print(collections.Counter((r['rK'], r['O'][0], min(r['ombre'], 9)) for r in res).most_common(12))
