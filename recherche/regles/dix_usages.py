#!/usr/bin/env python3
"""R-321 Le même circuit à 2 étages R2L2 utilisé N fois de suite (entrées au hasard, usages espacés de k périodes, mêmes voies).
Chaque usage est comparé au circuit neuf avec les mêmes entrées : sorties de C (direction, voie) et de A, B."""
import json, random, sys
from banc import launcher, sit, outcome, rotv
from outils_r import lot
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1)
F = json.load(open('data/chaine_r2l2.json'))
want = [tuple(map(int, a.split(','))) for a in sys.argv[1:2]] if len(sys.argv) > 1 else None
N = int(sys.argv[2]) if len(sys.argv) > 2 else 10; k = int(sys.argv[3]) if len(sys.argv) > 3 else 200
f = [x for x in F if tuple(x['C']) == want[0]][0] if want else F[0]
def ps(s):
    r, a, c = s.split('|')
    return [tuple(map(int, t.split(','))) for t in a.split(';')], [tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t]
def tr(x, cc, v): return (x[0] + v[0], x[1] + v[1], x[2]), {(p[0] + v[0], p[1] + v[1]): 1 for p in cc}
ants, cells = ps(f['porte1'])
src = {'B': (ants[0], [(1, 0)]), 'A': (ants[1], [c for c in cells if c != (1, 0)])}
Cg = launcher(G, f['r'], tuple(f['C'])); src['C'] = (Cg[0], list(Cg[1]))
dirs = {'B': D, 'A': rotv(R, D, (ants[1][2] - 4) % 6), 'C': rotv(R, D, f['r'])}
random.seed(5); seq = [tuple(random.randint(0, 1) for _ in range(3)) for _ in range(N)]
seq = [s if any(s) else (1, 1, 1) for s in seq]
al = []; ce = {}; idx = []
for u, bits in enumerate(seq):
    d = {}
    for n, on in zip('ABC', bits):
        if on:
            x, cc = tr(src[n][0], src[n][1], (-u * k * dirs[n][0], -u * k * dirs[n][1])); d[n] = len(al); al.append(x); ce.update(cc)
    idx.append(d)
lines = [sit(R, al, ce)]
for u, bits in enumerate(seq):           # références : chaque usage seul
    a2 = []; c2 = {}; d = {}
    for n, on in zip('ABC', bits):
        if on:
            x, cc = tr(src[n][0], src[n][1], (-u * k * dirs[n][0], -u * k * dirs[n][1])); d[n] = len(a2); a2.append(x); c2.update(cc)
    lines.append(sit(R, a2, c2)); idx.append(d)
out = lot(lines, 1 << 21, ncpu=2)
ok = 0
for u, bits in enumerate(seq):
    s = {n: outcome(R, out[0], i, P, dirs[n])[:3] for n, i in idx[u].items()}
    r = {n: outcome(R, out[1 + u], i, P, dirs[n])[:3] for n, i in idx[N + u].items()}
    good = s == r and all(v[0] == 'propre' for v in s.values()); ok += good
    print(f"usage {u+1:2d} entrées a,b,c = {bits} : {'juste' if good else 'FAUX'}  C → {s.get('C', '-')}")
print(f"{ok}/{N} usages justes ; situation complète : {len(al)} fourmis, {len(ce)} cases")
json.dump({'circuit': f, 'k': k, 'suite': seq, 'justes': ok, 'situation': lines[0]}, open('data/dix_usages.json', 'w'))
