"""Outils hexa R2L2 (nuit 26/11) : simulation exacte en entiers (2e moteur Python, indépendant de fourmi_r),
vaisseau, rotations. Conventions de fourmi_r : axiales, caps 0=E(1,0) 1=SE(0,1) 2=SO(-1,1) 3=O(-1,0) 4=NO(0,-1) 5=NE(1,-1) ;
blanc (0) → cap+2, noir (1) → cap+4 ; fourmis jouées l'une après l'autre (ordre de la liste)."""
HX = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
K = (2, 4)
def rot(v, r):
    """rotation de r crans de 60° (sens des caps) d'un vecteur axial"""
    x, y = v
    for _ in range(r % 6): x, y = -y, x + y
    return (x, y)
assert rot((1, 0), 1) == (0, 1) and rot((1, 0), 6) == (1, 0)
def step(ants, g):
    """un tour : chaque fourmi joue une fois, dans l'ordre. ants = liste de [x,y,h], g = dict case -> couleur (1 = noir)"""
    for a in ants:
        p = (a[0], a[1]); c = g.get(p, 0)
        a[2] = (a[2] + K[c]) % 6
        if c: del g[p]
        else: g[p] = 1
        a[0] += HX[a[2]][0]; a[1] += HX[a[2]][1]
def run(ants, cells, T):
    ants = [list(a) for a in ants]; g = {tuple(c): 1 for c in cells}
    for _ in range(T): step(ants, g)
    return ants, g
# vaisseau R-306 : fourmi (0,0) cap 4 + case (1,0) ; part en (1,-1) toutes les 8 étapes
SHIP = ((0, 0, 4), (1, 0))
def ship(r=0, pos=(0, 0)):
    """vaisseau tourné de r crans, translaté en pos : (fourmi, case)"""
    (x, y, h), c = SHIP
    cx, cy = rot(c, r)
    return (pos[0], pos[1], (h + r) % 6), (pos[0] + cx, pos[1] + cy)
def ship_dir(r): return rot((1, -1), r)
def sit(ants, cells):
    """situation au format fourmi_r"""
    return 'H:R2L2|' + ';'.join(f'{a[0]},{a[1]},{a[2]}' for a in ants) + '|' + ';'.join(f'{c[0]},{c[1]}' for c in cells)
# les 8 phases du vaisseau (direction r) : (cap, cases noires - position fourmi) -> (r, phase)
PHASES = {}
for r in range(6):
    a, c = ship(r)
    ants, g = [list(a)], {c: 1}
    for ph in range(8):
        PHASES[(ants[0][2], frozenset((cx - ants[0][0], cy - ants[0][1]) for cx, cy in g))] = (r, ph)
        step(ants, g)
    assert (ants[0][0] - a[0], ants[0][1] - a[1]) == ship_dir(r), r
assert len(PHASES) == 48
def reverse(ants, g):
    """gomme collective (R-311) : chaque fourmi revient sur la case qu'elle vient de quitter, cap retourné ; ordre de jeu inversé.
    Rejouer autant de tours défait exactement l'histoire (les fourmis finissent retournées)."""
    out = []
    for a in reversed(ants):
        x, y, h = a; dx, dy = HX[h]
        out.append([x - dx, y - dy, (h + 3) % 6])
    return out, dict(g)
if __name__ == '__main__':
    import random
    random.seed(3)
    for _ in range(20):    # test de la gomme collective sur des situations au hasard
        A0 = [[random.randint(-3, 3), random.randint(-3, 3), random.randint(0, 5)] for _ in range(3)]
        C0 = {(random.randint(-3, 3), random.randint(-3, 3)): 1 for _ in range(4)}
        a, g = run(A0, C0, 300); ra, rg = reverse(a, g)
        for _ in range(300): step(ra, rg)
        back = [[x + HX[(h + 3) % 6][0], y + HX[(h + 3) % 6][1], (h + 3) % 6] for x, y, h in reversed(ra)]
        assert rg == C0 and back == A0, (A0, C0)
    print('gomme collective : 20/20')
