#!/usr/bin/env python3
"""Banc d'essai des règles (R-306 et suivants) : DÉVIATION (b), CROISEMENT (c), RÉUTILISATION (d), mêmes protocoles pour toutes.
Lanceur = germe de data/germes_regles.json (fourmi en (0,0), autoroute dès le départ, période P, déplacement D par période).
Usage : python3 banc.py REGLE [REGLE…]   → data/banc_<règle>.json + ligne de résumé."""
import sys, json, subprocess, collections
from outils_r import lot, parse, geo
EXE = './fourmi_r'
K = 30                                   # la fourmi B touche l'obstacle après K périodes (loin de son germe)
TB = 1 << 21                             # pas max après choc
def rot(rule, x, y, d, r):
    """rotation de r crans (carré 90°, hexa 60°) autour de l'origine ; triangle : None"""
    for _ in range(r):
        if rule.startswith('T:'): return None
        if rule.startswith('H:'): x, y = -y, x + y; d = (d + 1) % 6
        else: x, y = -y, x; d = (d + 1) % 4
    return x, y, d
def rotv(rule, v, r):
    a = rot(rule, v[0], v[1], 0, r); return (a[0], a[1])
def launcher(g, r=0, at=(0, 0)):
    """(fourmi, cases) du germe tourné de r crans et translaté en at"""
    ax, ay, ad = rot(g['regle'], *g['fourmi'], r)
    cells = {}
    for x, y, k in g['cases']:
        X, Y, _ = rot(g['regle'], x, y, 0, r); cells[(X + at[0], Y + at[1])] = k
    return (ax + at[0], ay + at[1], ad), cells
def sit(rule, ants, cells):
    return f"{rule}|" + ';'.join(f"{x},{y},{d}" for x, y, d in ants) + '|' + ';'.join(f"{x},{y},{k}" for (x, y), k in cells.items())
def path(rule, ants, cells, a, b):
    out = subprocess.run([EXE, '-T', str(b), '-x', '-path', str(a), str(b), '-lot'], input=sit(rule, ants, cells) + '\n', capture_output=True, text=True).stdout
    l = [x for x in out.splitlines() if x.startswith('PATH')][0].split()[2:]
    return [tuple(map(int, p.split(','))) for p in l]
def dirclass(rule, D, D2):
    """r tel que D2 a la direction de rot^r(D) (même sens), sinon None"""
    _, M = geo(rule)
    for r in range(M if not rule.startswith('T:') else 1):
        a = rotv(rule, D, r)
        if a[0] * D2[1] - a[1] * D2[0] == 0 and a[0] * D2[0] + a[1] * D2[1] > 0: return r
    return None
def lane(D, p): return D[0] * p[1] - D[1] * p[0]
def outcome(rule, l, i, P, D):
    """issue de la fourmi i : ('propre'|'autre'|'perdue', classe de direction, voie, début)"""
    d = parse(l)
    if d['issue'] == 'CYCLE': return ('cycle', None, None, None)
    a = d['ants'][i] if i < len(d['ants']) else None
    if a is None: return ('perdue', None, None, None)
    p, dx, dy, deb = a
    r = dirclass(rule, D, (dx, dy))
    return ('propre' if p == P and r is not None and d['issue'] == 'AUTOROUTES' else 'autre', r, lane((dx, dy), d['fin'][i]), deb)

