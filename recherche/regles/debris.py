#!/usr/bin/env python3
"""R-317 Débris laissés par les chocs de 2 vaisseaux (cases non blanches à distance < 60 du point de choc, 14 400 pas)."""
import sys, json, subprocess, collections
from banc import launcher, sit, path, outcome, rotv, K
from outils_r import lot, parse, geo
rule = sys.argv[1]; G = json.load(open('data/germes_regles.json')); g = G[rule]; P, D = g['P'], tuple(g['D']); _, M = geo(rule)
ant, cells = launcher(g); X = path(rule, [ant], cells, K * P, K * P)[0][:2]
L = []; meta = []
for r in range(1, M):
    DA = rotv(rule, D, r)
    for kA in (K - 1, K, K + 1):
        for i in range(-3, 4):
            for j in range(-3, 4):
                st = (X[0] - kA * DA[0] + i, X[1] - kA * DA[1] + j); a2, c2 = launcher(g, r, st)
                if any(abs(x) + abs(y) < 3 for x, y in list(c2) + [a2[:2]]): continue
                c = dict(cells); c.update(c2); L.append(sit(rule, [ant, a2], c)); meta.append(r)
T = 60 * K * P
out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input='\n'.join(L) + '\n', capture_output=True, text=True).stdout.splitlines()
res = [l for l in out if not l.startswith('DUMP')]; dumps = [l for l in out if l.startswith('DUMP')]
st = collections.Counter(); ex = {}
for r, l, dmp in zip(meta, res, dumps):
    ob, oa = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, rotv(rule, D, r))
    kind = 'X' if not (ob[0] == 'propre' and oa[0] == 'propre') else 'T' if ob[1] == 0 and oa[1] == 0 else 'D'
    cs = [tuple(map(int, c.split(',')[:2])) for c in dmp.split('|')[2].split(';') if c]
    deb = sum(1 for c in cs if abs(c[0] - X[0]) + abs(c[1] - X[1]) < 60 and abs(c[0]) + abs(c[1]) > 6)
    st[(kind, min(deb, 9))] += 1
    if kind == 'D' and deb == 0: ex.setdefault(r, l.split('|')[:3])
print(rule, sorted(st.items()))
print('  chocs déviés SANS débris, exemples :', ex)
json.dump({'stat': {str(k): v for k, v in st.items()}, 'exemples_sans_debris': ex}, open('data/debris_' + rule.replace(':', '_') + '.json', 'w'))
