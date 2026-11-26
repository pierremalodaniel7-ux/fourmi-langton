#!/usr/bin/env python3
"""R-335 Mémoire 1 bit R2L2 à lecture destructive (comme une mémoire à tores), sans aucune case fixe : bit 1 = oscillateur O2 présent
(« H:R2L2|0,0,3;1,0,0|1,0;-1,1 », 2 fourmis + 2 cases, période 3), bit 0 = rien.
ÉCRIRE 1 = 3 vaisseaux (film à l'envers d'une destruction Da, variante et rotation au choix) ; LIRE = 1 sonde (destruction Db) : si le bit
vaut 1, O2 part en 3 vaisseaux (2 de plus que la sonde) et la case se vide ; si le bit vaut 0, la sonde traverse du vide.
Programme : écrire 1 ; lire (→ 1) ; récrire 1 ; lire (→ 1) ; lire (→ 0) ; écrire 1 ; tout dans UNE simulation, vaisseaux posés à t = 0.
Choix des variantes : pré-test des routes (2 vaisseaux sur le même axe, voies à ≤ 6, sens opposés, l'un encore en approche quand l'autre
repart → choc frontal en vol), puis simulation. Usage : python3 memoire.py [nb_essais]"""
import sys, json, random, itertools, subprocess
from ecran import Pair, OPTS, build, simulate, ships_of, tr, film
from hx import step, rot, sit, reverse, ship_dir
from exp_osc import hd
def lane(x, y, r):
    X, Y = rot((x, y), -r % 6); return X + Y
def route(a, r): l = lane(a[0], a[1], r); return (r % 3, l if r < 3 else -l, r)
CACHE = {}
def info(da, db):
    if (da, db) in CACHE: return CACHE[(da, db)]
    p = Pair(da, db)
    if p.ph_created is None: CACHE[(da, db)] = None; return None
    # routes du kit d'écriture : entrées (3) et sortie (1) ; du kit de lecture : entrée, sorties si ON
    cin = [(a, s[0]) for a, s in zip(p.CREATE[0], ships_of(*p.CREATE))]
    A, g = [list(a) for a in p.CREATE[0]], dict(p.CREATE[1])
    for _ in range(p.TC): step(A, g)
    cout = [(a, s[0]) for a, s in zip(A, ships_of(A, g)) if s and hd(a[0], a[1]) > 6]
    Eb, kitb, fb = film(*db)
    rin = [(kitb[0][0], db[1])]
    rout = [(a, s[0]) for a, s in zip(fb[0], ships_of(*fb)) if s]
    CACHE[(da, db)] = (p, cin, cout, rin, rout); return CACHE[(da, db)]
def rot_route(a, r, k):
    X, Y = rot((a[0], a[1]), k); return route((X, Y), (r + k) % 6)
def precheck(events, marge=6):
    """events : liste (t, kind, entrées [(a,r)], sorties [(a,r)], k) ; conflit = sortie d'un événement i et entrée d'un événement j > i
    sur le même axe, voies proches, sens opposés"""
    R = []
    for t, kind, ins, outs, k in events:
        R.append((t, [rot_route(a, r, k) for a, r in ins], [rot_route(a, r, k) for a, r in outs]))
    for i, (ti, _, oi) in enumerate(R):
        for j, (tj, ij, _) in enumerate(R):
            if tj <= ti: continue
            for (ax1, l1, r1) in oi:
                for (ax2, l2, r2) in ij:
                    if ax1 == ax2 and r1 != r2 and abs(l1 - l2) <= marge: return False
    return True
G = 1600
def plan_of(choice):
    """choice = ((da1, k1), (db1), (da2, k2), (db2), (db3), (da3, k3)) → plan de build + événements pour precheck"""
    (da1, k1), db1, (da2, k2), db2, db3, (da3, k3) = choice
    I1 = info(da1, db1); I2 = info(da2, db2); I3 = info(da3, db3 if False else db2)
    if not I1 or not I2: return None
    p1, p2 = I1[0], I2[0]
    tr1 = p1.t_erase(0, G); tr2 = p2.t_erase(2 * G, 3 * G)
    ev = [(0, 'écrit', I1[1], I1[2], k1), (tr1, 'lit1', I1[3], I1[4], k1), (2 * G, 'écrit', I2[1], I2[2], k2),
          (tr2, 'lit1', I2[3], I2[4], k2)]
    # lecture d'une case vide : sonde Db3 (on prend la variante db3 avec le pair de da2), elle traverse
    I3r = info(da2, db3)
    if not I3r: return None
    ev.append((4 * G, 'lit0', I3r[3], [(I3r[3][0][0], I3r[3][0][1])], k2))
    I3w = info(da3, db2)
    if not I3w: return None
    ev.append((5 * G, 'écrit', I3w[1], I3w[2], k3))
    return ev, (p1, p2, I3r[0], I3w[0]), (tr1, tr2)
