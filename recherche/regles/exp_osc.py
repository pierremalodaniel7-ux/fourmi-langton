"""Reconstruit en Python (hx.py, 2e moteur) une expérience de miroir.c : oscillateur + vaisseau (r, voie l, phase ph, ordre)."""
from hx import HX, step, run, ship, ship_dir, rot, sit, PHASES
def hd(dx, dy): return (abs(dx) + abs(dy) + abs(dx + dy)) // 2
def tdiv(a, b): return int(a / b)            # division C (vers 0)
def parse(s):
    rule, a, c = s.split('|')[:3]
    ants = [list(map(int, t.split(','))) for t in a.split(';') if t]
    cells = [tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t]
    return ants, cells
def period(ants, cells, pmax=5000):
    A = [list(a) for a in ants]; g = {c: 1 for c in cells}; g0 = dict(g); A0 = [list(a) for a in ants]
    for t in range(1, pmax + 1):
        step(A, g)
        if A == A0 and g == g0: return t
    return None
def setup(osc, r, l, ph, order, D=40):
    ants, cells = parse(osc); na = len(ants); p = period(ants, cells)
    ocx = tdiv(sum(a[0] for a in ants), na); ocy = tdiv(sum(a[1] for a in ants), na)
    A = [list(a) for a in ants]; g = {c: 1 for c in cells}; orad = 0; states = []
    for t in range(p):
        states.append(([list(a) for a in A], dict(g)))
        for a in A: orad = max(orad, hd(a[0] - ocx, a[1] - ocy))
        for c in g: orad = max(orad, hd(c[0] - ocx, c[1] - ocy))
        step(A, g)
    R = orad + 12; D = max(D, R + 20)
    TT = max(0, 8 * (2 * D + 10)); TT = TT // 8 * 8
    d = ship_dir(r); e = rot((1, 0), r)
    sp = (ocx - D * d[0] + l * e[0], ocy - D * d[1] + l * e[1])
    sa, sc = ship(r, sp)
    oa, og = states[ph]
    Ants = ([list(sa)] if order == 1 else []) + [list(a) for a in oa] + ([list(sa)] if order == 0 else [])
    G = dict(og); G[sc] = 1
    return dict(ants=Ants, g=G, T=TT, p=p, center=(ocx, ocy), R=R, states=states, ship_start=sp, D=D, na=na)
