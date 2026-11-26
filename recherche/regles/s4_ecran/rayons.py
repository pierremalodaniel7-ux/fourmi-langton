"""Rayons (demi-droites parcourues par les vaisseaux d'un usage) et distances exactes en entiers.
Un usage = pièces d'entrée (trajectoires) + issues par cas (trajectoires sortantes). Un rayon d'entrée est parcouru pour t ≤ t_in,
un rayon de sortie pour t ≥ t_out (instants approchés par excès : on prend les instants des chocs, marge comprise)."""
from traj import *
def pos_line(T, t0, t1, stride=8):
    return [antpos(to_label(T), t) for t in range(t0, t1, stride)]
def dist_point_ray(P, T, t0, t1):
    """distance minimale (fourmi) entre le point P et la trajectoire T sur [t0, t1] (pas de 1 : exact)"""
    L = to_label(T); return min(hdist(antpos(L, t), P) for t in range(t0, t1))
def head_on(outs, ins):
    """paires (sortie, entrée) sur le même axe en sens opposés à ≤ 6 voies (critère de R-338)"""
    bad = []
    for s in outs:
        ls = to_label(s)
        for e in ins:
            le = to_label(e)
            if (ls[0] - le[0]) % 6 == 3 and abs(ls[1] + le[1]) <= 6: bad.append((s, e))
    return bad
