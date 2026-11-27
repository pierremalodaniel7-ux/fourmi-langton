#!/usr/bin/env python3
"""S1 / R-406 Croisements DANS l'additionneur 2 bits R-405 : pour chaque cas, chaque paire de fourmis (i, j) qui n'interagissent pas
(chacune suit pas à pas sa trajectoire du système « sans l'autre ») mais dont les CHEMINS se coupent (même case visitée à des instants
différents) = croisement. On mesure la distance minimale à temps égal, et l'écart de temps au point de croisement.
Chemin = simulation 0 … W (un usage).
Usage : python3 s1_fusion/croise_add2.py D"""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
from add2_perm import build
from circuit import traj, hdist
D = int(sys.argv[1]); W = 5000; X = 4000
ALL = build('A', 0, D)
names = [n for n, p, v in ALL.pieces]; vars_ = [v for n, p, v in ALL.pieces]
etage = lambda n: 0 if not n.endswith('1') else 1
res = []
for inp in ALL.cases():
    P, vin, vout = traj(ALL, inp, W)
    present = [i for i, (n, p, v) in enumerate(ALL.pieces) if v is None or inp.get(v)]
    nm = [names[i] for i in present]
    # chemins prolongés : temps −X … W + X
    paths = []
    for a in range(P.shape[1]):
        cells = {}
        for t in range(P.shape[0]): cells.setdefault(tuple(P[t][a]), t)
        paths.append(cells)
    for a, b in itertools.combinations(range(P.shape[1]), 2):
        if etage(nm[a]) == etage(nm[b]): continue
        common = set(paths[a]) & set(paths[b])
        if not common: continue
        dmin = int(min(hdist(P[:, a] - P[:, b])))
        dt = min(abs(paths[a][c] - paths[b][c]) for c in common)
        res.append(dict(cas=''.join(str(inp[v]) for v in ('a0', 'b0', 'a1', 'b1')), i=nm[a], j=nm[b], cases_communes=len(common),
                        dist_min_meme_temps=dmin, ecart_temps=int(dt)))
json.dump(res, open(os.path.join(HERE, 'croise_add2.json'), 'w'), indent=0)
for r in res: print(r)
print(len(res), 'croisements entre étage 0 et étage 1 (chemins simulés 0 …', W, ')')
