"""S2 R-512 — HEXAGRAMME : horloge triangle A + sa copie B tournée de 60° autour du centre de A (étoile à 6 branches), B avancée de s pas.
Si B = « A un demi-tiers plus tard, tourné de 60° », la symétrie (rotation 60° + T/2 pas) fait vivre à chaque vaisseau la même histoire :
les croisements des arêtes de A et de B (vaisseaux pairs à 120°, comme dans la porte R-337, R-509) seraient des « portes » alimentées par
l'horloge. Horloges de tri_cycles_rB5.json dont le centre de rotation est un point du réseau ; tous les s ∈ [0, P).
Critère : CYCLE exact fourmi_r (T = 6P) puis interaction réelle (trajectoire ≠ superposition, hx.py).
Usage : python3 s2_horloge/hexagramme.py mod Pmax   (écrit s2_horloge/hexagramme_<mod>.json)"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import numpy as np
from hx import step, rot
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from deux_horloges import traj, rotarr
def rot2(x, y):
    for _ in range(2): x, y = -y, x + y
    return x, y
Mm = np.eye(2) - np.array([rot2(1, 0), rot2(0, 1)]).T
mod, Pmax = int(sys.argv[1]), int(sys.argv[2])
W = []
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if w['P'] % 6 != mod or w['P'] > Pmax: continue
    p = np.linalg.solve(Mm, np.array(w['c'], float))
    if np.allclose(p, np.round(p)): w['centre'] = [int(round(p[0])), int(round(p[1]))]; W.append(w)
hits = []; tot = collections.Counter()
for n, w in enumerate(W):
    P = w['P']; px, py = w['centre']; a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    snaps = []
    for t in range(P): snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
    lines = []
    for s in range(P):
        Bq, Gb = snaps[s]
        B2 = [(*(np.add(rot((x - px, y - py), 1), (px, py))), (h + 1) % 6) for x, y, h in Bq]
        C2 = [tuple(np.add(rot((x - px, y - py), 1), (px, py))) for x, y in Gb]
        B2 = [tuple(int(z) for z in q) for q in B2]; C2 = [tuple(int(z) for z in q) for q in C2]
        if set(C2) & set(map(tuple, c)) or {q[:2] for q in B2} & {tuple(x[:2]) for x in a}: continue
        lines.append((s, fmt([tuple(q) for q in a] + B2, [tuple(x) for x in c] + C2)))
    out = lot([l for _, l in lines], 6 * P + 10)
    X0 = None
    for (s, l), o in zip(lines, out):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] != 'CYCLE': continue
        if X0 is None: X0 = traj(w['sit'], 2 * P)
        X = traj(l, P)
        XB = rotarr(X0[s:s + P] - np.array([px, py]), 1) + np.array([px, py])
        d = int((X != np.concatenate([X0[:P], XB], 1)).any(-1).any(-1).sum())
        hits.append({'P0': P, 's': s, 'P': int(f[5]), 'diff': d, 'sit': l, 'horloge': w['sit'], 'centre': w['centre']})
    if n % 25 == 0: print(n, len(W), dict(tot), 'CYCLE', len(hits), 'dont interaction', sum(h['diff'] > 0 for h in hits), flush=True)
print('fin', len(W), 'horloges', dict(tot), 'CYCLE', len(hits), 'dont interaction', sum(h['diff'] > 0 for h in hits))
print(collections.Counter((h['P0'], h['P'], h['diff'] > 0) for h in hits).most_common(10))
json.dump(hits, open('s2_horloge/hexagramme_%d.json' % mod, 'w'))
