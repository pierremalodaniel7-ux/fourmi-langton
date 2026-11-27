"""Pixel = bascule RS de R-341 : OFF = M (2 fourmis + 1 case, période 21), ON = R' (2 fourmis + 5 cases, période 12), au même endroit.
Mise à 1 = 1 vaisseau direction 0 (voie 1, M en phase 16), mise à 0 = 1 vaisseau direction 2 (voie −2, R' en phase 2) ; chacun traverse.
Ici : les deux « kits » en trajectoires, pour un pixel tourné de rho crans et centré en c."""
from traj import *
from exp_osc import setup, parse
M = "H:R2L2|0,0,1;1,-1,0|-1,1"; R2 = "H:R2L2|-1,0,3;1,1,0|-1,0;-1,1;0,-1;1,0;1,1"
def orbit(osc):
    a, c = parse(osc); A = [list(x) for x in a]; g = {x: 1 for x in c}; A0 = [list(x) for x in a]; g0 = dict(g); out = []
    while True:
        out.append((sorted(map(tuple, A)), sorted(g))); step(A, g)
        if A == A0 and g == g0: return out
ORB = {0: orbit(M), 1: orbit(R2)}
def kit(osc, r, l, ph):
    E = setup(osc, r, l, ph, 0); A = E['ants']; sh = A[-1]; oa, og = E['states'][ph]
    cells = sorted(c for c in E['g'] if c not in og)
    S = of_label(lab_piece((tuple(sh), cells), 0))
    B = [list(a) for a in A]; g = dict(E['g'])
    for _ in range(E['T']): step(B, g)
    obj = (sorted(tuple(b) for b in B[:-1]), sorted(c for c in g if hd(*c) <= 6))
    sout = (tuple(B[-1]), sorted(c for c in g if hd(*c) > 6))
    return {'S': S, 'ph': ph, 'T': E['T'], 'out': of_label(lab_piece(sout, E['T'])), 'obj': obj}
SET = kit(M, 0, 1, 16); RST = kit(R2, 2, -2, 2)
SET['fin'] = ORB[1].index(SET['obj']); RST['fin'] = ORB[0].index(RST['obj'])   # phase de l'état d'arrivée à l'instant T
def place_state(state, phase, rho, c):
    """fourmis et cases du pixel (état 0/1, phase) tourné de rho et centré en c"""
    a, g = ORB[state][phase]
    A = [(rot((x, y), rho)[0] + c[0], rot((x, y), rho)[1] + c[1], (h + rho) % 6) for x, y, h in a]
    G = [(rot(p, rho)[0] + c[0], rot(p, rho)[1] + c[1]) for p in g]
    return A, G
def read_state(ants, cells, rho, c):
    """état (0/1) et phase du pixel centré en c, ou '?'"""
    na = sorted(a for a in ants if hd(a[0] - c[0], a[1] - c[1]) <= 6); nc = sorted(p for p in cells if hd(p[0] - c[0], p[1] - c[1]) <= 6)
    for s in (0, 1):
        for ph in range(len(ORB[s])):
            A, G = place_state(s, ph, rho, c)
            if sorted(A) == na and sorted(G) == nc: return (s, ph)
    return '?'
if __name__ == '__main__':
    print('mise à 1 :', SET['S'], '->', SET['out'], 'T', SET['T'], "R' en phase", SET['fin'])
    print('mise à 0 :', RST['S'], '->', RST['out'], 'T', RST['T'], 'M en phase', RST['fin'])
    print('sortie = entrée retardée ?', [to_label(SET['S']), to_label(SET['out'])], [to_label(RST['S']), to_label(RST['out'])])
