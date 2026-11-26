#!/usr/bin/env python3
"""R-338 Certificat : le demi-additionneur R-337 marche pour TOUT nombre d'usages et TOUTE suite d'entrées (usages espacés de k périodes).
Principe : si, pour deux usages quelconques u < v, aucune fourmi de u ne passe jamais à distance ≤ 6 d'une fourmi de v (trajectoires
calculées pour chaque usage SEUL), alors personne ne voit jamais un autre usage (les cases noires d'un vaisseau sont à ≤ 2 de sa fourmi,
et le circuit ne laisse aucune case) : l'évolution de N usages est exactement la superposition des usages seuls, et chaque usage donne la
bonne sortie (4 cas vérifiés). Les trajectoires seules sont exactes pour tout t : hors de la fenêtre simulée, chaque fourmi est un vaisseau
sur du blanc, donc pos(t + 8) = pos(t) + d exactement (en avant comme en arrière).
Distance entre usage 0 (entrées e1) et usage j (entrées e2, décalé de j·k·8 pas) : on calcule la distance minimale EXACTE sur toute la
droite des temps (morceaux rectilignes : minimum d'une fonction de t affine par morceaux sur chaque classe de t mod 8).
Usage : python3 demi_add_certif.py [k]"""
import sys, json, itertools
from hx import step, rot
from exp_osc import hd
from demi_add_z import usage_parts
k = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 200
g = json.load(open('resumes/demi_additionneur_reutilisable.json'))
gg = {'K2sit': g['K2'], 'K3sit': g['K3'], 'K2': [None] * 5 + [g['ordre_K2']], 'K3': [None] * 4 + [g['ordre_K3']]}
W = 4000                                  # fenêtre simulée [0, W] ; avant 0 et après W : vaisseaux en ligne droite (vérifié ci-dessous)
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
def traj(ab):
    ants, cells = usage_parts(gg, ab[0], ab[1], 0, k)
    A = [list(a) for a in ants]; G = {c: 1 for c in cells}
    P = [[tuple(a[:2]) for a in A]]
    for t in range(W + 8):
        step(A, G); P.append([tuple(a[:2]) for a in A])
    # vitesses aux deux bouts (déplacement sur 8 pas), et contrôle : périodicité exacte aux bouts
    vin = [(P[8][i][0] - P[0][i][0], P[8][i][1] - P[0][i][1]) for i in range(len(A))]
    vout = [(P[W + 8][i][0] - P[W][i][0], P[W + 8][i][1] - P[W][i][1]) for i in range(len(A))]
    return P, vin, vout
def pos(T, t, i):
    P, vin, vout = T
    if t < 0:
        m = (-t + 7) // 8; tt = t + 8 * m; return (P[tt][i][0] - m * vin[i][0], P[tt][i][1] - m * vin[i][1])
    if t > W + 8:
        m = (t - W) // 8; tt = t - 8 * m
        if tt > W + 8: tt -= 8; m += 1
        return (P[tt][i][0] + m * vout[i][0], P[tt][i][1] + m * vout[i][1])
    return P[t][i]
TR = {ab: traj(ab) for ab in CASES}
# contrôle des bouts : la fourmi est bien un vaisseau périodique avant 0 et après W (on compare les 8 derniers pas à pos(t) extrapolé)
for ab, T in TR.items():
    P, vin, vout = T
    for i in range(len(P[0])):
        assert all(P[t + 8][i] == (P[t][i][0] + vout[i][0], P[t][i][1] + vout[i][1]) for t in range(W - 64, W)), ('sortie', ab, i)
        assert all(P[t + 8][i] == (P[t][i][0] + vin[i][0], P[t][i][1] + vin[i][1]) for t in range(0, 64)), ('entrée', ab, i)
