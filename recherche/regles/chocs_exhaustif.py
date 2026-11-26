#!/usr/bin/env python3
"""R-333 TOUS les chocs de 2 vaisseaux R2L2 (calcul exhaustif sur un ensemble FINI de géométries relatives).
B = vaisseau r = 0 (phase 0) ; A = vaisseau de direction r ∈ 1..5, avancé de τ ∈ 0..7 pas ; position relative v ∈ Z² modulo
u = d_A − d_B (décaler le temps de 8 pas pour les deux = ajouter u à v) ; 2 ordres de jeu (A puis B, B puis A).
r = 0 (même direction) : les deux ne se rapprochent jamais (pas de choc). Rotation globale : B peut toujours être mis en r = 0.
Interaction possible seulement si les fourmis passent à distance ≤ DMAX (cases noires d'un vaisseau à distance ≤ 3 de sa fourmi,
+ 1 pas, + marge) : sinon chacun ne voit que du blanc → transparent EXACT. On simule les autres jusqu'à séparation et on classe.
Sortie : resumes/chocs_exhaustif.json + texte. Usage : python3 chocs_exhaustif.py [K] (K périodes avant le choc, défaut 25)"""
import sys, json, collections
from hx import HX, K as KT, ship, ship_dir, step, PHASES, rot, sit
KP = int(sys.argv[1]) if len(sys.argv) > 1 else 25
def hd(dx, dy): return (abs(dx) + abs(dy) + abs(dx + dy)) // 2
RAD = max(hd(cx, cy) for (h, cs) in PHASES for (cx, cy) in cs)     # rayon des cases noires d'un vaisseau autour de sa fourmi
DMAX = 2 * RAD + 2
def germ(r, pos, tau):
    a, c = ship(r, pos); ants = [list(a)]; g = {c: 1}
    for _ in range(tau): step(ants, g)
    return ants[0], g
def traj(ant, g, T):
    ants = [list(ant)]; g = dict(g); out = []
    for _ in range(T): step(ants, g); out.append((ants[0][0], ants[0][1]))
    return out
def ident(ants, g, k):
    """vaisseau ? fourmi k + cases noires à distance ≤ RAD (en excluant celles plus proches d'une autre fourmi)"""
    x, y, h = ants[k]
    near = frozenset((cx - x, cy - y) for (cx, cy) in g if hd(cx - x, cy - y) <= RAD
                     and all(hd(cx - b[0], cy - b[1]) > hd(cx - x, cy - y) for j, b in enumerate(ants) if j != k))
    return PHASES.get((h, near)), near
dB = ship_dir(0); res = []; T0 = 8 * KP
stats = collections.Counter(); outcomes = collections.Counter(); exemples = {}
for r in range(1, 6):
    dA = ship_dir(r); u = (dA[0] - dB[0], dA[1] - dB[1])
    # représentants de Z² / <u> : v et v + k u identifiés ; on garde le représentant du plus petit |v|
    reps = {}
    for vx in range(-30, 31):
        for vy in range(-30, 31):
            best = None
            for kk in range(-60, 61):
                w = (vx + kk * u[0], vy + kk * u[1]); key = (abs(w[0]) + abs(w[1]), w)
                if best is None or key < best: best = key
            reps[best[1]] = 1
    for tau in range(8):
        for v in reps:
            # trajectoires non perturbées : B part de −KP·dB, A de v − KP·dA (avancé de tau)
            bA, gA = germ(r, (v[0] - KP * dA[0], v[1] - KP * dA[1]), tau)
            bB, gB = germ(0, (-KP * dB[0], -KP * dB[1]), 0)
            tA, tB = traj(bA, gA, 2 * T0), traj(bB, gB, 2 * T0)
            dmin = min(hd(p[0] - q[0], p[1] - q[1]) for p, q in zip(tA, tB))
            if hd(bA[0] - bB[0], bA[1] - bB[1]) <= DMAX + 4: stats['départ trop proche'] += 1; continue
            if dmin > DMAX: stats['transparent exact (jamais assez proches)'] += 1; continue
            for order in (0, 1):
                ants = [list(bA), list(bB)] if order == 0 else [list(bB), list(bA)]
                g = dict(gA); g.update(gB)
                s0 = sit(ants, sorted(g))
                T = 2 * T0 + 8 * 60
                for _ in range(T): step(ants, g)
                iA, iB = (0, 1) if order == 0 else (1, 0)
                dist = hd(ants[0][0] - ants[1][0], ants[0][1] - ants[1][1])
                pa, _ = ident(ants, g, iA); pb, _ = ident(ants, g, iB)
                if dist > DMAX + 6 and pa and pb:
                    deb = len(g) - len(ident(ants, g, iA)[1]) - len(ident(ants, g, iB)[1])
                    kind = (pa[0], pb[0], deb)
                    typ = 'propre' if deb == 0 else 'débris'
                else:
                    kind = ('lié' if dist <= DMAX + 6 else 'autre', dist, len(g)); typ = kind[0]
                stats[typ] += 1; outcomes[(r, kind[:2] if typ in ('propre', 'débris') else kind[0], typ)] += 1
                res.append({'r': r, 'tau': tau, 'v': v, 'ordre': order, 'dmin': dmin, 'type': typ, 'sortie': kind, 'situation': s0, 'T': T})
                exemples.setdefault((r, str(kind[:2]), typ), s0)
print(f'RAD = {RAD}, DMAX = {DMAX}, K = {KP} périodes avant le choc')
print('bilan :', dict(stats))
for k in sorted(outcomes, key=str): print('  r_A =', k[0], 'sortie (r_A\', r_B\')' if k[2] in ('propre', 'débris') else '', k[1], k[2], outcomes[k])
json.dump({'stats': dict(stats), 'outcomes': {str(k): v for k, v in outcomes.items()}, 'chocs': res,
           'exemples': {str(k): v for k, v in exemples.items()}}, open('data/chocs_exhaustif.json', 'w'))
