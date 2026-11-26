#!/usr/bin/env python3
"""Portes d'interaction R2L2 dont le choc (a=b=1) dévie les 2 vaisseaux et ne laisse AUCUNE case (hors germes de départ)."""
import json, subprocess
from banc import launcher, sit, path, outcome, rotv, K
from outils_r import parse
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1)
ant, cells = launcher(G); X = path(R, [ant], cells, K * P, K * P)[0][:2]
L = []; meta = []
for r in range(1, 6):
    DA = rotv(R, D, r)
    for kA in (K - 1, K, K + 1):
        for i in range(-3, 4):
            for j in range(-3, 4):
                st = (X[0] - kA * DA[0] + i, X[1] - kA * DA[1] + j); a2, c2 = launcher(G, r, st)
                if any(abs(x) + abs(y) < 3 for x, y in list(c2) + [a2[:2]]): continue
                L.append(sit(R, [ant, a2], {**cells, **c2})); meta.append((r, a2, c2))
out = subprocess.run(['./fourmi_r', '-T', str(3000), '-x', '-dump', '-lot'], input='\n'.join(L) + '\n', capture_output=True, text=True).stdout.splitlines()
res = [l for l in out if not l.startswith('DUMP')]; dumps = [l for l in out if l.startswith('DUMP')]
good = []
for (r, a2, c2), l, dmp, s in zip(meta, res, dumps, L):
    d = parse(l)
    if len(d['ants']) < 2 or not all(d['ants'][:2]): continue
    ob, oa = outcome(R, l, 0, P, D), outcome(R, l, 1, P, rotv(R, D, r))
    if not (ob[0] == 'propre' and oa[0] == 'propre' and ob[1] != 0 and oa[1] != 0): continue
    cs = [tuple(map(int, c.split(',')[:2])) for c in dmp.split('|')[2].split(';') if c]
    fins = d['fin'][:2]
    deb = [c for c in cs if all(abs(c[0] - f[0]) + abs(c[1] - f[1]) > 6 for f in fins)]
    if not deb: good.append(s)
print('portes à choc dévié sans débris :', len(good))
json.dump(good, open('data/portes_propres.json', 'w'))
