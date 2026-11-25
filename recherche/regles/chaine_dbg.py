#!/usr/bin/env python3
"""R-319 (suite) Réutilisation du circuit à 2 étages : 1er usage (a1,b1,c1), 2e usage (a2,b2,c2) k périodes plus tard sur les mêmes
voies. Juste si TOUTES les fourmis du 2e usage sortent (direction, voie) comme dans un circuit neuf. 56 suites (1er usage non vide,
2e non vide) par placement."""
import json, itertools, sys
from banc import launcher, sit, outcome, rotv
from outils_r import lot
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1)
F = json.load(open('data/chaine_r2l2.json')); k = int(sys.argv[1]) if len(sys.argv) > 1 else 200; NF = int(sys.argv[2]) if len(sys.argv) > 2 else 20
def ps(s):
    r, a, c = s.split('|')
    return [tuple(map(int, t.split(','))) for t in a.split(';')], [tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t]
def tr(x, cc, v): return (x[0] + v[0], x[1] + v[1], x[2]), {(p[0] + v[0], p[1] + v[1]): 1 for p in cc}
tot_ok = 0; good = []
for f in F[:NF]:
    ants, cells = ps(f['porte1'])
    B = (ants[0], {(1, 0): 1}); A = (ants[1], {c: 1 for c in cells if c != (1, 0)})
    C = launcher(G, f['r'], tuple(f['C']))
    dirs = {'B': D, 'A': rotv(R, D, (ants[1][2] - 4) % 6), 'C': rotv(R, D, f['r'])}
    sh = {n: (-k * d[0], -k * d[1]) for n, d in dirs.items()}
    srcs = {'B': B, 'A': A, 'C': C}
    L = []; meta = []
    for bits in itertools.product((0, 1), repeat=6):
        first, second = bits[:3], bits[3:]
        if not any(first) or not any(second): continue
        for kind, on1 in (('seq', first), ('ref', (0, 0, 0))):
            al = []; ce = {}; idx = {}
            for (n, on) in zip('ABC', on1):
                if on: x, cc = srcs[n]; al.append(x); ce.update(cc)
            for (n, on) in zip('ABC', second):
                if on: x, cc = tr(*srcs[n], sh[n]); idx[n] = len(al); al.append(x); ce.update(cc)
            L.append(sit(R, al, ce)); meta.append((bits, kind, idx))
    out = lot(L, 1 << 19, ncpu=2)
    res = {}
    for l, (bits, kind, idx) in zip(out, meta):
        res[(bits, kind)] = {n: outcome(R, l, i, P, dirs[n])[:3] for n, i in idx.items()}
    bad = [b for b in {m[0] for m in meta} if not (res[(b, 'seq')] == res[(b, 'ref')] and all(v[0] == 'propre' for v in res[(b, 'seq')].values()))]
    print('  échecs (a1b1c1 a2b2c2):', sorted(bad)[:10])
    ok = sum(1 for bits in {m[0] for m in meta} if res[(bits, 'seq')] == res[(bits, 'ref')] and all(v[0] == 'propre' for v in res[(bits, 'seq')].values()))
    n = len({m[0] for m in meta}); tot_ok += ok == n
    if ok == n: good.append(f)
    print(f"placement {f['C']} r={f['r']} : {ok}/{n} suites justes", flush=True)
print('circuits à 2 étages entièrement réutilisables :', tot_ok, '/', min(NF, len(F)))
json.dump(good, open('data/chaine_reuse_ok.json', 'w'))
