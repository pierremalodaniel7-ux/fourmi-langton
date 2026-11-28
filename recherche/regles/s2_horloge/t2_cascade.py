"""T2 — COMPTEUR À 2 ÉTAGES (essai) : on part d'une machine t2_sym de période 2P (horloge + 3 objets qui retardent/avancent les vaisseaux,
le retard alterne d'un tour à l'autre : le vaisseau PORTE le bit) et on ajoute un 2e jeu de 3 copies 3-symétriques d'un objet, posé
devant les vaisseaux de l'horloge (dans la machine complète). Si le 2e étage réagit au retard, la période peut devenir 4P.
Usage : python3 s2_horloge/t2_cascade.py base.json rang mode [n]   (mode = exact | retard | tout) → s2_horloge/t2_cascade_<rang>_<mode>.json"""
import sys, json, collections, random
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, rot
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from tri import at
from exp_osc import hd
Hb = json.load(open(sys.argv[1])); rk = int(sys.argv[2]); base = Hb[rk]; mode = sys.argv[3]; nref = int(sys.argv[4]) if len(sys.argv) > 4 else 200
O = json.load(open('../../data/t2/objets.json')); C = json.load(open('../../data/t2/conversions_effet.json'))
U = {}
for c in C:
    ok = (mode in ('exact', 'tout') and c['kind'].endswith('/ exact')) or (mode in ('retard', 'tout') and c['kind'] == 'X1 ≠ X0 / retard' and abs(c['dt']) <= 12 and c['p1'] <= 42)
    if ok: U.setdefault((c['o'], c['k']), c)
random.seed(3); W = random.sample(sorted(U.values(), key=lambda c: (c['o'], c['k'])), min(nref, len(U)))
refs = []
for w in W:
    a, c = parts_of(O[w['o']]['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    for _ in range(w['ph']): step(A, G)
    s_a, s_c = at((0, (w['k'] - 40, 40), w['tau']), 0); A.append(list(s_a)); G.update({tuple(x): 1 for x in s_c})
    for t in range(400):
        if hd(A[2][0], A[2][1]) <= 10: break
        step(A, G)
    sx, sy, sh = A[2]
    refs.append({'o': w['o'], 'p0': O[w['o']]['p'], 'ship': (sh, frozenset((q[0] - sx, q[1] - sy) for q in G if hd(q[0] - sx, q[1] - sy) <= 2)),
                 'obj': ([(x - sx, y - sy, h) for x, y, h in A[:2]], [(q[0] - sx, q[1] - sy) for q in G if hd(q[0] - sx, q[1] - sy) > 2])})
def evolve(ants, cells, n):
    A = [list(t) for t in ants]; G = {tuple(t): 1 for t in cells}
    for _ in range(n): step(A, G)
    return [tuple(q) for q in A], list(G)
one = {}
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if w['P'] <= 1200: one.setdefault(w['P'], w)
cw = list(one.values())[base['clock']]; P0 = base['P0']; T = P0 // 3; cc = tuple(cw['c'])
# le centre/rotation R de l'horloge est défini dans le repère de cw['sit'] (temps 0) ; la base est l'horloge avancée de base['t'] pas : même R
def R(pt, k):
    x, y = pt
    for _ in range(k): x, y = rot((x, y), 2); x, y = x + cc[0], y + cc[1]
    return (x, y)
a, c = parts_of(base['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; nob = len(a) - 6
jobs = []; info = []; npose = collections.Counter()
for t in range(base['P']):
    for i in range(nob, len(A)):
        x, y, h = A[i]
        if min(hd(x - b[0], y - b[1]) for j, b in enumerate(A) if j != i) < 12: continue
        loc = frozenset((q[0] - x, q[1] - y) for q in G if hd(q[0] - x, q[1] - y) <= 2)
        for ri, r in enumerate(refs):
            for kk in range(6):
                if h != (r['ship'][0] + kk) % 6 or loc != frozenset(rot(q, kk) for q in r['ship'][1]): continue
                if npose[(i, kk, ri)] >= 2: continue
                Pa = [(*(lambda v: (v[0] + x, v[1] + y))(rot((px, py), kk)), (ph + kk) % 6) for px, py, ph in r['obj'][0]]
                Pc = [(lambda v: (v[0] + x, v[1] + y))(rot(q, kk)) for q in r['obj'][1]]
                allA, allC = list(Pa), list(Pc)
                for m in (1, 2):
                    ea, ec = evolve(Pa, Pc, (-m * T) % (r['p0'] * 8))
                    allA += [(*R((x_, y_), m), (h_ + 2 * m) % 6) for x_, y_, h_ in ea]; allC += [R(q, m) for q in ec]
                if min(hd(p[0] - b[0], p[1] - b[1]) for p in allA for b in A) < 7: continue
                if set(allC) & set(G) or len(set(allC)) < len(allC): continue
                npose[(i, kk, ri)] += 1
                jobs.append(fmt(allA + [tuple(q) for q in A], list(G) + allC)); info.append({'t': t, 'ship': i, 'kk': kk, 'ref': ri, 'o': r['o']})
    step(A, G)
print('base', rk, 'P', base['P'], 'références', len(refs), 'poses', len(jobs), flush=True)
hits = []; tot = collections.Counter(); B = 4000
for s in range(0, len(jobs), B):
    res = lot(jobs[s:s + B], 24 * P0 + 10)
    for j, inf, o in zip(jobs[s:s + B], info[s:s + B], res):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] == 'CYCLE': hits.append({**inf, 'P0': P0, 'base': rk, 'P': int(f[5]), 'sit': j})
    json.dump(hits, open('../../data/t2/t2_cascade_%d_%s.json' % (rk, mode), 'w'))
    print(s + B, dict(tot), 'CYCLE', len(hits), collections.Counter('x%d' % (x['P'] // P0) if x['P'] % P0 == 0 else 'autre' for x in hits), flush=True)
print(collections.Counter(x['P'] for x in hits).most_common(10))
