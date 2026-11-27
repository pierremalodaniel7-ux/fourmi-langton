"""S2 R-511 — horloge DOUBLE sur toutes les horloges triangle de tri_cycles_rB5.json (P ≡ 0 mod 6 d'abord : T/2 entier possible).
Même triangle, 2e train = la même horloge avancée de s pas, s ∈ [1, P). Critère : CYCLE exact (fourmi_r, T = 6P) + interaction réelle.
Usage : python3 s2_horloge/double2.py mod Pmax   (mod = 0 : P ≡ 0 mod 6 ; 3 : P ≡ 3 mod 6) ; écrit s2_horloge/double2_<mod>.json"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import numpy as np
from hx import step
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from deux_horloges import traj
mod, Pmax = int(sys.argv[1]), int(sys.argv[2])
W = [w for w in json.load(open('s2_horloge/tri_cycles_rB5.json')) if w['P'] % 6 == mod and w['P'] <= Pmax]
hits = []; tot = collections.Counter()
for n, w in enumerate(W):
    P = w['P']; a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    snaps = []
    for t in range(P): snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
    lines = []
    for s in range(1, P):
        Bq, Gb = snaps[s]
        if set(Gb) & set(map(tuple, c)) or {q[:2] for q in Bq} & {tuple(x[:2]) for x in a}: continue
        lines.append((s, fmt([tuple(q) for q in a] + Bq, [tuple(x) for x in c] + list(Gb))))
    out = lot([l for _, l in lines], 6 * P + 10)
    X0 = None
    for (s, l), o in zip(lines, out):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] != 'CYCLE': continue
        if X0 is None: X0 = traj(w['sit'], 2 * P)
        X = traj(l, P); S = np.concatenate([X0[:P], X0[s:s + P]], 1)
        d = int((X != S).any(-1).any(-1).sum())
        if d: hits.append({'P0': P, 's': s, 'P': int(f[5]), 'diff': d, 'sit': l, 'horloge': w['sit']})
    if n % 50 == 0: print(n, len(W), dict(tot), 'trouvées', len(hits), flush=True)
print('fin', dict(tot), 'CYCLE avec interaction', len(hits))
print(collections.Counter((h['P0'], h['P']) for h in hits).most_common(10))
json.dump(hits, open('s2_horloge/double2_%d.json' % mod, 'w'))
