#!/usr/bin/env python3
"""R-700 Catalogue des chocs PROPRES de 2 vaisseaux R2L2, en étiquettes (même ensemble fini que R-333 : B direction 0, A direction
r = 1..5, avancé de τ = 0..7, position relative v modulo u = d_A − d_B, 2 ordres de jeu).
Sortie : s4_ecran/data/chocs.json = liste de {ordre, LB, LA, sorties: [étiquette de la fourmi B, de la fourmi A]} (0 case restante,
2 vaisseaux), au temps T. Moteur fourmi_r ; échantillon recontrôlé par hx.py."""
import json, random
from lib4 import *
KP = 25
dB = ship_dir(0); lines = []; meta = []
for r in range(1, 6):
    dA = ship_dir(r); u = (dA[0] - dB[0], dA[1] - dB[1]); reps = {}
    for vx in range(-30, 31):
        for vy in range(-30, 31):
            best = min(((abs(vx + k * u[0]) + abs(vy + k * u[1]), (vx + k * u[0], vy + k * u[1])) for k in range(-60, 61)))
            reps[best[1]] = 1
    for tau in range(8):
        for v in reps:
            bA = ship(r, (v[0] - KP * dA[0], v[1] - KP * dA[1])); A = [list(bA[0])]; gA = {bA[1]: 1}
            for _ in range(tau): step(A, gA)
            pA = (tuple(A[0]), sorted(gA)); bB = ship(0, (-KP * dB[0], -KP * dB[1])); pB = (bB[0], [bB[1]])
            LA, LB = lab_piece(pA), lab_piece(pB)
            # rapprochement ? (sinon transparent exact)
            if min(hdist(antpos(LA, t), antpos(LB, t)) for t in range(0, 16 * KP, 2)) > 8: continue
            if hdist(antpos(LA, 0), antpos(LB, 0)) <= 14: continue
            for order in (0, 1):
                labs = [LB, LA] if order == 0 else [LA, LB]
                lines.append(situation(labs)); meta.append((order, LB, LA))
T = 16 * KP + 480
R = lotdump(lines, T)
cat = []; stats = {}
for (order, LB, LA), (a, c) in zip(meta, R):
    d = decode(a, c)
    if d is None or len(d) != 2: stats['sale'] = stats.get('sale', 0) + 1; continue
    iB, iA = (0, 1) if order == 0 else (1, 0)
    dd = decode([a[iB]], [p for p in c if hd(p[0] - a[iB][0], p[1] - a[iB][1]) <= 2]), decode([a[iA]], [p for p in c if hd(p[0] - a[iA][0], p[1] - a[iA][1]) <= 2])
    if not dd[0] or not dd[1]: stats['sale'] = stats.get('sale', 0) + 1; continue
    oB, oA = lab_of(dd[0][0], T), lab_of(dd[1][0], T)
    if (oB, oA) == (LB, LA): stats['transparent'] = stats.get('transparent', 0) + 1; continue
    stats['propre'] = stats.get('propre', 0) + 1
    cat.append({'ordre': order, 'LB': LB, 'LA': LA, 'oB': oB, 'oA': oA})
os.makedirs(HERE + '/data', exist_ok=True)
json.dump(cat, open(HERE + '/data/chocs.json', 'w'))
print(len(lines), 'chocs simulés', stats)
# contrôle 2e moteur sur 60 au hasard
random.seed(1); ok = 0; S = random.sample(range(len(lines)), 60)
for i in S:
    pa, pc = pyrun(lines[i], T); ok += sorted(pa) == sorted(R[i][0]) and sorted(pc) == sorted(R[i][1])
print('2 moteurs :', ok, '/ 60')
