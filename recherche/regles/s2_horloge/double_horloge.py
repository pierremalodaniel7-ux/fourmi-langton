"""S2 R-511 — HORLOGE DOUBLE : la même horloge triangle (R-500, terme j) posée deux fois sur le MÊME triangle, la 2e avancée de s pas.
Les 6 + 6 vaisseaux roulent sur les mêmes droites ; chaque horaire croise de face un anti-horaire de l'autre train (choc = « porte »
de croisement, qui avance les deux vaisseaux). On essaie tous les s ∈ [1, P) ; critère : CYCLE exact (fourmi_r) de toute la machine (12 fourmis),
puis interaction réelle (trajectoire ≠ superposition, hx.py). Usage : python3 s2_horloge/double_horloge.py j"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import numpy as np
from hx import step
from fa_lib import parts_of
from demi_add_k import fmt
from formule import horloge, periode
from outils_r import lot
from deux_horloges import traj
j = int(sys.argv[1]); P = periode(j)
a, c = parts_of(horloge(j)); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
snaps = []
for t in range(P): snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
lines = []
for s in range(1, P):
    Bq, Gb = snaps[s]
    if set(Gb) & set(map(tuple, c)) or any(tuple(q[:2]) in {tuple(x[:2]) for x in a} for q in Bq): lines.append(None); continue
    lines.append(fmt([tuple(q) for q in a] + Bq, [tuple(x) for x in c] + list(Gb)))
idx = [i for i, l in enumerate(lines) if l]
out = lot([lines[i] for i in idx], 6 * P + 10)
X0 = traj(horloge(j), 2 * P)
res = []; I = collections.Counter()
for i, l in zip(idx, out):
    f = l.split('|'); I[f[3]] += 1
    if f[3] != 'CYCLE': continue
    s = i + 1; Pj = int(f[5])
    X = traj(lines[i], P)
    S = np.concatenate([X0[:P], X0[s:s + P]], 1)
    diff = int((X != S).any(-1).any(-1).sum())
    res.append({'j': j, 's': s, 'P': Pj, 'diff': diff, 'sit': lines[i]})
print('j', j, 'P', P, 'décalages essayés', len(idx), 'issues', dict(I), 'CYCLE avec interaction', sum(r['diff'] > 0 for r in res))
print(collections.Counter((r['P'], r['diff'] > 0) for r in res).most_common(12))
json.dump([r for r in res if r['diff']], open('s2_horloge/double_%d.json' % j, 'w'))
