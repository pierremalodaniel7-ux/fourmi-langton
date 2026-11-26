#!/usr/bin/env python3
"""R-318 RÉUTILISATION d'une porte « à choc » (2 entrées A, B ; présence = 1) : géométries de R-310 qui dévient.
1er usage (a1,b1), puis 2e usage (a2,b2) sur LES MÊMES VOIES, k périodes plus tard (chaque entrée reculée de k périodes sur sa voie).
La porte est RÉUTILISABLE si, pour les 16 suites (a1,b1,a2,b2), les sorties du 2e usage (direction + voie de chaque fourmi)
sont celles d'une porte neuve avec (a2,b2). Usage : porte_reuse.py REGLE [k] [max_geometries]"""
import sys, json, collections, itertools
from banc import launcher, sit, path, outcome, rotv, K, TB
from outils_r import lot, parse, geo
rule = sys.argv[1]; k = int(sys.argv[2]) if len(sys.argv) > 2 else 100; NG = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
G = json.load(open('data/germes_regles.json')); g = G[rule]; P, D = g['P'], tuple(g['D']); _, M = geo(rule)
ant, cells = launcher(g); X = path(rule, [ant], cells, K * P, K * P)[0][:2]
def tr(a, c, v): return (a[0] + v[0], a[1] + v[1], a[2]), {(x + v[0], y + v[1]): kk for (x, y), kk in c.items()}
geos = []
for r in range(1, M):
    DA = rotv(rule, D, r)
    for kA in (K - 1, K, K + 1):
        for i in range(-3, 4):
            for j in range(-3, 4):
                st = (X[0] - kA * DA[0] + i, X[1] - kA * DA[1] + j); a2, c2 = launcher(g, r, st)
                if any(abs(x) + abs(y) < 3 for x, y in list(c2) + [a2[:2]]): continue
                geos.append((r, a2, c2))
# garder les géométries qui dévient (1 usage, a=b=1)
L = []
for r, a2, c2 in geos:
    c = dict(cells); c.update(c2); L.append(sit(rule, [ant, a2], c))
dev = []
for (r, a2, c2), l in zip(geos, lot(L, TB)):
    ob, oa = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, rotv(rule, D, r))
    if ob[0] == 'propre' and oa[0] == 'propre' and not (ob[1] == 0 and oa[1] == 0): dev.append((r, a2, c2))
dev = dev[:NG]
print(rule, 'k =', k, 'géométries qui dévient :', len(dev), flush=True)
def build(B, A, B2, A2, bits):
    a1, b1, a2_, b2_ = bits; ants = []; c = {}; idx = {}
    for name, (a, cc), on in (('B', B, b1), ('A', A, a1), ('B2', B2, b2_), ('A2', A2, a2_)):
        if on: idx[name] = len(ants); ants.append(a); c.update(cc)
    return ants, c, idx
lines = []; meta = []
for gi, (r, a2, c2) in enumerate(dev):
    DA = rotv(rule, D, r)
    B = (ant, cells); A = (a2, c2)
    B2 = tr(ant, cells, (-k * D[0], -k * D[1])); A2 = tr(a2, c2, (-k * DA[0], -k * DA[1]))
    for bits in itertools.product((0, 1), repeat=4):
        if bits[2] == 0 and bits[3] == 0: continue
        ants, c, idx = build(B, A, B2, A2, bits)
        lines.append(sit(rule, ants, c)); meta.append((gi, bits, idx, r, 'seq'))
        if bits[0] or bits[1]:      # référence : 2e usage seul (porte neuve)
            ants, c, idx2 = build(B, A, B2, A2, (0, 0, bits[2], bits[3]))
            lines.append(sit(rule, ants, c)); meta.append((gi, bits, idx2, r, 'ref'))
out = lot(lines, TB)
res = collections.defaultdict(dict)
for l, (gi, bits, idx, r, kind) in zip(out, meta):
    DA = rotv(rule, D, r); o = {}
    for name in ('B2', 'A2'):
        if name in idx:
            oc = outcome(rule, l, idx[name], P, D if name == 'B2' else DA); o[name] = (oc[0], oc[1], oc[2])
    res[(gi, bits)][kind] = o
okg = 0; seqok = 0; nseq = 0; ex = []
for gi in range(len(dev)):
    allok = True
    for bits in itertools.product((0, 1), repeat=4):
        if bits[2] == 0 and bits[3] == 0: continue
        if not (bits[0] or bits[1]): continue          # 1er usage vide : rien à tester
        nseq += 1
        s, rf = res[(gi, bits)]['seq'], res[(gi, bits)]['ref']
        good = s == rf and all(v[0] == 'propre' for v in s.values())
        seqok += good; allok &= good
    if allok:
        okg += 1
        if len(ex) < 5: ex.append(sit(rule, [ant, dev[gi][1]], {**cells, **dev[gi][2]}))
print(f"  suites justes : {seqok}/{nseq} ; portes réutilisables (12/12 suites) : {okg}/{len(dev)}")
json.dump({'regle': rule, 'k': k, 'geometries': len(dev), 'suites_justes': seqok, 'suites': nseq, 'portes_reutilisables': okg, 'exemples': ex},
          open(f"data/porte_reuse_{rule.replace(':', '_')}_k{k}.json", 'w'))
