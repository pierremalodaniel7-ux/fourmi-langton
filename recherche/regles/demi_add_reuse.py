#!/usr/bin/env python3
"""R-326 Demi-additionneurs R2L2 de R-325 : (1) retenue C = a∧b sur la voie « A déviée » ; (2) réutilisation : 2 usages successifs
(k périodes d'écart, mêmes voies, constantes K2, K3 renvoyées à chaque usage), 16 suites (a1,b1,a2,b2) : le 2e usage doit donner
S (nombre de vaisseaux sur la voie S) et C comme une machine neuve. Puis N usages au hasard pour le meilleur."""
import json, itertools, random, sys
from banc import sit, rotv
from outils_r import lot, parse
R = 'H:R2L2'; P = 8
F = json.load(open('data/demi_add4.json')); k = 200; NF = int(sys.argv[1]) if len(sys.argv) > 1 else 60
def tracks(l):
    d = parse(l); return [((a[1], a[2]), a[1] * d['fin'][i][1] - a[2] * d['fin'][i][0]) if a else None for i, a in enumerate(d['ants'])]
B = ((0, 0, 4), [(1, 0)]); A = ((29, -56, 0), [(28, -55)])
lc = lot([sit(R, [B[0], A[0]], {(1, 0): 1, (28, -55): 1})], 1 << 16)[0]; Ctrack = tracks(lc)[1]
def build(f, uses):
    srcs = {'B': B, 'A': A, 'K2': (tuple(f['K2'][0]), [tuple(c) for c in f['K2'][1]]), 'K3': (tuple(f['K3'][0]), [tuple(c) for c in f['K3'][1]])}
    dd = {}
    for n, (x, cc) in srcs.items():          # direction de chaque source (pour reculer sur sa voie)
        dd[n] = tracks(lot([sit(R, [x], {c: 1 for c in cc})], 1 << 16)[0])[0][0]
    al = []; ce = {}
    for u, (a, b) in enumerate(uses):
        for n, on in (('B', b), ('A', a), ('K2', 1), ('K3', 1)):
            if not on: continue
            x, cc = srcs[n]; v = (-u * k * dd[n][0], -u * k * dd[n][1])
            al.append((x[0] + v[0], x[1] + v[1], x[2])); [ce.__setitem__((c[0] + v[0], c[1] + v[1]), 1) for c in cc]
    return sit(R, al, ce)
def SC(l, S):
    t = tracks(l)
    if any(x is None for x in t): return None
    return (sum(1 for x in t if x == S), sum(1 for x in t if x == Ctrack))
res_all = []
for fi, f in enumerate(F[:NF]):
    S = (tuple(f['S'][0]), f['S'][1])
    one = {ab: SC(l, S) for ab, l in zip(((0,0),(1,0),(0,1),(1,1)), lot([build(f, [ab]) for ab in ((0,0),(1,0),(0,1),(1,1))], 1 << 19))}
    okC = one == {(0,0): (0,0), (1,0): (1,0), (0,1): (1,0), (1,1): (0,1)}
    if not okC: res_all.append((fi, 'table', one)); continue
    seqs = list(itertools.product(((0,0),(1,0),(0,1),(1,1)), repeat=2))
    out = lot([build(f, list(s)) for s in seqs], 1 << 20)
    good = 0
    for s, l in zip(seqs, out):
        t = SC(l, S)
        exp = tuple(a + b for a, b in zip(one[s[0]], one[s[1]]))     # total sur les voies S et C = 1er + 2e usage
        good += t == exp
    res_all.append((fi, good, 16))
    print(fi, 'table S,C juste ; suites justes', good, '/ 16', flush=True)
ok = [r for r in res_all if r[1] == 16]
print('demi-additionneurs : table juste', sum(1 for r in res_all if r[1] != 'table'), '/', len(res_all), '; réutilisables 16/16 :', len(ok))
json.dump({'resultats': [list(map(str, r)) for r in res_all], 'reutilisables': [r[0] for r in ok]}, open('data/demi_add_reuse.json', 'w'))
