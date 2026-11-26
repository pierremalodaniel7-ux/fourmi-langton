"""R-345 Enchaîner deux circuits : le circuit 2 est tourné de rho crans, avancé de tau pas et translaté pour qu'une de ses pièces d'entrée
suive EXACTEMENT la route et l'horaire d'une sortie du circuit 1 (vaisseau décodé au temps Tref). Positions entières, calcul exact."""
from fa_lib import *
from circuit import *
from hx import rot, step
def advance(piece, tau):
    (x, y, h), cs = piece; A_ = [[x, y, h]]; G = {tuple(c): 1 for c in cs}
    for _ in range(tau): step(A_, G)
    return (tuple(A_[0]), sorted(G))
def rotate(piece, rho):
    (x, y, h), cs = piece; X, Y = rot((x, y), rho)
    return ((X, Y, (h + rho) % 6), [rot(tuple(c), rho) for c in cs])
def translate(piece, v):
    (x, y, h), cs = piece
    return ((x + v[0], y + v[1], h), [(c[0] + v[0], c[1] + v[1]) for c in cs])
def frame(target, Tref, P):
    """(tau, v) tels que translate(advance(P, tau), v) soit à l'instant Tref dans l'état du vaisseau target = (r, voie, abscisse, phase).
    P : pièce-vaisseau (déjà tournée) de même direction. None si impossible (parité)."""
    r, lt, at, pht = target
    d0 = decode([P[0]], P[1])[0]
    assert d0[0] == r, (d0, target)
    tau = (pht - d0[3]) % 8
    P1 = advance(P, tau); d1 = decode([P1[0]], P1[1])[0]
    assert d1[3] == pht
    assert Tref % 8 == 0
    dl = lt - d1[1]; da = at - d1[2] - 2 * (Tref // 8)
    if (dl + da) % 2: return None
    v = rot(((dl + da) // 2, (dl - da) // 2), r)
    return tau, v
def attach(C2, name, rho, target, Tref):
    """nouveau Circuit = C2 tourné de rho, avancé et translaté pour que la pièce `name` suive target ; la pièce garde son entrée
    (on la retire ensuite si elle est fournie par le circuit 1)."""
    rp = [(n, rotate(p, rho), v) for n, p, v in C2.pieces]
    P = dict((n, p) for n, p, v in rp)[name]
    fr = frame(target, Tref, P)
    if fr is None: return None
    tau, v = fr
    return Circuit([(n, translate(advance(p, tau), v), var) for n, p, var in rp])
