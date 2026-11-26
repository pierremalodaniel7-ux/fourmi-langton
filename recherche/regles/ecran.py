#!/usr/bin/env python3
"""R-335 Écran et mémoire R2L2 avec un pixel dont l'état OFF est VIDE.
Pixel ON = oscillateur O2 = « H:R2L2|0,0,3;1,0,0|1,0;-1,1 » (2 fourmis + 2 cases, période 3, son propre renversé) ; OFF = rien du tout.
Destruction PROPRE (miroir.c, DES, 0 case restante) : 1 vaisseau → 3 vaisseaux. ÉCRIRE = film inversé d'une destruction Da (3 vaisseaux
convergent, O2 apparaît, 1 vaisseau repart) ; EFFACER / LIRE = une destruction Db (si le pixel est OFF le vaisseau-sonde traverse du
vide : rien ne change ; s'il est ON, O2 part en 3 vaisseaux : la lecture « 1 » = un vaisseau qui sort dans une direction donnée).
Usage : python3 ecran.py choix        → essaie toutes les paires (Da, Db) sur la démo écran et la démo mémoire
        python3 ecran.py demo i j     → rejoue la paire choisie, 2 moteurs, écrit resumes/ecran.json"""
import sys, json, subprocess, itertools
from hx import step, rot, sit, reverse, PHASES, ship_dir
from exp_osc import setup, hd
O2 = "H:R2L2|0,0,3;1,0,0|1,0;-1,1"
OPTS = sorted({tuple(int(kv.split('=')[1]) for kv in l.split()[3:7]) for l in open('data/des2b_0.txt') if O2 in l})  # (ord, r, l, ph)
def film(o, r, l, ph):
    E = setup(O2, r, l, ph, o); assert E['center'] == (0, 0)
    A, g = [list(a) for a in E['ants']], dict(E['g'])
    sh = A[-1] if o == 0 else A[0]
    kit = ([list(sh)], {c: 1 for c in g if c not in E['states'][ph][1]})
    for _ in range(E['T']): step(A, g)
    return E, kit, (A, g)
def ships_of(A, g):
    out = []
    for a in A:
        near = frozenset((p[0] - a[0], p[1] - a[1]) for p in g if hd(p[0] - a[0], p[1] - a[1]) <= 2)
        out.append(PHASES.get((a[2], near)))
    return out
def back(ants, g, s):
    assert s % 8 == 0
    out = []; G = {}
    for a in ants:
        cs = [p for p in g if hd(p[0] - a[0], p[1] - a[1]) <= 2]
        B = [list(a)]; gg = {p: 1 for p in cs}
        for _ in range(8): step(B, gg)
        d = (B[0][0] - a[0], B[0][1] - a[1]); k = s // 8
        out.append([a[0] - k * d[0], a[1] - k * d[1], a[2]])
        for p in cs: G[(p[0] - k * d[0], p[1] - k * d[1])] = 1
    return out, G
def tr(kit, P, k=0):
    """kit tourné de k crans (60°) autour de l'origine puis translaté en P"""
    A = []
    for x, y, h in kit[0]: X, Y = rot((x, y), k); A.append([X + P[0], Y + P[1], (h + k) % 6])
    return A, {(lambda v: (v[0] + P[0], v[1] + P[1]))(rot(c, k)): 1 for c in kit[1]}
class Pair:
    def __init__(self, da, db):
        self.da, self.db = da, db
        Ea, _, fa = film(*da); self.CREATE = reverse(*fa); self.TC = Ea['T']
        # état créé (phase) : on rejoue le kit seul
        A, g = [list(a) for a in self.CREATE[0]], dict(self.CREATE[1])
        for _ in range(self.TC): step(A, g)
        self.created = (sorted(tuple(a) for a in A if hd(*a[:2]) <= 6), sorted(p for p in g if hd(*p) <= 6))
        self.ok_create = sum(1 for a in A if hd(*a[:2]) <= 6) == 2 and all(hd(*p) <= 6 or any(hd(p[0]-a[0], p[1]-a[1]) <= 2 for a in A) for p in g)
        Eb, self.ERASE, fb = film(*db); self.TE = Eb['T']; self.PH_E = db[3]; self.states = Eb['states']
        self.ph_created = next((k for k, (sa, sg) in enumerate(self.states) if sorted(map(tuple, sa)) == self.created[0] and sorted(sg) == self.created[1]), None)
        self.read_dirs = sorted(s[0] for s in ships_of(*fb) if s)      # directions des 3 vaisseaux d'une lecture « 1 »
        self.probe_dir = db[1]
    def t_erase(self, t_create, tmin):
        e = (tmin + 7) // 8 * 8
        while (e - (t_create + self.TC) + self.ph_created) % 3 != self.PH_E: e += 8
        return e
    def lire(self, A, g, P):
        na = sorted((a[0] - P[0], a[1] - P[1], a[2]) for a in A if hd(a[0] - P[0], a[1] - P[1]) <= 6)
        nc = sorted((p[0] - P[0], p[1] - P[1]) for p in g if hd(p[0] - P[0], p[1] - P[1]) <= 6)
        if not na and not nc: return 'OFF'
        for k in range(6):
            for sa, sg in self.states:
                ra, rg = tr((sa, sg), (0, 0), k)
                if na == sorted(map(tuple, ra)) and nc == sorted(rg): return 'ON' if k == 0 else 'ON%d' % k
        return '?'