def run(choice, verbose=False):
    pl = plan_of(choice)
    if not pl: return None
    ev, (p1, p2, p3r, p3w), (tr1, tr2) = pl
    (da1, k1), db1, (da2, k2), db2, db3, (da3, k3) = choice
    P = (0, 0)
    # build avec des paires différentes par événement
    ants, cells = [], {}
    def add(kit, k, s, before=None):
        a, g = __import__('ecran').back(*tr(kit, P, k), s); cells.update(g)
        if before is None: ants.extend(a); return len(ants) - len(a)
        ants[before:before] = a; return before
    i1 = add(p1.CREATE, k1, 0); add(p1.ERASE, k1, tr1, i1 if db1[0] == 1 else None)
    i2 = add(p2.CREATE, k2, 2 * G); add(p2.ERASE, k2, tr2, i2 if db2[0] == 1 else None)
    add(p3r.ERASE, k2, 4 * G)
    add(p3w.CREATE, k3, 5 * G)
    def etat(A, g):
        na = [a for a in A if hd(a[0], a[1]) <= 6]; nc = [c for c in g if hd(*c) <= 6]
        if not na and not nc: return 0
        return p1.lire(A, g, P)
    def bit(t0, TE):
        def f(A, g):
            n = 0
            for a in A:
                d = hd(a[0], a[1])
                if 15 < d < TE // 8 + 25:
                    sid = ships_of([a], {c: 1 for c in g if hd(c[0] - a[0], c[1] - a[1]) <= 2})[0]
                    if sid:
                        v = ship_dir(sid[0])
                        if hd(a[0] + v[0], a[1] + v[1]) > d: n += 1
            return n
        return (t0 + TE, f)
    checks = [(G, etat), (2 * G - 8, etat), (3 * G, etat), (4 * G - 8, etat), (5 * G - 8, etat), (6 * G, etat),
              bit(tr1, p1.TE), bit(tr2, p2.TE), bit(4 * G, p3r.TE)]
    vals, A, g = simulate(ants, cells, checks, 6 * G + 1600, P)
    return vals, ants, cells
if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    random.seed(11); tried = 0; ok = []
    DA = [o for o in OPTS]; DB = [o for o in OPTS]
    while tried < N and len(ok) < 3:
        ch = ((random.choice(DA), random.randrange(6)), random.choice(DB), (random.choice(DA), random.randrange(6)), random.choice(DB),
              random.choice(DB), (random.choice(DA), random.randrange(6)))
        pl = plan_of(ch)
        if not pl: continue
        tried += 1
        res = run(ch)
        if not res: continue
        vals = res[0]
        st = [v[:2] if isinstance(v, str) else v for v in vals]
        # ordre des checks par temps : G, lit1 (tr1+TE), 2G-8, 3G, lit2, 4G-8, lit0, 5G-8, 6G
        if tried % 200 == 0: print('essai', tried, ch, vals); sys.stdout.flush()
        good = [vals[0] != 0 and 'ON' in str(vals[0])]
        seq = vals
        # attendu (dans l'ordre des temps) : ON, 3, 0, ON, 3, 0, 1, 0, ON
        if [('ON' if isinstance(v, str) and v.startswith('ON') else v) for v in seq] == ['ON', 3, 0, 'ON', 3, 0, 1, 0, 'ON']:
            ok.append(ch); print('MÉMOIRE OK', ch, seq); sys.stdout.flush()
    print('essais', tried, 'réussis', len(ok))
    json.dump({'reussis': [list(map(str, c)) for c in ok]}, open('data/memoire_choix.json', 'w'))
