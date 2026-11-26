#!/usr/bin/env python3
"""S1 / R-404 (complément) Deux vaisseaux PARALLÈLES (même direction) : à quelle distance s'influencent-ils ?
Vaisseau B direction 0 à l'origine ; A direction 0 décalé de (x, y) ∈ [−8, 8]², avancé de tau ∈ 0..7 pas, 2 ordres ;
on compare 800 pas joints aux trajectoires libres. Usage : python3 s1_fusion/paralleles.py"""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from hx import ship, step
from chocs_exhaustif_lib import hd
def run(ants, g, n):
    A = [list(a) for a in ants]; G = dict(g); P = []
    for _ in range(n): step(A, G); P.append([tuple(a[:2]) for a in A])
    return P
tab = collections.defaultdict(collections.Counter)
for x in range(-8, 9):
    for y in range(-8, 9):
        for tau in range(8):
            a, c = ship(0, (x, y)); A = [list(a)]; G = {c: 1}
            for _ in range(tau): step(A, G)
            b, cb = ship(0, (0, 0))
            if c == cb or (A[0][0], A[0][1]) == (0, 0) or cb in G: continue
            fa = run([A[0]], G, 800); fb = run([b], {cb: 1}, 800)
            dmin = min(hd(p[0][0] - q[0][0], p[0][1] - q[0][1]) for p, q in zip(fa, fb))
            for order in (0, 1):
                ants = [A[0], b] if order == 0 else [b, A[0]]; g = dict(G); g[cb] = 1
                if len(g) < 2: continue
                J = run(ants, g, 800); ia, ib = (0, 1) if order == 0 else (1, 0)
                same = all(J[t][ia] == fa[t][0] and J[t][ib] == fb[t][0] for t in range(800))
                tab[dmin][same] += 1
for d in sorted(tab): print('distance', d, ':', tab[d][True], 'sans influence,', tab[d][False], 'avec')