def simulate(ants, cells, checks, TEND, P):
    """checks : liste (t, fonction(A, g) -> valeur) ; renvoie les valeurs + état final"""
    A = [list(a) for a in ants]; g = dict(cells); t = 0; vals = []
    for ts, f in sorted(checks, key=lambda c: c[0]):
        while t < ts: step(A, g); t += 1
        vals.append(f(A, g))
    while t < TEND: step(A, g); t += 1
    return vals, A, g
def build(pair, plan):
    """pose les kits ; une sonde « ord = 1 » doit jouer AVANT les fourmis de l'objet : on l'insère avant le kit qui l'a écrit"""
    ants, cells = [], {}; last = {}
    for ev in plan:
        kind, P, s = ev[:3]; k = ev[3] if len(ev) > 3 else 0
        a, g = back(*tr(pair.CREATE if kind == 'écrit' else pair.ERASE, P, k), s); cells.update(g)
        if kind == 'écrit': last[P] = len(ants); ants += a
        elif pair.db[0] == 1 and P in last:
            i = last[P]; ants[i:i] = a
            for q in last:
                if last[q] >= i and q != P: last[q] += len(a)
        else: ants += a
    return ants, cells
def screen(pair, P1=(0, 0), P2=(40, 20), G=1600, k1=0, k2=0, k3=0):
    plan = [('écrit', P1, 0, k1), ('efface', P1, pair.t_erase(0, G), k1), ('écrit', P2, G, k2), ('efface', P2, pair.t_erase(G, 2 * G), k2), ('écrit', P1, 2 * G, k3)]
    ants, cells = build(pair, plan)
    SNAP = [G, 2 * G, 3 * G]
    checks = [(ts, lambda A, g: (pair.lire(A, g, P1), pair.lire(A, g, P2))) for ts in SNAP]
    vals, A, g = simulate(ants, cells, checks, 3 * G + 1600, None)
    return plan, ants, cells, SNAP, vals
def memory(pair, P=(0, 0), G=1600, kw=(0, 0, 0)):
    """mémoire 1 bit à lecture destructive (comme une mémoire à tores) : écrire 1 ; lire (→ 1, la case se vide) ; récrire 1 ;
    lire (→ 1) ; lire sans récrire (→ 0) ; écrire 1. Lire = envoyer la sonde Db (tournée comme l'objet présent) ; bit lu = nombre de
    vaisseaux qui s'ÉLOIGNENT du pixel, nés de cette lecture (≥ 2 : bit 1 ; 0 : bit 0 ; la sonde elle-même n'est pas comptée)."""
    w = [0, 2 * G, 5 * G]
    plan = [('écrit', P, w[0], kw[0]), ('efface', P, pair.t_erase(w[0], G), kw[0]), ('écrit', P, w[1], kw[1]),
            ('efface', P, pair.t_erase(w[1], 3 * G), kw[1]), ('efface', P, 4 * G, kw[1]), ('écrit', P, w[2], kw[2])]
    ants, cells = build(pair, plan)
    TEND = 6 * G + 1600
    reads = [ev for ev in plan if ev[0] == 'efface']
    def bit(ev):
        s = ev[2]; tt = s + pair.TE
        def f(A, g):
            n = 0
            for a in A:
                d = hd(a[0] - P[0], a[1] - P[1])
                if 15 < d < pair.TE // 8 + 25:
                    sid = ships_of([a], {p: 1 for p in g if hd(p[0] - a[0], p[1] - a[1]) <= 2})[0]
                    if sid:
                        v = ship_dir(sid[0])
                        if (a[0] - P[0]) * v[0] + (a[1] - P[1]) * v[1] + (a[0] - P[0]) * v[1] / 2 + (a[1] - P[1]) * v[0] / 2 > 0: n += 1
            return n
        return tt, f
    checks = [(ts, (lambda A, g: pair.lire(A, g, P))) for ts in (G, 2 * G - 8, 3 * G, 4 * G - 8, 5 * G - 8, 6 * G)]
    checks += [bit(ev) for ev in reads]
    vals, A, g = simulate(ants, cells, checks, TEND, P)
    return plan, ants, cells, vals, A, g
if __name__ == '__main__':
    if sys.argv[1] == 'choix':
        good = []
        for da, db in itertools.product(OPTS, OPTS):
            p = Pair(da, db)
            if p.ph_created is None: continue
            ok = False
            for k2, k3 in itertools.product(range(6), range(6)):
                plan, ants, cells, SNAP, vals = screen(p, k2=k2, k3=k3)
                v = [tuple(x[:2] for x in w) for w in vals]
                if v == [('ON', 'OF'), ('OF', 'ON'), ('ON', 'OF')]: ok = True; print('  écran OK', da, db, 'k2', k2, 'k3', k3, vals); break
            if ok:
                okm = None
                for kw in itertools.product(range(6), repeat=3):
                    planm, _, _, valm, _, _ = memory(p, kw=kw)
                    st = [v[:2] if isinstance(v, str) else v for v in valm]
                    if [x for x in st if isinstance(x, str)] == ['ON', 'OF', 'ON', 'OF', 'OF', 'ON']: okm = (kw, valm); break
                good.append((da, db, okm)); print('écran OK', da, db, 'mémoire', okm)
        print(len(OPTS), 'options ;', len(good), 'paires OK pour l\'écran ;', sum(1 for g in good if g[2]), 'aussi pour la mémoire')
