"""S2 R-509 — bilan des vaisseaux du demi-additionneur R-337 (entrées a, b + constantes K2, K3) : quels vaisseaux sortent, où, quand.
Pour chaque cas (a,b) : simulation hx.py T = 1 200 pas, puis chaque fourmi est reconnue comme vaisseau (cap + cases) : direction r,
voie (position projetée), et instant virtuel de passage à l'origine de sa droite. Usage : python3 s2_horloge/porte_sorties.py"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, PHASES, ship_dir, rot
from exp_osc import hd
R = json.load(open('resumes/demi_additionneur_reutilisable.json'))
B = ((0, 0, 4), [(1, 0)]); A = ((30, -56, 0), [(29, -55)])
K2 = (tuple(R['K2'][0]), [tuple(c) for c in R['K2'][1]]); K3 = (tuple(R['K3'][0]), [tuple(c) for c in R['K3'][1]])
def ships(ants, g):
    out = []
    for x, y, h in ants:
        cl = frozenset((cx - x, cy - y) for cx, cy in g if hd(cx - x, cy - y) <= 2)
        out.append(PHASES.get((h, cl)))
    return out
def cas(a, b, T=1200):
    parts = [K2, K3] + ([A] if a else []) + ([B] if b else [])   # K2, K3 joués en 1er (ordre R-337), puis porte (B avant A : ordre 0)
    if a and b: parts = [K2, K3, B, A]
    ants = [list(p[0]) for p in parts]; g = {c: 1 for p in parts for c in p[1]}
    names = ['K2', 'K3'] + (['B', 'A'] if a and b else (['A'] if a else []) + (['B'] if b else []))
    for _ in range(T): step(ants, g)
    return names, ants, g, ships(ants, g)
if __name__ == '__main__':
    for a in (0, 1):
        for b in (0, 1):
            n, ants, g, s = cas(a, b)
            print('cas', (a, b), 'cases hors vaisseaux :', len(g) - sum(1 for x in s if x))
            for nm, q, sh in zip(n, ants, s):
                print('  ', nm, 'pos', q[:2], 'cap', q[2], '-> vaisseau (dir, phase)', sh, 'dep/8 pas', ship_dir(sh[0]) if sh else None)
def libre(p, T):
    ants = [list(p[0])]; g = {c: 1 for c in p[1]}
    for _ in range(T): step(ants, g)
    return ants[0]
def decalages(a, b, T=1200):
    """chaque vaisseau sortant (dir r) comparé au vaisseau entrant de même direction le plus proche, prolongé librement : écart (dx, dy)"""
    n, ants, g, s = cas(a, b, T)
    parts = {'K2': K2, 'K3': K3, 'A': A, 'B': B}
    free = {nm: (libre(parts[nm], T), PHASES_dir(parts[nm])) for nm in n}
    out = []
    for q, sh in zip(ants, s):
        cand = [(abs(q[0] - f[0][0]) + abs(q[1] - f[0][1]), nm) for nm, f in free.items() if f[1] == sh[0]]
        d, nm = min(cand); f = free[nm][0]
        out.append((sh[0], nm, (q[0] - f[0], q[1] - f[1])))
    return out
def PHASES_dir(p):
    ants = [list(p[0])]; g = {c: 1 for c in p[1]}
    return ships(ants, g)[0][0]
if __name__ == '__main__':
    print('direction de sortie, vaisseau entrant de même direction le plus proche, écart (dx, dy) à sa trajectoire libre :')
    for a in (0, 1):
        for b in (0, 1): print('  cas', (a, b), decalages(a, b))
