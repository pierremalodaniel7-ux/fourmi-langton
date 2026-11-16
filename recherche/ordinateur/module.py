"""module.py — construction d'UN module additionneur complet (cadre du module).
Retenue entrante = rayon ↗ sur la voie x+y=0 (clé (0,0)), émulé ici par un germe lointain.
Lecteur S : somme  c⊕a⊕b  -> ↘ (0) ou ↙ (1).   Lecteur K : retenue maj(c,a,b) -> ↘ (0) ou rayon ↗ exact (1).
Positions entières. Tout est vérifié par simulation complète des 8 entrées à la fin."""
import fourmis as F, construit as C, itertools, json, sys
P = F.P
T = 260000
RAY = F.germe(-400, 400, 2)            # rayon ↗ voie 0 venant de A=-800
ENTREES = list(itertools.product((0, 1), repeat=3))   # (c,a,b)

def actif(cond, e):
    c, a, b = e; v = {'c': c, 'a': a, 'b': b}
    return all(v[k] == x for k, x in cond.items())

def config(M, e, lecteurs=('S', 'K'), avec_rayon=True):
    cells, ants = [], []
    if e[0] and avec_rayon: cells += RAY[0]; ants.append(RAY[1])
    for r in lecteurs:
        R = M[r]; cells += R['seed'][0]; ants.append(R['seed'][1])
        cells += [tuple(n['cell']) for n in R['nodes'] if actif(n['cond'], e)]
    return cells, ants

def idx(M, e, r, lecteurs=('S', 'K')):
    i = 1 if (e[0]) else 0
    return i + list(lecteurs).index(r)

def sim(M, e, r, lecteurs=('S', 'K'), TT=T):
    cells, ants = config(M, e, lecteurs)
    return C.hw(cells, ants, idx(M, e, r, lecteurs), TT)

def interdit(M, r, branche):
    """cases touchées par tout ce qui n'est pas le chemin du lecteur r dans la branche"""
    autres = [x for x in M if x != r]
    out = set()
    for e in ENTREES:
        dans = all(e[i] == v for i, v in enumerate(branche))
        if dans: cells, ants = config(M, e, autres)
        else: cells, ants = config(M, e)
        F.simule(cells, ants, T, 0); out |= F.touchees()
    return out

def place_noeud(M, r, branche, cond, veut, sps=tuple(range(8, 140, 4))):
    e = tuple(list(branche) + [0] * (3 - len(branche)))
    cells, ants = config(M, e); w = idx(M, e, r)
    X = interdit(M, r, branche)
    for sp in sps:
        h, cand = C.candidats(cells, ants, w, T, 0, sp)
        if not cand: continue
        best = None
        for (x, y, u) in cand:
            if (x, y) in X: continue
            h2, _ = C.hw(cells + [(x, y)], ants, w, T, tmin=u + 2)
            if h2 is None or h2[1] != veut: continue
            ch = h2[0] - u
            if best is None or ch < best[2]: best = ((x, y), h2, ch)
        if best:
            M[r]['nodes'].append({'cell': best[0], 'cond': cond, 'br': list(branche)})
            return best
    return None

def approche(lane, Aturn, cls, avoid=set()):
    """germe ↙ sur la voie lane ; virage -> ↘ dont la classe (A mod 4, L mod 4) = cls"""
    best = None
    for dl in range(0, 8):
        for dA in range(4):
            l = lane + dl; A = Aturn + 2400 + dA; x = (l + A) // 2; y = l - x
            sc, sa = F.germe(x, y, 0)
            h, cand = C.candidats(sc, [sa], 0, 80000, 0, 600 - 25 + (dA * 0))
            for (cx, cy, u) in cand or []:
                h2, _ = C.hw(sc + [(cx, cy)], [sa], 0, 80000, tmin=u + 2)
                if not h2 or h2[1] != 3: continue
                if (h2[2][0] % 4, h2[2][1]) != cls: continue
                ch = h2[0] - u
                if best is None or ch < best[0]: best = (ch, (sc, sa), (cx, cy), h2)
    return best
