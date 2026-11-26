#!/usr/bin/env python3
"""R-343 Certificat : la bascule RS de R-341 supporte un nombre QUELCONQUE de cycles « mise à 1 puis mise à 0 ».
Cycle 0 : M (phase 0 à t = 0) ; mise à 1 à es (M en phase ph1), mise à 0 à er (R' en phase ph2) ; on choisit la durée P du cycle pour que
M soit de nouveau en phase 0 à t = P (contrôlé par simulation : objet à t = P = objet à t = 0). Le cycle j est la copie décalée de j·P.
Par récurrence, chaque cycle se déroule à l'identique SI aucun vaisseau d'un cycle ne passe à ≤ 6 d'un vaisseau d'un autre cycle (calcul exact
sur toute la droite des temps, vaisseaux rectilignes hors de leur cycle) et si, hors de son propre cycle, aucun vaisseau ne passe à ≤ 9 du
centre (l'objet tient dans un rayon 3). Usage : python3 bascule_certif.py [J]"""
import sys, json, itertools
from hx import step
from exp_osc import hd, parse
_argv = sys.argv; sys.argv = [_argv[0], '0', '2']
import bascule_demo as bd
sys.argv = _argv
J = int(sys.argv[1]) if len(sys.argv) > 1 else 10
X = json.load(open('data/bascules_RS.json'))[0]
R = X['R']; K1, K2 = bd.K1, bd.K2; OR, OR2 = bd.OR, bd.OR2
ph1, T1, ph2, T2 = bd.ph1, bd.T1, bd.ph2, bd.T2
es = next(e for e in range(0, 200) if e % len(OR) == ph1)
er = next(e for e in range(es + T1, es + T1 + 200) if (bd.i_end1 + e - (es + T1)) % len(OR2) == ph2)
P = next(p for p in range(er + T2 + 1600, er + T2 + 1700) if (bd.i_end2 + p - (er + T2)) % len(OR) == 0)
a0, c0 = parse(R)
def cycle_traj(W):
    """objet + 2 vaisseaux du cycle 0, positions à chaque pas de 0 à W"""
    A = [list(x) for x in a0]; g = {c: 1 for c in c0}; idx = []
    for Kt, e in ((K1, es), (K2, er)):
        a, gg = bd.backx(Kt, e); idx.append(len(A)); A += a; g.update(gg)
    Pp = [[tuple(x[:2]) for x in A]]
    snap = None
    for t in range(W):
        if t == P: snap = ([list(x) for x in A], dict(g))
        step(A, g); Pp.append([tuple(x[:2]) for x in A])
    return snap[0], snap[1], Pp, idx
A, g, Pp, idx = cycle_traj(P + 8)
objP = (sorted(tuple(x) for x in A if hd(x[0], x[1]) <= 8), sorted(c for c in g if hd(*c) <= 8))
print(f'cycle : es = {es}, er = {er}, P = {P} ; objet à t = P identique à t = 0 : {objP == OR[0]}')
assert objP == OR[0]
# trajectoires exactes des 2 vaisseaux du cycle 0 pour tout t (rectilignes avant 0 et après P)
W = P
def mk(i):
    vin = (Pp[8][i][0] - Pp[0][i][0], Pp[8][i][1] - Pp[0][i][1]); vout = (Pp[W + 8][i][0] - Pp[W][i][0], Pp[W + 8][i][1] - Pp[W][i][1])
    assert all(Pp[t + 8][i] == (Pp[t][i][0] + vin[0], Pp[t][i][1] + vin[1]) for t in range(0, 64))
    assert all(Pp[t + 8][i] == (Pp[t][i][0] + vout[0], Pp[t][i][1] + vout[1]) for t in range(W - 64, W))
    def pos(t):
        if t < 0: m = (-t + 7) // 8; tt = t + 8 * m; return (Pp[tt][i][0] - m * vin[0], Pp[tt][i][1] - m * vin[1])
        if t > W + 8:
            m = (t - W) // 8; tt = t - 8 * m
            if tt > W + 8: tt -= 8; m += 1
            return (Pp[tt][i][0] + m * vout[0], Pp[tt][i][1] + m * vout[1])
        return Pp[t][i]
    return pos, vin, vout
S = [mk(i) for i in idx]
# (b) hors de son cycle, un vaisseau reste à > 9 du centre
far_out = min(min(hd(*S[k][0](t)) for t in list(range(-4000, 0)) + list(range(P, P + 4000))) for k in range(2))
print('distance minimale au centre hors du cycle :', far_out)
# (a) vaisseaux du cycle 0 contre vaisseaux du cycle j
worst = 10 ** 9
for j in range(1, J + 1):
    d = 10 ** 9
    for (p1, v1, w1), (p2, v2, w2) in itertools.product(S, S):
        for t in range(-200, P + j * P + 4000):
            a, b = p1(t), p2(t - j * P); d = min(d, hd(a[0] - b[0], a[1] - b[1]))
    worst = min(worst, d)
    if j <= 3 or j == J: print(f'écart de {j} cycle(s) : distance minimale entre vaisseaux = {d}')
ok = worst > 6 and far_out > 9
print('CERTIFIÉ' if ok else 'à examiner', f'(distance ≥ {worst} entre cycles, ≥ {far_out} du centre hors cycle)')
json.dump({'es': es, 'er': er, 'P': P, 'distance_min': worst, 'centre_hors_cycle': far_out, 'certifie': ok}, open('resumes/bascule_certif.json', 'w'))
