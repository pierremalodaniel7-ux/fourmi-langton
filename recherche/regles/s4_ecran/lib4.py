"""S4 écran (26/11 soir) — outils communs. Tout est en entiers.
ÉTIQUETTE d'un vaisseau libre = (r, voie, V) : r = direction, voie = voie de sa route, V = 4·abscisse + phase − t (constante le
long du vol : la phase avance de 1 par pas et l'abscisse de 2 par période de 8 pas). Une étiquette décrit TOUTE la trajectoire
(dans le vide). On transforme une étiquette par rotation (crans de 60° autour de l'origine), translation et décalage de temps.
Réutilise : hx.py (2e moteur Python), fa_lib.py (decode, lotdump = fourmi_r en lot sur 2 cœurs), demi_add_k.py (OFFS, lane)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.dirname(HERE)
os.chdir(REG); sys.path.insert(0, REG)
from hx import step, rot, ship, ship_dir, PHASES, sit as hsit
from fa_lib import decode, lotdump, parts_of, pyrun
from demi_add_k import OFFS, lane, fmt
from exp_osc import hd
def along(x, y, r):
    X, Y = rot((x, y), -r % 6); return X - Y
def lab_of(dec, t):
    """dec = (r, voie, abscisse, phase) décodé au temps t -> étiquette"""
    r, l, a, ph = dec; return (r, l, 4 * a + ph - t)
def dec_of(L, t):
    r, l, V = L; u = V + t; p = l % 2
    a = 2 * ((u - 4 * p) // 8) + p; ph = u - 4 * a
    assert 0 <= ph < 8
    return (r, l, a, ph)
def piece(L, t=0):
    """pièce-vaisseau ((x, y, cap), [cases]) dans l'état de l'étiquette L au temps t"""
    r, l, a, ph = dec_of(L, t)
    X, Y = (l + a) // 2, (l - a) // 2
    g = rot((X, Y), r); (x, y, h), c = ship(r, g)
    A = [[x, y, h]]; G = {c: 1}
    for _ in range(ph): step(A, G)
    return (tuple(A[0]), sorted(G))
def lab_piece(p, t=0):
    d = decode([p[0]], p[1]); assert d, p
    return lab_of(d[0], t)
def antpos(L, t):
    r, l, a, ph = dec_of(L, t); X, Y = (l + a) // 2, (l - a) // 2
    g = rot((X, Y), r); o = OFFS[(r, ph)]
    return (g[0] + o[0], g[1] + o[1])
def transform(L, rho=0, v=(0, 0), delta=0):
    """rotation de rho crans autour de l'origine, puis translation v, puis tout retardé de delta pas"""
    (x, y, h), cs = piece(L, 0)
    X, Y = rot((x, y), rho); cs = [rot(c, rho) for c in cs]
    p = ((X + v[0], Y + v[1], (h + rho) % 6), [(c[0] + v[0], c[1] + v[1]) for c in cs])
    r, l, Vv = lab_piece(p, 0)
    return (r, l, Vv - delta)
def slide(L, d_r, k):
    """même trajectoire de référence translatée de k·d (d = direction d_r) et retardée de 8k : ce que devient une pièce d'un choc
    qu'on fait glisser de k périodes le long de la route de direction d_r"""
    d = ship_dir(d_r); return transform(L, 0, (k * d[0], k * d[1]), 8 * k)
def situation(labels, t=0):
    """situation fourmi_r (ordre de jeu = ordre de la liste) à l'instant t"""
    P = [piece(L, t) for L in labels]
    return fmt([p[0] for p in P], [c for p in P for c in p[1]])
def labels_at(ants, cells, t):
    d = decode(ants, cells)
    if d is None: return None
    return sorted(lab_of(x, t) for x in d)
def hdist(p, q): return hd(p[0] - q[0], p[1] - q[1])
def closest(L1, L2, t0, t1, stepn=1):
    """distance minimale entre les fourmis de deux trajectoires libres sur [t0, t1]"""
    return min((hdist(antpos(L1, t), antpos(L2, t)), t) for t in range(t0, t1, stepn))