def banc(g):
    rule, P, D = g['regle'], g['P'], tuple(g['D'])
    _, M = geo(rule); nb = [(1,0),(0,1),(-1,0),(0,-1)] if M == 4 and not rule.startswith('H:') else [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
    if rule.startswith('T:'): nb = [(1,0),(0,1),(-1,0),(0,-1)]
    ant, cells = launcher(g)
    t2 = K * P
    V = list(dict.fromkeys((x, y) for x, y, _ in path(rule, [ant], cells, t2, t2 + P - 1)))
    solo = parse(lot([sit(rule, [ant], cells)], TB)[0]); sol = outcome(rule, lot([sit(rule, [ant], cells)], TB)[0], 0, P, D)
    R = {'regle': rule, 'P': P, 'D': D, 'V': len(V)}
    # (b1) 1 case, (b2) 2 cases voisines
    def dev(confs, tag):
        lines = []
        for cs in confs:
            c = dict(cells); [c.__setitem__(v, 1) for v in cs]; lines.append(sit(rule, [ant], c))
        res = [outcome(rule, l, 0, P, D) for l in lot(lines, TB)]
        n = len(res); pr = [o for o in res if o[0] == 'propre']
        transp = sum(1 for o in pr if o[1] == 0 and o[2] == sol[2])
        dirs = collections.Counter(o[1] for o in pr)
        chaos = sorted(max(0, o[3] - t2) for o in pr if not (o[1] == 0 and o[2] == sol[2]))
        R[tag] = {'n': n, 'propre': len(pr), 'transparent': transp, 'dirs': {str(k): v for k, v in dirs.items()},
                  'nb_dirs_sortie': len([k for k in dirs if k != 0] ) + (1 if any(o[1] == 0 and o[2] != sol[2] for o in pr) else 0),
                  'chaos_med': chaos[len(chaos) // 2] if chaos else None, 'chaos_max': chaos[-1] if chaos else None,
                  'issues': dict(collections.Counter(o[0] for o in res))}
        return res
    r1 = dev([[v] for v in V], 'b1_1case')
    pairs = list(dict.fromkeys(tuple(sorted([v, (v[0] + e[0], v[1] + e[1])])) for v in V for e in nb))
    dev(pairs, 'b2_2cases')
    # (b3) vieille trace : lanceur A tourné de r crans, passe en X (point de B au temps t2) K/3 périodes avant B
    X = V[0]; tr = []; cr = []
    rots = range(1, M) if not rule.startswith('T:') else []
    for r in rots:
        DA = rotv(rule, D, r)
        for kA, store in ((K // 3, tr), (K, cr)):
            for i in range(4):
                for j in range(4):
                    st = (X[0] - kA * DA[0] + i, X[1] - kA * DA[1] + j)
                    if rule.startswith('T:') and (st[0] + st[1]) % 2: continue
                    a2, c2 = launcher(g, r, st)
                    c = dict(cells); c.update(c2)
                    store.append((r, st, sit(rule, [ant, a2], c), a2, c2))
    def b3(store, tag):
        if not store: R[tag] = None; return
        res = lot([s[2] for s in store], TB)
        # solo de A
        solosA = lot([sit(rule, [s[3]], s[4]) for s in store], TB)
        ob = [outcome(rule, l, 0, P, D) for l in res]
        oa = [outcome(rule, l, 1, P, rotv(rule, D, s[0])) for l, s in zip(res, store)]
        sa = [outcome(rule, l, 0, P, rotv(rule, D, s[0])) for l, s in zip(solosA, store)]
        n = len(ob)
        bp = sum(1 for o in ob if o[0] == 'propre')
        both = sum(1 for o, a in zip(ob, oa) if o[0] == 'propre' and a[0] == 'propre')
        transp = sum(1 for o, a, s in zip(ob, oa, sa) if o[0] == 'propre' and o[1] == 0 and o[2] == sol[2] and a[0] == 'propre' and a[1] == 0 and a[2] == s[2])
        dirs = collections.Counter(o[1] for o in ob if o[0] == 'propre')
        chaos = sorted(max(0, o[3] - t2) for o in ob if o[0] == 'propre' and not (o[1] == 0 and o[2] == sol[2]))
        R[tag] = {'n': n, 'B_propre': bp, 'deux_propres': both, 'transparent': transp, 'dirs_B': {str(k): v for k, v in dirs.items()},
                  'chaos_med': chaos[len(chaos) // 2] if chaos else None, 'issues_B': dict(collections.Counter(o[0] for o in ob))}
        if tag == 'c_croisement':
            R[tag]['exemples_transparents'] = [s[2] for o, a, s2, s in zip(ob, oa, sa, store) if o[0] == 'propre' and o[1] == 0 and o[2] == sol[2] and a[0] == 'propre' and a[1] == 0 and a[2] == s2[2]][:3]
    b3(tr, 'b3_trace'); b3(cr, 'c_croisement')
    # (d) réutilisation : A = même lanceur m périodes devant sur la même voie ; B part derrière
    reu = {}
    for m in (3, 10):
        a2, c2 = launcher(g, 0, (m * D[0], m * D[1]))
        if rule.startswith('T:') and (m * D[0] + m * D[1]) % 2: continue
        c = dict(cells); c.update(c2)
        l = lot([sit(rule, [ant, a2], c)], TB)[0]
        reu[f'libre_m{m}'] = {'B': outcome(rule, l, 0, P, D), 'A': outcome(rule, l, 1, P, D), 'solo': sol, 'ligne': parse(l)['sig']}
    # obstacle réutilisable : cas b1 « propres et déviés » ; A passe d'abord (m=3 périodes devant), B ensuite
    defl = [(V[k], o) for k, o in enumerate(r1) if o[0] == 'propre' and not (o[1] == 0 and o[2] == sol[2])]
    lines = []; meta = []
    for v, o in defl:
        for m in (3, 10):
            a2, c2 = launcher(g, 0, (m * D[0], m * D[1]))
            c = dict(cells); c.update(c2); c[(v[0] + m * D[0], v[1] + m * D[1])] = 1   # obstacle placé K périodes devant A
            # A seul contre l'obstacle se comporte comme B seul contre v (translation) : sortie de référence = o translaté
            lines.append(sit(rule, [ant, a2], c)); meta.append((v, o, m))
    same = 0; same_dir = 0; Bpropre = 0; det = collections.Counter()
    if lines:
        for l, (v, o, m) in zip(lot(lines, TB), meta):
            ob, oa = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, D)
            if ob[0] == 'propre': Bpropre += 1
            if ob[0] == 'propre' and oa[0] == 'propre' and ob[1] == oa[1]:
                same_dir += 1
                if ob[2] == oa[2]: same += 1
            det[(ob[0], ob[1] == oa[1] if ob[0] == 'propre' and oa[0] == 'propre' else None)] += 1
    reu['miroir'] = {'n': len(lines), 'B_propre': Bpropre, 'meme_direction_que_A': same_dir, 'meme_voie_que_A': same,
                     'detail': {str(k): v for k, v in det.items()}}
    R['d_reutilisation'] = reu
    return R
if __name__ == '__main__':
    G = json.load(open('data/germes_regles.json'))
    for rule in sys.argv[1:]:
        R = banc(G[rule])
        json.dump(R, open('data/banc_' + rule.replace(':', '_') + '.json', 'w'), indent=1, default=str)
        b1, b2, b3, c = R['b1_1case'], R['b2_2cases'], R['b3_trace'], R['c_croisement']
        print(f"{rule}\tP={R['P']}\t1case {b1['propre']}/{b1['n']} transp {b1['transparent']} dirs {b1['dirs']} chaos {b1['chaos_med']}"
              f"\t2cases {b2['propre']}/{b2['n']}\ttrace {b3 and str(b3['B_propre'])+'/'+str(b3['n'])}\tcrois.transp {c and str(c['transparent'])+'/'+str(c['n'])}"
              f"\tmiroir {R['d_reutilisation']['miroir']['meme_voie_que_A']}/{R['d_reutilisation']['miroir']['n']}", flush=True)
