"""T2 — objets posés en 3 COPIES 3-symétriques sur une horloge triangle (une par côté) : si l'objet retarde les vaisseaux, la règle de
compensation (R-514) demande que ça arrive sur les 3 côtés à la fois (R-519) ; avec 3 copies, l'horloge peut « ralentir » (tiers T + d)
ou alterner (T + d0, T + d1 : le vaisseau porte l'état de la bascule → 2e étage possible).
Copie 1 : objet de référence posé devant un vaisseau libre (comme t2_tb_horloge.py) ; copies 2, 3 : R(objet avancé de −T), R²(objet
avancé de −2T), R = rotation 120° + c de l'horloge (état(t + T) = R(état(t))).
Usage : python3 s2_horloge/t2_sym.py Pmax mode [n]   (mode = exact | retard)  → s2_horloge/t2_sym_<mode>.json"""
import sys, json, collections, random
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, rot
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from tri import at
from exp_osc import hd
Pmax, mode = int(sys.argv[1]), sys.argv[2]; nref = int(sys.argv[3]) if len(sys.argv) > 3 else 300
O = json.load(open('../../data/t2/objets.json')); C = json.load(open('../../data/t2/conversions_effet.json'))
U = {}
for c in C:
    if mode == 'exact' and c['kind'].endswith('/ exact'): U.setdefault((c['o'], c['k']), c)
    if mode == 'retard' and c['kind'] == 'X1 ≠ X0 / retard' and abs(c['dt']) <= 12 and c['p1'] <= 42: U.setdefault((c['o'], c['k']), c)
random.seed(2); W = random.sample(sorted(U.values(), key=lambda c: (c['o'], c['k'])), min(nref, len(U)))
refs = []
for w in W:
    a, c = parts_of(O[w['o']]['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    for _ in range(w['ph']): step(A, G)
    s_a, s_c = at((0, (w['k'] - 40, 40), w['tau']), 0); A.append(list(s_a)); G.update({tuple(x): 1 for x in s_c})
    for t in range(400):
        if hd(A[2][0], A[2][1]) <= 10: break
        step(A, G)
    sx, sy, sh = A[2]
    ship = (sh, frozenset((q[0] - sx, q[1] - sy) for q in G if hd(q[0] - sx, q[1] - sy) <= 2))
    obj = ([(x - sx, y - sy, h) for x, y, h in A[:2]], [(q[0] - sx, q[1] - sy) for q in G if hd(q[0] - sx, q[1] - sy) > 2])
    refs.append({'o': w['o'], 'k': w['k'], 'p0': O[w['o']]['p'], 'dt': w.get('dt'), 'ship': ship, 'obj': obj})
def evolve(ants, cells, n):
    A = [list(t) for t in ants]; G = {tuple(t): 1 for t in cells}
    for _ in range(n): step(A, G)
    return [tuple(q) for q in A], list(G)
def R(pt, c, k=1):
    x, y = pt
    for _ in range(k): x, y = rot((x, y), 2); x, y = x + c[0], y + c[1]
    return (x, y)
one = {}
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if w['P'] <= Pmax: one.setdefault(w['P'], w)
clocks = list(one.values())
jobs = []; info = []
for ci, w in enumerate(clocks):
    P = w['P']; T = P // 3; cc = tuple(w['c']); a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    npose = collections.Counter()
    for t in range(P):
        for i, (x, y, h) in enumerate(A):
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
                        ea, ec = evolve(Pa, Pc, (-m * T) % (r['p0'] * 8))   # objet seul, reculé de m·T (modulo un multiple de sa période)
                        allA += [(*R((x_, y_), cc, m), (h_ + 2 * m) % 6) for x_, y_, h_ in ea]; allC += [R(q, cc, m) for q in ec]
                    if min(hd(p[0] - b[0], p[1] - b[1]) for p in allA for b in A) < 7: continue
                    if set(allC) & set(G) or len(set(allC)) < len(allC): continue
                    npose[(i, kk, ri)] += 1
                    jobs.append(fmt(allA + [tuple(q) for q in A], list(G) + allC)); info.append({'clock': ci, 'P0': P, 't': t, 'ship': i, 'kk': kk, 'ref': ri, 'o': r['o'], 'dt': r['dt']})
        step(A, G)
print('références', len(refs), 'horloges', len(clocks), 'poses :', len(jobs), flush=True)
hits = []; tot = collections.Counter(); B = 4000
for s in range(0, len(jobs), B):
    Tm = 12 * max(x['P0'] for x in info[s:s + B]) + 10
    res = lot(jobs[s:s + B], Tm)
    for j, inf, o in zip(jobs[s:s + B], info[s:s + B], res):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] == 'CYCLE': hits.append({**inf, 'P': int(f[5]), 'sit': j})
    json.dump(hits, open('../../data/t2/t2_sym_%s.json' % mode, 'w'))
    print(s + B, dict(tot), 'CYCLE', len(hits), collections.Counter('x%d' % (h['P'] // h['P0']) if h['P'] % h['P0'] == 0 else 'autre' for h in hits), flush=True)
print(collections.Counter((h['P0'], h['P']) for h in hits).most_common(20))
