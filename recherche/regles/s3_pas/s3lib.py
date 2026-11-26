"""S3 (26/11 soir) — bibliothèque commune : vaisseaux R2L2 décrits par leur LIGNE D'UNIVERS (entiers exacts).
Ligne d'univers d'un vaisseau = (r, gx, gy, ph) : à t = 0, c'est le germe ship(r, (gx, gy)) de hx.py avancé de ph pas (0 ≤ ph < 8).
À l'instant t : germe (gx, gy) + d_r · ((ph + t) // 8), phase (ph + t) % 8 (vrai tant que le vaisseau roule sur du blanc).
Moteurs : fourmi_r_big (copie de ../fourmi_r.c avec MAXA = 4096 au lieu de 128, rien d'autre) et hx.py (Python pur, ../hx.py).
Aucune nouvelle règle de simulation ici : seulement de la géométrie et des appels aux deux moteurs."""
import os, sys, subprocess, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from hx import ship, ship_dir, rot, step, PHASES, HX
def hd(dx, dy): return (abs(dx) + abs(dy) + abs(dx + dy)) // 2
# états du vaisseau : (r, ph) -> (fourmi relative au germe (dx, dy, cap), cases relatives au germe)
STATE = {}
for r in range(6):
    a, c = ship(r); A = [list(a)]; g = {c: 1}
    for ph in range(8):
        STATE[(r, ph)] = ((A[0][0] - a[0], A[0][1] - a[1], A[0][2]), sorted((x - a[0], y - a[1]) for (x, y) in g))
        step(A, g)
# reconnaissance : (cap, cases relatives à la fourmi) -> (r, ph)
REC = {}
for (r, ph), ((dx, dy, h), cs) in STATE.items():
    REC[(h, frozenset((x - dx, y - dy) for x, y in cs))] = (r, ph)
assert len(REC) == 48
def at(wl, t):
    """(r, gx, gy, ph) de la même ligne d'univers ramenée à l'instant t (germe et phase à t)"""
    r, gx, gy, ph = wl; n = ph + t; d = ship_dir(r); q = n // 8
    return (r, gx + d[0] * q, gy + d[1] * q, n % 8)
def norm(r, gx, gy, ph, t):
    """vaisseau vu à l'instant t avec germe (gx,gy) et phase ph -> ligne d'univers (à t = 0)"""
    d = ship_dir(r); ph0 = (ph - t) % 8; m = (ph0 + t - ph) // 8
    return (r, gx - d[0] * m, gy - d[1] * m, ph0)
def render(wl, t=0):
    """état du vaisseau à l'instant t : (fourmi (x, y, cap), [cases])"""
    r, gx, gy, ph = at(wl, t); (dx, dy, h), cs = STATE[(r, ph)]
    return (gx + dx, gy + dy, h), [(gx + x, gy + y) for x, y in cs]
def antpos(wl, t):
    r, gx, gy, ph = at(wl, t); (dx, dy, h), _ = STATE[(r, ph)]; return (gx + dx, gy + dy)
def rotwl(wl, k):
    """rotation de k crans (60°) autour de l'origine (la règle est invariante par rotation)"""
    r, gx, gy, ph = wl; X, Y = rot((gx, gy), k); return ((r + k) % 6, X, Y, ph)
def transwl(wl, v):
    r, gx, gy, ph = wl; return (r, gx + v[0], gy + v[1], ph)
def tshift(wl, s):
    """la même ligne d'univers retardée de s pas (le vaisseau passe au même endroit s pas plus tard)"""
    return at(wl, -s)
def decode(ants, cells, t):
    """liste triée des lignes d'univers (à t = 0) des vaisseaux d'un état observé à l'instant t ; None si une fourmi n'est pas un
    vaisseau propre ou s'il reste des cases non expliquées"""
    cs = set(cells); used = set(); out = []
    for x, y, h in ants:
        near = frozenset((p[0] - x, p[1] - y) for p in cs if hd(p[0] - x, p[1] - y) <= 2)
        k = REC.get((h, near))
        if k is None: return None
        r, ph = k; (dx, dy, _), _ = STATE[(r, ph)]
        out.append(norm(r, x - dx, y - dy, ph, t)); used |= {(x + a, y + b) for a, b in near}
    if cs - used: return None
    return sorted(out)
def sit(ants, cells):
    return 'H:R2L2|' + ';'.join(f'{a[0]},{a[1]},{a[2]}' for a in ants) + '|' + ';'.join(f'{c[0]},{c[1]}' for c in cells)
def sit_wls(wls):
    """situation fourmi_r à t = 0 pour une liste ordonnée (ordre de jeu) de lignes d'univers"""
    A = []; C = []
    for w in wls:
        a, cs = render(w, 0); A.append(a); C += cs
    assert len(set(C)) == len(C), 'deux vaisseaux se chevauchent à t = 0'
    return sit(A, C)
def parse(s):
    _, a, c = s.split('|')[:3]
    return [tuple(map(int, t.split(','))) for t in a.split(';') if t], [tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t]
BIG = os.path.join(HERE, 'fourmi_r_big')
def run_c(lines, T, ncpu=2):
    """moteur C : état exact après T pas pour chaque situation -> liste de (fourmis, cases)"""
    parts = [lines[i::ncpu] for i in range(ncpu)]; res = [None] * ncpu
    def w(k):
        if not parts[k]: res[k] = []; return
        o = subprocess.run([BIG, '-T', str(T), '-x', '-dump', '-lot'], input='\n'.join(parts[k]) + '\n', capture_output=True, text=True).stdout
        res[k] = [l for l in o.splitlines() if l.startswith('DUMP')]
    th = [threading.Thread(target=w, args=(k,)) for k in range(ncpu)]; [t.start() for t in th]; [t.join() for t in th]
    out = [None] * len(lines)
    for k in range(ncpu):
        assert len(res[k]) == len(parts[k]), 'moteur C : sortie incomplète'
        for j, l in enumerate(res[k]): out[k + j * ncpu] = parse(l.split(' ', 1)[1])
    return out
def run_py(s, T):
    """2e moteur : hx.py (Python pur)"""
    a, c = parse(s); A = [list(t) for t in a]; G = {tuple(t[:2]): 1 for t in c}
    for _ in range(T): step(A, G)
    return [tuple(t) for t in A], sorted(G)
