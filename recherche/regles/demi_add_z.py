#!/usr/bin/env python3
"""R-337 Demi-additionneur R2L2 réutilisable : porte R-327 + zigzag K2 → K3 SANS DÉBRIS, cherché systématiquement.
Porte : B = vaisseau r 0 en (0,0) (joué en 1er), A = vaisseau r 2 en (30,−56) ; point de porte X = (30,−30).
U = A seul (direction 2, voie x = 30) ; V = B seul (direction 0, voie 0) ; a∧b : A décalé de 2 voies (et B d'1).
Géométrie : la seule façon de mettre U sur la voie de V est de le tourner en direction 4 (vers la gauche) en X1 = (30, −30 + s1), puis
de le retourner en direction 0 en X2 = (30 − s1, −30 + s1), sur la ROUTE D'ARRIVÉE de B (en amont de la porte) : S repasse ensuite par X,
plus tard, et continue sur la voie de V. (Toute autre direction s'éloigne des deux rayons de sortie.)
Étape 1 (K2) : A + K2 → U tourné en direction 4 + K2 propre, 0 case ; et A + B + K2 : sorties propres, 0 case.
Étape 2 (K3) : A + K2 + K3 → un vaisseau en direction 0 sur la voie 0 (= S), 0 case ; B + K2 + K3 : V intact ; K2 + K3 seuls : rien sur S.
Usage : python3 demi_add_z.py etape1 | etape2 | reuse"""
import sys, json, itertools, collections
from hx import ship, ship_dir, rot, step
from demi_add_k import lotdump, ships, fmt, OFFS, lane
from exp_osc import hd
B = ship(0, (0, 0)); A = ship(2, (30, -56)); X = (30, -30)
def kship(rK, meet, tm, i, j, tau):
    """vaisseau K de direction rK qui passerait (sans rien) près de « meet » au temps tm, décalé de (i,j), avancé de tau pas"""
    dK = ship_dir(rK); st = (meet[0] - tm // 8 * dK[0] + i, meet[1] - tm // 8 * dK[1] + j)
    ka, kc = ship(rK, st); KA = [list(ka)]; KG = {kc: 1}
    for _ in range(tau): step(KA, KG)
    return (tuple(KA[0]), sorted(KG))
def sit_of(parts, order):
    """parts : dict nom -> (fourmi, cases) ; order : liste des noms dans l'ordre de jeu"""
    ants = []; cells = []
    for n in order:
        if n in parts: ants.append(parts[n][0]); cells += list(parts[n][1])
    return fmt(ants, cells)
AT = {'A': (A[0], [A[1]]), 'B': (B[0], [B[1]])}
# trajectoire de U (A seul) : position aux temps multiples de 8
Ua = [list(A[0])]; Ug = {A[1]: 1}; UP = {0: tuple(A[0][:2])}
for t in range(1, 3000):
    step(Ua, Ug)
    if t % 8 == 0: UP[t] = (Ua[0][0], Ua[0][1])
def t_at_y(y):
    return min(UP, key=lambda t: abs(UP[t][1] - y) + abs(UP[t][0] - 30))
T = 4000
if sys.argv[1] == 'etape1':
    cand = []
    for s1 in range(8, 41, 2):
        X1 = (30, -30 + s1); tm = t_at_y(X1[1])
        for rK in (0, 1, 3, 4, 5):
            for i in range(-3, 4):
                for j in range(-3, 4):
                    for tau in range(8):
                        K = kship(rK, X1, tm, i, j, tau)
                        if hd(K[0][0] - 30, K[0][1] + 56) < 10 or hd(K[0][0], K[0][1]) < 10: continue
                        for ko in range(3): cand.append((s1, rK, i, j, tau, ko, K))
    print('candidats K2 :', len(cand)); sys.stdout.flush()
    def order(ko, names): L = [n for n in ('B', 'A') if n in names]; L.insert(ko, 'K2'); return L
    r10 = lotdump([sit_of(AT | {'K2': c[6]}, order(c[5], ['A'])) for c in cand], T)
    keep = []
    for c, r in zip(cand, r10):
        s, deb = ships(*r)
        if s is None or deb: continue
        if any(x[0] == 4 for x in s): keep.append((c, s))
    print('U tourné en direction 4, propre :', len(keep)); sys.stdout.flush()
    r11 = lotdump([sit_of(AT | {'K2': c[6]}, order(c[5], ['A', 'B'])) for c, _ in keep], T)
    r00 = lotdump([sit_of({'K2': c[6]}, ['K2']) for c, _ in keep], T)
    r01 = lotdump([sit_of(AT | {'K2': c[6]}, order(c[5], ['B'])) for c, _ in keep], T)
    good = []
    for (c, s10), a, b, d in zip(keep, r11, r00, r01):
        s11, d11 = ships(*a); s00, _ = ships(*b); s01, d01 = ships(*d)
        if s11 is None or d11 or s01 is None or d01: continue
        e = [x for x in s10 if x[0] == 4][0]
        if e in s11 or e in s00 or e in s01: continue          # la route « e » ne doit servir qu'au cas (1,0)
        if (0, 0) not in s01: continue                           # V intact
        good.append({'K2': c[:6], 'sit': c[6], 'e': e, 's10': s10, 's11': s11, 's00': s00, 's01': s01})
    print('K2 retenus (4 cas propres, e seulement dans (1,0), V intact) :', len(good))
    for g in good[:8]: print(' ', g['K2'], 'e =', g['e'], '(1,0)', g['s10'], '(1,1)', g['s11'], '(0,1)', g['s01'])
    json.dump(good, open('data/dz_k2.json', 'w'))
if sys.argv[1] == 'etape2':
    K2s = json.load(open('data/dz_k2.json'))
    reps = {}
    for g in K2s:
        key = (g['e'][1], tuple(map(tuple, g['s11'])), tuple(map(tuple, g['s01'])))
        if key not in reps or g['K2'][0] < reps[key]['K2'][0]: reps[key] = g
    reps = sorted(reps.values(), key=lambda g: g['K2'][0])[:int(sys.argv[2]) if len(sys.argv) > 2 else 40]
    print('K2 distincts essayés :', len(reps)); sys.stdout.flush()
    cand = []
    for gi, g in enumerate(reps):
        K2 = (tuple(g['sit'][0]), [tuple(c) for c in g['sit'][1]]); ko2 = g['K2'][5]
        # trajectoire du vaisseau e (cas (1,0)) : on cherche quand il croise la route de B (voie 0 de la direction 0)
        L = [n for n in ('A',)]; L.insert(ko2, 'K2')
        ants = [list(AT[n][0]) if n != 'K2' else list(K2[0]) for n in L]; cells = {c: 1 for n in L for c in (AT[n][1] if n != 'K2' else K2[1])}
        ie = None; meet = None
        for t in range(1, 3500):
            step(ants, cells)
            if t % 8 == 0 and t > 300:
                for k, a in enumerate(ants):
                    if a[2] % 2 == 0 and abs(a[0] + a[1]) <= 1 and a[0] < 30 and (ie is None or k == ie):
                        # fourmi paire au voisinage de la route de B en amont de la porte, après le virage
                        if ie is None and hd(a[0] - 30, a[1] + 30) > 6: ie = k; meet = (t, (a[0], a[1]))
            if meet: break
        if not meet: continue
        tm, X2 = meet
        for rK in range(6):
            for i in range(-3, 4):
                for j in range(-3, 4):
                    for tau in range(8):
                        K3 = kship(rK, X2, tm, i, j, tau)
                        if hd(K3[0][0] - X2[0], K3[0][1] - X2[1]) < 10: continue
                        for ko in range(3): cand.append((gi, rK, i, j, tau, ko, K3, X2, tm))
    print('candidats K3 :', len(cand)); sys.stdout.flush()
    def order(ko2, ko3, names):
        L = [n for n in ('B', 'A') if n in names]; L.insert(min(ko2, len(L)), 'K2'); L.insert(min(ko3, len(L)), 'K3'); return L
    def parts(gi, K3):
        g = reps[gi]; return AT | {'K2': (tuple(g['sit'][0]), [tuple(c) for c in g['sit'][1]]), 'K3': K3}
    r10 = lotdump([sit_of(parts(c[0], c[6]), order(reps[c[0]]['K2'][5], c[5], ['A'])) for c in cand], T)
    keep = [c for c, r in zip(cand, r10) if (lambda s, d: s is not None and not d and (0, 0) in s)(*ships(*r))]
    print('S sur la voie de V dans le cas (1,0), propre :', len(keep)); sys.stdout.flush()
    res = {ab: lotdump([sit_of(parts(c[0], c[6]), order(reps[c[0]]['K2'][5], c[5], [n for n, v in zip('AB', ab) if v])) for c in keep], T)
           for ab in [(0, 0), (0, 1), (1, 1)]}
    good = []
    for n, c in enumerate(keep):
        out = {}
        for ab in [(0, 0), (0, 1), (1, 1)]:
            s, d = ships(*res[ab][n]); out[ab] = None if (s is None or d) else s
        if None in out.values(): continue
        if (0, 0) not in out[(0, 1)] or (0, 0) in out[(0, 0)] or (0, 0) in out[(1, 1)]: continue
        if out[(0, 1)].count((0, 0)) != 1: continue
        s10 = ships(*r10[cand.index(c)])[0]
        others = set(out[(0, 0)]) | set(out[(0, 1)]) | set(s10)
        Cs = [x for x in out[(1, 1)] if x not in others]
        if not Cs: continue
        good.append({'K2': reps[c[0]]['K2'], 'K2sit': reps[c[0]]['sit'], 'K3': c[1:6], 'K3sit': c[6], 'C': Cs, 'sorties': {str(k): v for k, v in out.items()} | {'(1, 0)': s10}})
    print('demi-additionneurs (4 cas justes, 0 case) :', len(good))
    for g in good[:6]: print(' ', g['K2'], g['K3'], 'C', g['C'], g['sorties'])
    json.dump(good, open('data/dz_ha.json', 'w'))
def usage_parts(g, a, b, u, k):
    """fourmis/cases d'un usage u (entrées a, b) reculées de u·k périodes sur leurs routes ; ordre de jeu de l'usage"""
    K2 = (tuple(g['K2sit'][0]), [tuple(c) for c in g['K2sit'][1]]); K3 = (tuple(g['K3sit'][0]), [tuple(c) for c in g['K3sit'][1]])
    P = AT | {'K2': K2, 'K3': K3}
    L = [n for n, v in (('B', b), ('A', a)) if v]; L.insert(min(g['K2'][5], len(L)), 'K2'); L.insert(min(g['K3'][4], len(L)), 'K3')
    ants = []; cells = []
    for n in L:
        an, cs = P[n]
        r = next(r for r in range(6) if (an[2] - 4) % 6 == r or True and False) if False else None
        # direction du vaisseau : simulé seul 8 pas
        X_ = [list(an)]; G_ = {c: 1 for c in cs}
        for _ in range(8): step(X_, G_)
        d = (X_[0][0] - an[0], X_[0][1] - an[1])
        ants.append((an[0] - u * k * d[0], an[1] - u * k * d[1], an[2])); cells += [(c[0] - u * k * d[0], c[1] - u * k * d[1]) for c in cs]
    return ants, cells
def multi(g, seq, k):
    ants = []; cells = []
    for u, (a, b) in enumerate(seq):
        A_, C_ = usage_parts(g, a, b, u, k); ants += A_; cells += C_
    return fmt(ants, cells)
if sys.argv[1] == 'reuse':
    good = json.load(open('data/dz_ha.json')); k = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    Tm = lambda n: n * k * 8 + 4000
    seqs = list(itertools.product([(0, 0), (0, 1), (1, 0), (1, 1)], repeat=2))
    # référence : un usage seul, observé au temps Tm(2) (l'usage u est en retard de u·k périodes)
    lines = []; idx = []
    for gi, g in enumerate(good):
        for sq in seqs:
            lines.append(multi(g, sq, k)); idx.append((gi, sq, 'multi'))
        for ab in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            for u in range(2):
                A_, C_ = usage_parts(g, ab[0], ab[1], u, k); lines.append(fmt(A_, C_)); idx.append((gi, (u, ab), 'seul'))
    R = lotdump(lines, Tm(2))
    ref = {}; mult = {}
    for (gi, key, kind), r in zip(idx, R):
        (ref if kind == 'seul' else mult)[(gi, key)] = r
    ok = collections.Counter(); best = []
    for gi, g in enumerate(good):
        n = 0
        for sq in seqs:
            # superposition attendue : usage 0 = référence (0, sq[0]) ; usage 1 = référence (1, sq[1]) ; les constantes K2, K3 en double
            e0 = ref[(gi, (0, sq[0]))]; e1 = ref[(gi, (1, sq[1]))]
            exp_a = sorted(e0[0] + e1[0]); exp_c = sorted(set(e0[1]) ^ set(e1[1]))
            got = mult[(gi, sq)]
            if sorted(got[0]) == exp_a and sorted(got[1]) == exp_c: n += 1
        ok[n] += 1
        if n == 16: best.append(gi)
    print(f'k = {k} : réutilisables 16/16 (superposition exacte des 2 usages) : {len(best)} / {len(good)} ; répartition', dict(sorted(ok.items())))
    json.dump([good[i] for i in best], open(f'data/dz_ha_reuse_{k}.json', 'w'))
if sys.argv[1] == 'vingt':
    import random
    good = json.load(open('data/dz_ha_reuse_200.json')); k = 200; NU = 20
    random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 26)
    seqs = [[random.choice([(0, 0), (0, 1), (1, 0), (1, 1)]) for _ in range(NU)] for _ in range(3)]
    TT = NU * k * 8 + 4000
    lines = []; idx = []
    for gi, g in enumerate(good):
        for si, sq in enumerate(seqs): lines.append(multi(g, sq, k)); idx.append((gi, si))
    R = lotdump(lines, TT)
    # attendu : superposition des usages isolés (calculés seuls, même instant final)
    singles = {}
    need = sorted({(gi, u, ab) for gi in range(len(good)) for sq in seqs for u, ab in enumerate(sq)})
    S = lotdump([fmt(*usage_parts(good[gi], ab[0], ab[1], u, k)) for gi, u, ab in need], TT)
    for key, r in zip(need, S): singles[key] = r
    okg = []
    for gi, g in enumerate(good):
        n = 0
        for si, sq in enumerate(seqs):
            ea = []; ec = set()
            for u, ab in enumerate(sq): r = singles[(gi, u, ab)]; ea += r[0]; ec ^= set(r[1])
            got = R[idx.index((gi, si))]
            n += (sorted(got[0]) == sorted(ea) and set(got[1]) == ec)
        if n == len(seqs): okg.append(gi)
    print(f'{NU} usages au hasard × {len(seqs)} suites : superposition exacte pour {len(okg)} / {len(good)} demi-additionneurs')
    json.dump({'seqs': seqs, 'ok': [good[i] for i in okg]}, open('data/dz_ha_vingt.json', 'w'))
