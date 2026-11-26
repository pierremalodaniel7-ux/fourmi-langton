"""Trajectoires de vaisseaux libres, forme (r, gx, gy, τ) : au temps τ le vaisseau est en phase 0 avec sa position de référence g ;
(g, τ) ~ (g + d_r, τ + 8). Opérations exactes (entiers) : rotation, translation, retard. Un choc du catalogue = 2 entrées, 2 sorties,
un ordre de jeu, un lieu et un instant ; on le transforme en bloc."""
from lib4 import *
D = [ship_dir(r) for r in range(6)]
def norm(T):
    r, x, y, t = T; n = t // 8
    return (r, x - n * D[r][0], y - n * D[r][1], t - 8 * n)
def of_label(L):
    r, l, a, ph = dec_of(L, 0); X, Y = (l + a) // 2, (l - a) // 2; g = rot((X, Y), r)
    return norm((r, g[0], g[1], -ph))
def to_label(T):
    r, x, y, t = norm(T)
    # au temps t : phase 0, référence g -> abscisse / voie
    X, Y = rot((x, y), -r % 6); l, a = X + Y, X - Y
    return (r, l, 4 * a + 0 - t)
def rotT(T, k):
    r, x, y, t = T; X, Y = rot((x, y), k); return norm(((r + k) % 6, X, Y, t))
def movT(T, v=(0, 0), dt=0):
    r, x, y, t = T; return norm((r, x + v[0], y + v[1], t + dt))
def same(T1, T2): return norm(T1) == norm(T2)
def piece_at(T, t=0):
    return piece(to_label(T), t)
def sit_of(Ts, t=0):
    return situation([to_label(T) for T in Ts], t)
class Choc:
    """ins = [traj fourmi B, traj fourmi A], outs = [sortie de B, sortie de A], first = indice (0 = B, 1 = A) de la fourmi jouée en 1er,
    lieu p et instant te"""
    def __init__(self, ins, outs, first, p=(0, 0), te=200):
        self.ins, self.outs, self.first, self.p, self.te = ins, outs, first, p, te
    def rot(self, k):
        return Choc([rotT(T, k) for T in self.ins], [rotT(T, k) for T in self.outs], self.first, rot(self.p, k), self.te)
    def mov(self, v=(0, 0), dt=0):
        return Choc([movT(T, v, dt) for T in self.ins], [movT(T, v, dt) for T in self.outs], self.first, (self.p[0] + v[0], self.p[1] + v[1]), self.te + dt)
    def align(self, i, X, n=0, side='ins'):
        """tourne et déplace le choc pour que son entrée i (ou sa sortie i si side = 'outs') suive exactement la trajectoire X
        (glissé de n périodes le long de X)"""
        C = self.rot((X[0] - getattr(self, side)[i][0]) % 6); Ti = getattr(C, side)[i]
        dx, dy, dt = X[1] - Ti[1], X[2] - Ti[2], X[3] - Ti[3]
        d = D[X[0]]
        C = C.mov((dx + n * d[0], dy + n * d[1]), dt + 8 * n)
        assert same(getattr(C, side)[i], X)
        return C
def catalogue(deflect_only=True):
    import json
    cat = json.load(open(HERE + '/data/chocs.json')); out = []
    for c in cat:
        LB, LA, oB, oA = (tuple(c[k]) for k in ('LB', 'LA', 'oB', 'oA'))
        if deflect_only and (oB[0] in (LB[0], LA[0]) or oA[0] in (LB[0], LA[0])): continue
        out.append(Choc([of_label(LB), of_label(LA)], [of_label(oB), of_label(oA)], 0 if c['ordre'] == 0 else 1))
    return out
