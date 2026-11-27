"""T2 — 2e moteur (hx.py) pour les bascules T de phase (tbascule_200.json) : objet + 2 vaisseaux identiques (même route, Δ pas d'écart),
on vérifie : 2 vaisseaux libres, direction 0, EXACTS (même vaisseau virtuel qu'en entrée), objet revenu dans l'orbite de X0 à la même place,
et après le 1er vaisseau seul, objet DÉPHASÉ (≠ X0 non perturbé). Usage : python3 s2_horloge/tb_hx.py"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, ship_dir
from fa_lib import parts_of
from tri import at, virt
from tbascule import orbit
from exp_osc import hd
W = json.load(open('s2_horloge/tbascule_200.json')); O = json.load(open('../../data/t2/objets.json'))
ok = collections.Counter(); T1 = 700
for w in W:
    o = O[w['o']]; a, c = parts_of(o['sit']); orb = orbit(a, c, o['p'])
    A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    for _ in range(w['ph']): step(A, G)
    sh1 = (0, (w['k'] - 40, 40), w['tau']); r, p, tau = sh1; d = ship_dir(r); s = tau - w['Delta']; m = s // 8
    sh2 = (r, (p[0] + m * d[0], p[1] + m * d[1]), s % 8)
    a1, c1 = at(sh1, 0); a2, c2 = at(sh2, 0)
    A += [list(a1), list(a2)]
    for x in list(c1) + list(c2): G[tuple(x)] = 1
    Tf = T1 + w['Delta']
    for _ in range(Tf): step(A, G)
    v1 = virt(tuple(A[2]), G, Tf)[0]; v2 = virt(tuple(A[3]), G, Tf)[0]
    rest = (tuple(map(tuple, A[:2])), frozenset(q for q in G if hd(q[0] - A[2][0], q[1] - A[2][1]) > 2 and hd(q[0] - A[3][0], q[1] - A[3][1]) > 2))
    exact = v1 == sh1 and v2 == sh2
    ok[(exact, rest in orb)] += 1
print('(vaisseaux exacts, objet revenu dans l\'orbite de X0) :', dict(ok), 'sur', len(W))