def mind(T1, T2, shift):
    """distance minimale sur tous les temps entre les fourmis de T1(t) et de T2(t − shift)"""
    best = 10 ** 9
    n1, n2 = len(T1[0][0]), len(T2[0][0])
    lo = min(0, shift) - 8; hi = max(W, W + shift) + 16
    for t in range(lo, hi):                       # fenêtre où l'un des deux n'est pas rectiligne (+ bords)
        for i in range(n1):
            p = pos(T1, t, i)
            for j in range(n2):
                q = pos(T2, t - shift, j); d = hd(p[0] - q[0], p[1] - q[1])
                if d < best: best = d
    # hors fenêtre : mouvements rectilignes de période 8 : sur chaque classe t mod 8, la différence est affine en m ; on vérifie que la
    # distance croît des deux côtés (dérivée de la différence non nulle et qui éloigne), sinon on prolonge
    for side in (-1, 1):
        for i in range(n1):
            for j in range(n2):
                t0 = lo if side < 0 else hi
                d0 = hd(*(lambda p, q: (p[0] - q[0], p[1] - q[1]))(pos(T1, t0, i), pos(T2, t0 - shift, j)))
                d1 = hd(*(lambda p, q: (p[0] - q[0], p[1] - q[1]))(pos(T1, t0 + side * 800, i), pos(T2, t0 + side * 800 - shift, j)))
                v1 = (T1[2] if side > 0 else T1[1])[i]; v2 = (T2[2] if t0 - shift > W else T2[1] if t0 - shift < 0 else (0, 0))[j]
                if v1 == v2 and (t0 - shift > W + 8 or t0 - shift < 0): continue     # même vitesse : distance constante (= d0, déjà comptée)
                if d1 <= d0:      # ne s'éloignent pas encore : on balaie plus loin jusqu'à ce qu'ils s'éloignent
                    t = t0
                    for _ in range(20000):
                        t += side * 8
                        p, q = pos(T1, t, i), pos(T2, t - shift, j); d = hd(p[0] - q[0], p[1] - q[1]); best = min(best, d)
                        p2, q2 = pos(T1, t + side * 800, i), pos(T2, t + side * 800 - shift, j)
                        if hd(p2[0] - q2[0], p2[1] - q2[1]) > d: break
                    else: return -1
    return best
K8 = k * 8
res = {}; worst = 10 ** 9
J = int(sys.argv[2]) if len(sys.argv) > 2 else 12
for jj in range(1, J + 1):
    for e1, e2 in itertools.product(CASES, CASES):
        d = mind(TR[e1], TR[e2], jj * K8); res[(jj, e1, e2)] = d; worst = min(worst, d)
    print(f'écart de {jj} usage(s) : distance minimale entre fourmis de 2 usages = {min(res[(jj, a, b)] for a, b in itertools.product(CASES, CASES))}')
    sys.stdout.flush()
# au-delà de J : un usage j > J n'a, pendant toute la vie « non rectiligne » de l'usage 0, que des vaisseaux en approche très loin ;
# et deux routes rectilignes (sortie de l'usage 0, entrée de l'usage j) ne peuvent se rapprocher que si elles sont sur le même axe en sens
# opposés à moins de 6 voies (sinon leur distance au point de croisement grandit avec j) : on liste ces paires.
def droite(T, i, out):
    P, vin, vout = T; v = vout[i] if out else vin[i]; p = P[W][i] if out else P[0][i]
    r = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)].index(v)
    X, Y = rot(p, -r % 6); return r, X + Y
sorties = {droite(TR[ab], i, True) for ab in CASES for i in range(len(TR[ab][0][0]))}
entrees = {droite(TR[ab], i, False) for ab in CASES for i in range(len(TR[ab][0][0]))}
fronts = [(s, e) for s in sorties for e in entrees if (s[0] - e[0]) % 6 == 3 and abs(s[1] + e[1]) <= 6]
print('paires (sortie, entrée) sur le même axe, en sens opposés, à ≤ 6 voies :', fronts)
print('distance minimale sur tous les écarts 1 …', J, ':', worst, '→', 'CERTIFIÉ (> 6)' if worst > 6 and not fronts else 'à examiner')
json.dump({'k': k, 'J': J, 'distance_min': worst, 'fronts': fronts}, open('resumes/demi_add_certif.json', 'w'))
