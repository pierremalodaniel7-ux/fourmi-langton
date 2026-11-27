#!/usr/bin/env python3
"""S1 / R-403 FUSION PROPRE ET RÉUTILISABLE à 2 constants : « intercepteur de déchet ».
Base = fusion à 1 constant NON réutilisable (fusion1_ok.json) dont le SEUL défaut est un déchet qui repart à contresens sur l'axe
d'une entrée (types (1,2,2) « g1 → s2 » et (4,5,4) « g2 → s1 », 144 chacun ; les invariants I1/I2 de R-331 forcent sa direction).
On cherche un 2e constant K' qui percute ce déchet δ périodes après sa naissance (là où l'entrée correspondante est déjà passée) :
3 cas propres, O présent dans x et y, absent du cas « aucun », O sans ombre (aucune sortie du cas « aucun » parallèle à ≤ 6 voies),
aucune route de face (sorties / entrées s1, s2, K, K'), puis 2 usages 9/9 en superposition exacte.
Usage : python3 s1_fusion/fusion3.py <type 122|454> <début> <fin>"""
import sys, os, json, itertools, time, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from fa_lib import decode, back, lotdump, sit, kship
from hx import ship_dir, rot
from exp_osc import hd
from fusion_reuse import Excl, route, front, make
from circuit import check_multi
T = 4000
typ = sys.argv[1]; b0, b1 = int(sys.argv[2]), int(sys.argv[3])
D = json.load(open(os.path.join(HERE, 'fusion1.json'))); K = (tuple(D['K'][0]), [tuple(c) for c in D['K'][1]])
ok = json.load(open(os.path.join(HERE, 'fusion1_ok.json'))); rk = route(K)
bases = []
for z in ok:
    O = z['O']; ins = {'s1': tuple(z['r1']), 's2': tuple(z['r2']), 'K': rk}; bad = set()
    for q in (0, 1, 2):
        for o in z['out%d' % q]:
            for n, e in ins.items():
                if front(tuple(o[:2]), e): bad.add(('O' if list(o) == list(O) else 'g%d' % q) + '->' + n)
    t = '%d%d%d' % (z['r1'][0], z['r2'][0], O[0])
    if t == typ and len(bad) == 1: bases.append((z, bad.pop()))
print('bases du type', typ, ':', len(bases), flush=True)
def place(P, t, rK):
    """départ d'un vaisseau de direction rK qui serait au point P à l'instant t (multiple de 8)"""
    dK = ship_dir(rK); return (P[0] - t // 8 * dK[0], P[1] - t // 8 * dK[1])
def refpoint(o, t):
    """point de référence au temps t d'un vaisseau décodé o = (r, voie, abscisse, phase) au temps T"""
    r, l, a, ph = o; a2 = a - 2 * ((T - t) // 8)
    X, Y = (l + a2) // 2, (l - a2) // 2
    return rot((X, Y), r)
out_path = os.path.join(HERE, 'fusion3_%s_%d_%d.json' % (typ, b0, b1)); good = []; stats = collections.Counter(); t0 = time.time()
for bi in range(b0, min(b1, len(bases))):
    z, bad = bases[bi]
    C = Excl(make(z, K)); cs = C.cases()
    R = lotdump([C.sit(e) for e in cs], T); d = [decode(*r) for r in R]
    q = int(bad[1]); gname = bad.split('->')[1]
    O = sorted((set(map(tuple, d[1])) & set(map(tuple, d[2]))) - set(map(tuple, d[0])))[0]
    garb = [o for o in d[q] if tuple(o) != O and front(tuple(o[:2]), route(dict((n, p) for n, p, v in C.pieces)[gname]))]
    if len(garb) != 1: stats['déchet ambigu'] += 1; continue
    g = garb[0]
    ins = [route(p) for n, p, v in C.pieces]
    tk = 8 * (25 + 60)
    cand = []
    for dl in (3, 6, 10, 16, 25, 40):
        t = tk + 8 * dl; P = refpoint(g, t)
        for rK in range(6):
            for i in range(-3, 4):
                for j in range(-3, 4):
                    st = place((P[0] + i, P[1] + j), t, rK)
                    for tau in range(8):
                        Kp = kship(rK, st, tau)
                        if min(hd(Kp[0][0] - p[0][0], Kp[0][1] - p[0][1]) for _, p, _ in C.pieces) < 12: continue
                        if any(front(route(Kp), e) for e in ins): continue
                        for first in (0, 1): cand.append((dl, rK, i, j, tau, first, Kp))
    Cs = [Excl(([('Kp', c[6], None)] + list(C.pieces)) if c[5] else (list(C.pieces) + [('Kp', c[6], None)])) for c in cand]
    RR = lotdump([X.sit(e) for X in Cs for e in X.cases()], T)
    nb = 0
    for n, (c, X) in enumerate(zip(cand, Cs)):
        dd = [decode(*RR[3 * n + k]) for k in range(3)]
        if None in dd: stats['sale'] += 1; continue
        dd = [set(map(tuple, x)) for x in dd]
        com = (dd[1] & dd[2]) - dd[0]
        com = {o for o in com if not any(p[0] == o[0] and abs(p[1] - o[1]) <= 6 for p in dd[0])}
        if not com: stats['pas de sortie commune sans ombre'] += 1; continue
        outs = {o[:2] for x in dd for o in x}
        if any(front(s, e) for s in outs for e in ins + [route(c[6])]): stats['route de face'] += 1; continue
        Op = sorted(com)[0]; X.outputs = {'O': (lambda e: e['x'] | e['y'], [Op])}
        n2 = sum(1 for e1, e2 in itertools.product(X.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(X, [e1, e2], 200)))
        if n2 != 9: stats['2 usages < 9/9'] += 1; continue
        stats['OK'] += 1; nb += 1
        good.append(dict(base=bi, typ=typ, c=c[:6], Kp=c[6], O=Op, out=[sorted(x) for x in dd], pieces=[(nn, p, v) for nn, p, v in X.pieces]))
        print('FUSION PROPRE RÉUTILISABLE (2 usages 9/9)', bi, c[:6], 'O =', Op, flush=True)
    json.dump(good, open(out_path, 'w'))
    print(f'base {bi} ({len(cand)} placements) : {nb} ; {dict(stats)} {round(time.time() - t0)} s', flush=True)
print('fin', dict(stats))
