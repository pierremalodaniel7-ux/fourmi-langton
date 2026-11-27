"""T2 — ÉTOILE DÉCALÉE (symétrie d'ordre 2) : horloge triangle A + B = image de A par la rotation de 180° autour d'un point O
(O entier ou demi-entier, PAS le centre de A), B avancée de s pas. Pour s = 0 ou P/2 la superposition vérifie état(t + s) = g(état(t)),
g = rotation 180° autour de O (ordre 2) : une porte X et sa jumelle g(X) peuvent alors être dans des états DIFFÉRENTS au même instant,
ce qui permettrait une porte qui alterne (diviseur par 2) — impossible dans une machine 3-symétrique où les portes sont équivalentes.
CYCLE exact fourmi_r (T = 6P), interaction réelle (≠ superposition).
On ne teste que s = 0 et s = P/2 (les deux s qui donnent la symétrie d'ordre 2).
Usage : python3 s2_horloge/etoile180.py Pmin Pmax rmax [max_horloges]   (écrit s2_horloge/etoile180_<Pmin>_<Pmax>.json au fur et à mesure)"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import numpy as np
from hx import step
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from deux_horloges import traj
from fractions import Fraction as Fr
def centre(c):
    cx, cy = c; return (Fr(cx - cy, 3), Fr(cx + 2 * cy, 3))   # p − rot120(p) = c (voir bihorloge.py)
Pmin, Pmax, rmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); maxh = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
W = [w for w in json.load(open('s2_horloge/tri_cycles_rB5.json')) if Pmin <= w['P'] <= Pmax]
seen = set(); WU = []
for w in W:   # une horloge par (P, taille) suffit pour un premier balayage
    X = traj(w['sit'], 1).reshape(-1, 2)
    key = (w['P'], w['boite'] if 'boite' in w else None)
    if key in seen: continue
    seen.add(key); WU.append(w)
WU = WU[:maxh]
out_name = 's2_horloge/etoile180_%d_%d.json' % (Pmin, Pmax)
hits = []; tot = collections.Counter()
for n, w in enumerate(WU):
    P = w['P']; cx, cy = centre(w['c'])
    a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    snaps = []
    for t in range(P): snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
    XA = traj(w['sit'], 2 * P)
    # O = centre de A + (u/2, v/2), décalage non nul de distance ≤ rmax (en demi-cases)
    c2 = (round(2 * cx), round(2 * cy))
    Os = [(u, v) for u in range(-rmax, rmax + 1) for v in range(-rmax, rmax + 1) if (abs(u) + abs(v) + abs(u + v)) // 2 <= rmax]
    lines = []
    for (u, v) in Os:
        # x -> 2O - x avec 2O = (tx, ty) entier, proche de 2·centre(A) mais différent (sinon : hexagramme R-512)
        tx, ty = c2[0] + u, c2[1] + v
        if (tx, ty) == (2 * cx, 2 * cy): continue
        for s in ([0, P // 2] if P % 2 == 0 else [0]):
            Bq, Gb = snaps[s]
            B2 = [(tx - x, ty - y, (h + 3) % 6) for x, y, h in Bq]; C2 = [(tx - x, ty - y) for x, y in Gb]
            if set(C2) & set(map(tuple, c)) or {q[:2] for q in B2} & {tuple(x[:2]) for x in a}: continue
            lines.append((s, tx, ty, fmt([tuple(q) for q in a] + B2, [tuple(x) for x in c] + C2)))
    if True:
        res = lot([l for *_, l in lines], 6 * P + 10)
        for (s, tx, ty, l), o in zip(lines, res):
            f = o.split('|'); tot[f[3]] += 1
            if f[3] != 'CYCLE': continue
            XB = np.array([tx, ty]) - XA[s:s + P]
            X = traj(l, P); d = int((X != np.concatenate([XA[:P], XB], 1)).any(-1).any(-1).sum())
            if d > 0: hits.append({'P0': P, 'O2': [tx, ty], 's': s, 'P': int(f[5]), 'diff': d, 'sit': l})
    json.dump(hits, open(out_name, 'w'))
    print(n, len(WU), 'P', P, dict(tot), 'CYCLE avec interaction', len(hits), flush=True)
print('fin', dict(tot), 'interaction', len(hits))
print(collections.Counter((h['P0'], h['P']) for h in hits).most_common(12))
