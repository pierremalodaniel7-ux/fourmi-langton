#!/usr/bin/env python3
"""R-348 Relais à 3 états (boucle, consigne 3a/3b). T3 (BOUCLE.md) : un relais qui dévie un vaisseau de ±120° à chaque passage doit
avoir un nombre d'états multiple de 3. On cherche R0 → R1 → R2 → R0 : à chaque passage un vaisseau arrive sur la MÊME route absolue
(direction r, voie l) et un seul vaisseau repart sur la MÊME route (r', l'), r' = r ± 2, l'objet changeant d'état (2 fourmis).
Étape 1 : 95 oscillateurs à 2 fourmis (miroir2 enum 2 3 1 4096) × 6 directions × voies × phases × 2 ordres.
Étape 2 et 3 : on retire sur R1 puis R2 avec la même route d'entrée, à toutes les phases. Moteur fourmi_r (lot) ; hx.py pour revérifier.
Usage : python3 relais.py data/osc2.txt"""
import sys, json, collections, time
from fa_lib import lotdump, decode, kship
from hx import ship, ship_dir, rot, step, PHASES
from demi_add_k import OFFS, lane, fmt
from exp_osc import hd
D = 30; TT = 8 * (2 * D + 12)
def parse(s):
    _, a, c = s.strip().split('|')[:3]
    return [tuple(map(int, t.split(','))) for t in a.split(';') if t], [tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t]
def orbit(ants, cells, pmax=3000):
    A = [list(a) for a in ants]; g = {tuple(c): 1 for c in cells}; st0 = (tuple(map(tuple, A)), frozenset(g)); L = []
    for t in range(pmax):
        L.append((tuple(map(tuple, A)), frozenset(g))); step(A, g)
        if (tuple(map(tuple, A)), frozenset(g)) == st0: return L
    return None
def key(L):
    """clé d'une orbite à position absolue : ensemble des états (fourmis non ordonnées)"""
    return frozenset((frozenset(a), c) for a, c in L)
def center(ants): return (sum(a[0] for a in ants) // len(ants), sum(a[1] for a in ants) // len(ants))
def split(ants, cells, c0, rad=10):
    """objet (fourmis/cases à ≤ rad du centre c0) + vaisseaux (r, voie, abscisse, phase) ; None si sale"""
    obj = [a for a in ants if hd(a[0] - c0[0], a[1] - c0[1]) <= rad]; far = [a for a in ants if a not in obj]
    oc = [c for c in cells if hd(c[0] - c0[0], c[1] - c0[1]) <= rad]; fc = [c for c in cells if c not in oc]
    sh = decode(far, fc)
    return (obj, oc, sh) if sh is not None else None
def fire(states, routes):
    """states : liste (nom, orbite L) ; routes : liste (r, voie absolue) ou None = toutes les voies proches.
    Renvoie les conversions (nom, r, voie, phase, ordre, sortie(s), objet restant (fourmis, cases), état initial)."""
    jobs = []; meta = []
    for nm, L in states:
        p = len(L); c0 = center(L[0][0])
        for r in range(6):
            d = ship_dir(r); e = rot((1, 0), r)
            for l in range(-8, 9):
                st = (c0[0] - D * d[0] + l * e[0], c0[1] - D * d[1] + l * e[1]); la = lane(st[0], st[1], r)
                if routes is not None and (r, la) not in routes: continue
                sa, sc = ship(r, st)
                for ph in range(p):
                    ants, cells = L[ph]
                    for o in (0, 1):
                        A = ([sa] if o else []) + list(ants) + ([] if o else [sa])
                        jobs.append(fmt(A, list(cells) + [sc])); meta.append((nm, r, la, ph, o, c0))
    out = []
    for m, res in zip(meta, lotdump(jobs, TT) if jobs else []):
        s = split(res[0], res[1], m[5])
        if s is None: continue
        obj, oc, sh = s
        if len(sh) != 1 or len(obj) != 2: continue
        out.append(m[:5] + (sh[0], (tuple(sorted(obj)), tuple(sorted(oc)))))
    return out
if __name__ == '__main__':
    t0 = time.time()
    osc = [l.split('| ', 1)[1].strip() for l in open(sys.argv[1]) if l.startswith('OSC')]
    S0 = []
    for i, o in enumerate(osc):
        L = orbit(*parse(o))
        if L: S0.append((i, L))
    K0 = {i: key(L) for i, L in S0}
    c1 = fire(S0, None)
    dev = [c for c in c1 if c[5][0] in ((c[1] + 2) % 6, (c[1] + 4) % 6)]
    print('étape 1 : conversions propres', len(c1), '; dont déviées ±120°', len(dev), flush=True)
    # le reste : un oscillateur ? différent de R0 ?
    R1 = {}
    for c in dev:
        L = orbit(list(c[6][0]), list(c[6][1]))
        if not L: continue
        k = key(L)
        if k == K0[c[0]]: continue        # redevenu lui-même : interdit par T3 (contrôle)
        R1.setdefault(k, (L, []))[1].append(c)
    print('R1 distincts (oscillateurs, ≠ R0) :', len(R1), flush=True)
    # étape 2 : sur chaque R1, même route d'entrée, même route de sortie
    found2 = []; R2 = {}
    items = list(R1.items())
    for b in range(0, len(items), 300):
        chunk = items[b:b + 300]
        states = [(j + b, v[0]) for j, (k, v) in enumerate(chunk)]
        routes = {(c[1], c[2]) for k, v in chunk for c in v[1]}
        c2 = fire(states, routes)
        for c in c2:
            k1, (L1, prev) = items[c[0]]
            for p in prev:
                if (p[1], p[2]) != (c[1], c[2]) or (p[5][0], p[5][1]) != (c[5][0], c[5][1]): continue
                L = orbit(list(c[6][0]), list(c[6][1]))
                if not L: continue
                k2 = key(L)
                R2.setdefault(k2, (L, []))[1].append((p, c))
    print('chaînes R0 → R1 → R2 (même route) :', sum(len(v[1]) for v in R2.values()), '; R2 distincts', len(R2), flush=True)
    found = []
    items2 = list(R2.items())
    for b in range(0, len(items2), 300):
        chunk = items2[b:b + 300]
        states = [(j + b, v[0]) for j, (k, v) in enumerate(chunk)]
        routes = {(p[1], p[2]) for k, v in chunk for p, c in v[1]}
        c3 = fire(states, routes)
        for c in c3:
            k2, (L2, prev) = items2[c[0]]
            L = orbit(list(c[6][0]), list(c[6][1]))
            if not L: continue
            k3 = key(L)
            for p, q in prev:
                if (p[1], p[2]) != (c[1], c[2]) or (p[5][0], p[5][1]) != (c[5][0], c[5][1]): continue
                if k3 == K0[p[0]]: found.append({'R0': osc[p[0]], 'pas1': p[:6], 'pas2': q[:6], 'pas3': c[:6]})
    print('RELAIS À 3 ÉTATS (R0 → R1 → R2 → R0, même route) :', len(found), ' temps', round(time.time() - t0), 's')
    json.dump(found, open('data/relais3.json', 'w'), default=str)
    for f in found[:10]: print(f)
