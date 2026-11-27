"""S1 : premier instant où la simulation commune s'écarte de la réunion des deux sous-systèmes (hx.py), et fourmis en cause."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from hx import step
from exp_osc import hd
def diverge(P1, P2, Tmax, order):
    """P1, P2 : listes de pièces (fourmi, cases) ; order : liste des pièces du système commun dans l'ordre de jeu (même objets)"""
    def mk(P):
        A = [list(p[0]) for p in P]; G = {}
        for p in P:
            for c in p[1]: G[tuple(c)] = 1
        return A, G
    A1, G1 = mk(P1); A2, G2 = mk(P2); A, G = mk(order)
    idx = [ (0, P1.index(p)) if p in P1 else (1, P2.index(p)) for p in order]
    for t in range(Tmax):
        step(A1, G1); step(A2, G2); step(A, G)
        exp = [A1[j] if s == 0 else A2[j] for s, j in idx]
        if exp != A:
            md = min((hd(a[0] - b[0], a[1] - b[1]), i, j) for i, a in enumerate(A1) for j, b in enumerate(A2))
            return t + 1, md, [i for i in range(len(A)) if exp[i] != A[i]]
    return None
def close(P1, P2, Tmax, skip1=(), skip2=(), lim=3):
    """rencontres (distance ≤ lim) entre fourmis de deux systèmes simulés SÉPARÉMENT (hors indices skip) : liste (t, d, i, j)"""
    def mk(P):
        A = [list(p[0]) for p in P]; G = {}
        for p in P:
            for c in p[1]: G[tuple(c)] = 1
        return A, G
    A1, G1 = mk(P1); A2, G2 = mk(P2); ev = []
    for t in range(Tmax):
        step(A1, G1); step(A2, G2)
        for i, a in enumerate(A1):
            if i in skip1: continue
            for j, b in enumerate(A2):
                if j in skip2: continue
                d = hd(a[0] - b[0], a[1] - b[1])
                if d <= lim: ev.append((t + 1, d, i, j))
    return ev
