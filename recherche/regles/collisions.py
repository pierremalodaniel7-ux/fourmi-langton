#!/usr/bin/env python3
"""R-310 Catalogue des chocs de 2 autoroutes « fraîches » (même règle) : B depuis l'origine, A tournée de r crans,
départ X - kA·D_A + (i,j), i,j ∈ [-W,W], kA ∈ {K-1, K, K+1} (A et B arrivent ensemble en X).
Classes : T transparent (les 2 comme seules), S décalées (même directions, voie changée), D déviées (≥ 1 direction changée,
2 autoroutes propres), F fusion/groupe, X autre (perte, chaos, autre autoroute). Usage : python3 collisions.py REGLE [W]"""
import sys, json, collections
from banc import launcher, sit, path, outcome, rotv, K, TB
from outils_r import lot, parse, geo
G = json.load(open('data/germes_regles.json'))
rule = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 4
g = G[rule]; P, D = g['P'], tuple(g['D']); _, M = geo(rule)
ant, cells = launcher(g); t2 = K * P
X = path(rule, [ant], cells, t2, t2)[0][:2]
confs = []
for r in range(1, M):
    DA = rotv(rule, D, r)
    for kA in (K - 1, K, K + 1):
        for i in range(-W, W + 1):
            for j in range(-W, W + 1):
                st = (X[0] - kA * DA[0] + i, X[1] - kA * DA[1] + j)
                a2, c2 = launcher(g, r, st)
                if any(abs(x - ant[0]) + abs(y - ant[1]) < 3 for x, y in list(c2) + [a2[:2]]): continue
                c = dict(cells); c.update(c2)
                confs.append((r, kA, i, j, sit(rule, [ant, a2], c), sit(rule, [a2], c2)))
res = lot([c[4] for c in confs], TB)
solA = lot([c[5] for c in confs], TB)
solB = outcome(rule, lot([sit(rule, [ant], cells)], TB)[0], 0, P, D)
cat = collections.Counter(); types = collections.Counter(); ex = {}
for c, l, sa in zip(confs, res, solA):
    r = c[0]; DA = rotv(rule, D, r)
    ob, oa, s = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, DA), outcome(rule, sa, 0, P, DA)
    sig = parse(l)['sig']
    if ob[0] == 'propre' and oa[0] == 'propre':
        if ob[1] == 0 and oa[1] == 0:
            k = 'T' if ob[2] == solB[2] and oa[2] == s[2] else 'S'
        else: k = 'D'
        if 'x2' in sig: k = 'F'
    else: k = 'X'
    cat[(r, k)] += 1
    if k == 'D': types[(r, ob[1], oa[1])] += 1; ex.setdefault((r, ob[1], oa[1]), c[4])
    if k == 'T': ex.setdefault((r, 'T'), c[4])
print(rule, 'chocs', len(confs))
for r in range(1, M):
    print(f"  r={r} ({360 * r // M}°) :", ' '.join(f"{k}={cat[(r, k)]}" for k in 'TSDFX'))
print('  types de déviation (r, sortie B, sortie A) :', dict(types))
json.dump({'regle': rule, 'n': len(confs), 'cat': {str(k): v for k, v in cat.items()}, 'types': {str(k): v for k, v in types.items()},
           'exemples': {str(k): v for k, v in ex.items()}}, open('data/collisions_' + rule.replace(':', '_') + '.json', 'w'))
