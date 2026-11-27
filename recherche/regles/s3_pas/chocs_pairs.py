#!/usr/bin/env python3
"""R-600 Catalogue des chocs de 2 vaisseaux de la MÊME classe de caps (directions paires 0, 2, 4), avec les lignes d'univers exactes
des sorties. B = direction 0, A = direction r ∈ {2, 4} (les autres paires s'obtiennent par rotation de 120°), A avancé de τ pas,
position relative v modulo u = d_A − d_B (même méthode que ../chocs_exhaustif.py, R-333), 2 ordres de jeu.
Pour chaque choc : issue (transparent / décalé / échangé / DÉVIÉ = les deux partent dans la 3e direction / débris / lié) et lignes
d'univers des 2 sorties (à t = 0). Sortie : data/chocs_pairs.json. Usage : python3 chocs_pairs.py"""
import json, collections, os
from s3lib import *
KP = 25
dB = ship_dir(0); res = []
os.makedirs('data', exist_ok=True)
stats = collections.Counter()
for r in (1, 2, 3, 4, 5):
    dA = ship_dir(r); u = (dA[0] - dB[0], dA[1] - dB[1])
    reps = {}
    for vx in range(-30, 31):
        for vy in range(-30, 31):
            best = None
            for kk in range(-60, 61):
                w = (vx + kk * u[0], vy + kk * u[1]); key = (abs(w[0]) + abs(w[1]), w)
                if best is None or key < best: best = key
            reps[best[1]] = 1
    for tau in range(8):
        for v in reps:
            wB = (0, -KP * dB[0], -KP * dB[1], 0)
            wA = (r, v[0] - KP * dA[0], v[1] - KP * dA[1], tau)
            T = 16 * KP + 8 * 60
            dmin = min(hd(antpos(wA, t)[0] - antpos(wB, t)[0], antpos(wA, t)[1] - antpos(wB, t)[1]) for t in range(T))
            if dmin > 8: continue
            if hd(antpos(wA, 0)[0] - antpos(wB, 0)[0], antpos(wA, 0)[1] - antpos(wB, 0)[1]) <= 14: continue
            for order in (0, 1):
                W = [wA, wB] if order == 0 else [wB, wA]
                s0 = sit_wls(W)
                a, c = run_py(s0, T)
                dist = hd(a[0][0] - a[1][0], a[0][1] - a[1][1])
                d = decode(a, c, T) if dist > 14 else None
                if d is None:
                    typ = 'débris/lié'; outs = None
                else:
                    iA, iB = (0, 1) if order == 0 else (1, 0)
                    oA = decode([a[iA]], [x for x in c if hd(x[0] - a[iA][0], x[1] - a[iA][1]) <= 2], T)[0]
                    oB = decode([a[iB]], [x for x in c if hd(x[0] - a[iB][0], x[1] - a[iB][1]) <= 2], T)[0]
                    outs = (oA, oB)
                    if oA == wA and oB == wB: typ = 'transparent'
                    elif oA[0] == r and oB[0] == 0: typ = 'décalé'
                    elif oA[0] == 0 and oB[0] == r: typ = 'échangé'
                    else: typ = f"dévié A{oA[0]} B{oB[0]}"

                stats[(r, typ)] += 1
                res.append(dict(r=r, tau=tau, v=v, ordre=order, dmin=dmin, type=typ, A=wA, B=wB, sorties=outs, T=T))
for k in sorted(stats): print(k, stats[k])
json.dump(res, open('data/chocs_pairs.json', 'w'))
