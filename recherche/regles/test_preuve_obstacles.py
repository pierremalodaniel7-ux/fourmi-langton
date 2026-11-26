#!/usr/bin/env python3
"""Contre-vérification de R-330 par force brute : vaisseau R2L2 lancé dans des champs de cases au hasard (densité p, carré de côté L
devant lui, et aussi demi-plan entier aléatoire) : on mesure le plus grand recul F − a ; puis direction de sortie après le champ."""
import random
from hx import HX, K, SHIP, PHASES
A = lambda x, y: x - y
random.seed(1)
worst = 0; outs = {}; n = 0
for trial in range(3000):
    p = random.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9])
    L = random.choice([3, 5, 10, 20])
    ox, oy = random.randint(5, 15), random.randint(-15, -5)
    (x, y, h), c0 = SHIP; g = {c0: 1}; vis = {(x, y), c0}
    for t in range(80):                      # 10 périodes sur du blanc (cadre de la preuve)
        c = g.get((x, y), 0); h = (h + K[c]) % 6
        if c: del g[(x, y)]
        else: g[(x, y)] = 1
        x += HX[h][0]; y += HX[h][1]; vis.add((x, y))
    ox, oy = x + random.randint(-6, 12), y + random.randint(-12, 6)
    for i in range(-L, L + 1):
        for j in range(-L, L + 1):
            q = (ox + i, oy + j)
            if q not in vis and random.random() < p: g[q] = 1      # n'importe où SAUF les cases déjà visitées
    F = max(A(*v) for v in vis); w = 0
    for t in range(4000):
        c = g.get((x, y), 0); h = (h + K[c]) % 6
        if c: del g[(x, y)]
        else: g[(x, y)] = 1
        x += HX[h][0]; y += HX[h][1]; F = max(F, A(x, y)); w = max(w, F - A(x, y))
    worst = max(worst, w); n += 1
    near = frozenset((cx - x, cy - y) for cx, cy in g if abs(cx - x) + abs(cy - y) <= 3)
    k = PHASES.get((h, near))
    outs[k[0] if k else None] = outs.get(k[0] if k else None, 0) + 1
print(f'{n} champs au hasard : recul max F−a = {worst} (preuve : ≤ 3) ; sortie (r du vaisseau : 0 = même direction) : {outs}')
