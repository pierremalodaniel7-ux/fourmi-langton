#!/usr/bin/env python3
"""R-315 Réutilisation d'un lieu de choc : pour chaque choc « dévié » (2 vaisseaux propres, ≥ 1 direction changée) de R-310,
(1) cases laissées près du point de choc ; (2) on rejoue le même choc avec une 2e paire translatée de k périodes en arrière le long
de B (k = 40, 100) : les 2 sorties de la 2e paire sont-elles EXACTEMENT les sorties de la 1re translatées ? Usage : reuse_chocs.py REGLE"""
import sys, json, subprocess, collections
from banc import launcher, sit, path, outcome, rotv, K, TB
from outils_r import lot, parse, geo
G = json.load(open('data/germes_regles.json'))
rule = sys.argv[1]; W = 3
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
                confs.append((r, a2, c2))
TT = 60 * K * P
def tr(a, c, v): return (a[0] + v[0], a[1] + v[1], a[2]), {(x + v[0], y + v[1]): k for (x, y), k in c.items()}
L1 = []
for r, a2, c2 in confs:
    c = dict(cells); c.update(c2); L1.append(sit(rule, [ant, a2], c))
R1 = lot(L1, TT, ('-x',))
dev = []
for (r, a2, c2), l in zip(confs, R1):
    ob, oa = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, rotv(rule, D, r))
    if ob[0] == 'propre' and oa[0] == 'propre' and not (ob[1] == 0 and oa[1] == 0) and 'x2' not in parse(l)['sig']:
        dev.append((r, a2, c2, parse(l)['fin'], (ob[1], oa[1])))
print(rule, 'chocs déviés', len(dev))
stat = collections.Counter(); ex = []
for k in (40, 100):
    v = (-k * D[0], -k * D[1]); L2 = []
    for r, a2, c2, fin, ty in dev:
        b2, cb = tr(ant, cells, v); a3, c3 = tr(a2, c2, v)
        c = dict(cells); c.update(c2); c.update(cb); c.update(c3)
        L2.append(sit(rule, [ant, a2, b2, a3], c))
    R2 = lot(L2, TT + k * P, ('-x',))
    for (r, a2, c2, fin, ty), l in zip(dev, R2):
        f2 = parse(l)['fin']
        # la 2e paire, en retard de k périodes, doit être à (fin1 translatée de v) décalée de -k périodes de sa propre direction ;
        # on compare donc les VOIES et directions : même direction que la 1re et même voie (relative à la translation v)
        d = parse(l); a = d['ants']
        ok = len(a) == 4 and all(a) and (a[2][1], a[2][2]) == (a[0][1], a[0][2]) and (a[3][1], a[3][2]) == (a[1][1], a[1][2])
        if ok:
            for i0, i1 in ((0, 2), (1, 3)):
                dx, dy = a[i0][1], a[i0][2]
                l0 = dx * (f2[i0][1] + v[1]) - dy * (f2[i0][0] + v[0]); l1 = dx * f2[i1][1] - dy * f2[i1][0]
                if l0 != l1: ok = False
        stat[(k, ok)] += 1
        if ok and k == 100 and len(ex) < 5: ex.append(l.split('|')[:3])
print('  2e choc identique (mêmes directions, mêmes voies) :', {f"k={k}": f"{stat[(k, True)]}/{len(dev)}" for k in (40, 100)})
json.dump({'regle': rule, 'devies': len(dev), 'stat': {str(k): v for k, v in stat.items()}, 'exemples': ex}, open('data/reuse_chocs_' + rule.replace(':', '_') + '.json', 'w'))
