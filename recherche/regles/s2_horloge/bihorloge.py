"""T2 — BI-HORLOGE CONCENTRIQUE : deux horloges triangle DIFFÉRENTES de même période P (donc même T = P/3), même centre de rotation,
B tournée de k·60° (k = 0 : même sens ; k = 1 : étoile comme l'hexagramme R-512) et avancée de s pas, s ∈ [0, P).
Pourquoi : la machine entière garde la symétrie « tiers » (rotation 120° + T pas), donc la fermeture ne porte que sur un tiers (R-514) ;
avec deux horloges de géométries différentes, les portes peuvent voir des entrées plus variées que dans l'hexagramme.
Critère : CYCLE exact fourmi_r (T = 6P), puis interaction réelle (trajectoire ≠ superposition, hx.py).
Usage : python3 s2_horloge/bihorloge.py Pmin Pmax k [max_paires]   (écrit s2_horloge/bihorloge_<Pmin>_<Pmax>_<k>.json au fur et à mesure)"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import numpy as np
from fractions import Fraction as Fr
from hx import step, rot
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from deux_horloges import traj, rotarr
def centre(c):
    # p tel que p − rot120(p) = c  (rot120 = 2 crans) ; solution exacte en fractions
    # rot120(x, y) = (−x − y, x)  ⇒  (2x + y, y − x) = c
    cx, cy = c; x = Fr(cx - cy, 3); y = Fr(cx + 2 * cy, 3)
    assert 2 * x + y == cx and y - x == cy
    return (x, y)
Pmin, Pmax, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); maxp = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
byP = collections.defaultdict(list)
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if Pmin <= w['P'] <= Pmax: byP[w['P']].append(w)
out_name = 's2_horloge/bihorloge_%d_%d_%d.json' % (Pmin, Pmax, k)
hits = []; tot = collections.Counter(); npairs = 0
for P in sorted(byP):
    # horloges distinctes (une horloge vue à un autre instant = la même) : signature = ensemble des états relatifs au centre
    U = []
    for w in byP[P]:
        cx, cy = centre(w['c'])
        if k == 1 and (cx.denominator != 1 or cy.denominator != 1): continue
        a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
        sig = set(); snaps = []
        for t in range(P):
            st = (tuple(sorted((q[0] - cx, q[1] - cy, q[2]) for q in A)), tuple(sorted((x - cx, y - cy) for x, y in G)))
            sig.add(hash(st)); snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
        first = hash((tuple(sorted((q[0] - cx, q[1] - cy, q[2]) for q in parts_of(w['sit'])[0])),
                      tuple(sorted((x - cx, y - cy) for x, y in parts_of(w['sit'])[1]))))
        if any(first in u['sig'] for u in U): continue
        U.append({'w': w, 'sig': sig, 'snaps': snaps, 'cen': (cx, cy)})
    for i in range(len(U)):
        for j in range(len(U)):
            if i == j or npairs >= maxp: continue      # i == j avec k = 1 : hexagramme (déjà fait, R-512) ; k = 0 : double horloge (R-511)
            if k == 0 and j < i: continue
            A_, B_ = U[i], U[j]; ax, ay = A_['cen']; bx, by = B_['cen']
            tx, ty = ax - bx, ay - by
            if tx.denominator != 1 or ty.denominator != 1: continue
            npairs += 1
            a, c = parts_of(A_['w']['sit']); lines = []
            for s in range(P):
                Bq, Gb = B_['snaps'][s]
                if k == 0:
                    B2 = [(int(x + tx), int(y + ty), h) for x, y, h in Bq]; C2 = [(int(x + tx), int(y + ty)) for x, y in Gb]
                else:
                    B2 = []; C2 = []
                    for x, y, h in Bq:
                        u, v = rot((int(x - bx), int(y - by)), 1); B2.append((int(u + ax), int(v + ay), (h + 1) % 6))
                    for x, y in Gb:
                        u, v = rot((int(x - bx), int(y - by)), 1); C2.append((int(u + ax), int(v + ay)))
                if set(C2) & set(map(tuple, c)) or {q[:2] for q in B2} & {tuple(x[:2]) for x in a}: continue
                lines.append((s, fmt([tuple(q) for q in a] + B2, [tuple(x) for x in c] + C2)))
            res = lot([l for _, l in lines], 6 * P + 10)
            X0 = None
            for (s, l), o in zip(lines, res):
                f = o.split('|'); tot[f[3]] += 1
                if f[3] != 'CYCLE': continue
                if X0 is None:
                    XA = traj(A_['w']['sit'], 2 * P); XB = traj(B_['w']['sit'], 2 * P)
                    if k == 0: XB = XB + np.array([int(tx), int(ty)])
                    else: XB = rotarr(XB - np.array([int(bx), int(by)]), 1) + np.array([int(ax), int(ay)])
                X = traj(l, P); d = int((X != np.concatenate([XA[:P], XB[s:s + P]], 1)).any(-1).any(-1).sum())
                hits.append({'P0': P, 'i': i, 'j': j, 'k': k, 's': s, 'P': int(f[5]), 'diff': d, 'sit': l})
            json.dump(hits, open(out_name, 'w'))
            print('P', P, 'paire', i, j, '/', len(U), dict(tot), 'CYCLE', len(hits), 'interaction', sum(h['diff'] > 0 for h in hits), flush=True)
print('fin', npairs, 'paires', dict(tot), 'CYCLE', len(hits), 'interaction', sum(h['diff'] > 0 for h in hits))
print(collections.Counter((h['P0'], h['P']) for h in hits if h['diff'] > 0).most_common(12))
