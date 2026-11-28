"""T2 — HEXAGRAMME + 3e TRAIN : on part d'un hexagramme propre (R-512 : A + B = rot60(A avancée de s)), on ajoute une 3e copie C de la même
horloge, même centre : C = A avancée de s2 (k3 = 0) ou C = rot60(A avancée de s2) (k3 = 1), s2 ∈ [0, P0). La machine garde la symétrie
« tiers » (rotation 120° + T pas), et une même droite peut porter 2 vaisseaux par tiers : condition nécessaire d'une porte qui alterne
(diviseur par 2) dans une machine 3-symétrique (R-516). CYCLE exact fourmi_r (T = 8 P0), puis analyse des portes (t2_regulier).
Usage : python3 s2_horloge/hexa3.py fichier_propres.json k3 [i0 i1]   (écrit s2_horloge/hexa3_<k3>_<i0>.json au fur et à mesure)"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, rot
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
F = json.load(open(sys.argv[1])); k3 = int(sys.argv[2])
i0, i1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, len(F))
out_name = 's2_horloge/hexa3_%d_%d.json' % (k3, i0)
hits = []; tot = collections.Counter()
for n in range(i0, min(i1, len(F))):
    h = F[n]; P0 = h['P0']; px, py = h['centre']
    a, c = parts_of(h['horloge']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    ma, mc = parts_of(h['sit'])
    lines = []
    for s2 in range(P0):
        Bq = [tuple(q) for q in A]; Gb = list(G)
        if k3 == 1:
            B2 = []; CC = []
            for x, y, hh in Bq:
                u, v = rot((x - px, y - py), 1); B2.append((u + px, v + py, (hh + 1) % 6))
            for x, y in Gb:
                u, v = rot((x - px, y - py), 1); CC.append((u + px, v + py))
        else:
            B2 = Bq; CC = Gb
        step(A, G)
        if set(CC) & set(mc) or {q[:2] for q in B2} & {q[:2] for q in ma}: continue
        lines.append((s2, fmt(list(ma) + B2, list(mc) + CC)))
    res = lot([l for _, l in lines], 8 * P0 + 10)
    for (s2, l), o in zip(lines, res):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] == 'CYCLE': hits.append({'n': n, 'P0': P0, 's2': s2, 'k3': k3, 'P': int(f[5]), 'sit': l})
    json.dump(hits, open(out_name, 'w'))
    print(n, 'P0', P0, dict(tot), 'CYCLE', len(hits), flush=True)
print('fin', dict(tot), 'CYCLE', len(hits), collections.Counter((h['P0'], h['P']) for h in hits).most_common(10))
