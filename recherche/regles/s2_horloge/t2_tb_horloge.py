"""T2 — BASCULE T (tbascule.py : un oscillateur dont la PHASE est décalée par un vaisseau qui passe exactement, et remise par le suivant)
posée sur un côté d'une horloge triangle : les vaisseaux horaires successifs du même côté (un par tiers) la font basculer à chaque passage.
3 passages par période P ⇒ si la bascule alterne vraiment, la machine entière a la période 2P (diviseur par 2 / accumulateur s ← s ⊕ 1).
Pose : on simule (objet + 1er vaisseau) de tbascule jusqu'à ce que le vaisseau soit à 10 cases de l'objet (référence) ; dans l'horloge,
à chaque instant où un vaisseau libre isolé est dans le même état (à rotation près), on pose l'objet tourné au même endroit relatif.
Critère : CYCLE exact fourmi_r (T = 10 P). Usage : python3 s2_horloge/t2_tb_horloge.py Pmax"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, rot
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from tri import at
from exp_osc import hd
Pmax = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else 'tb'
O = json.load(open('../../data/t2/objets.json'))
if mode == 'tb': W = json.load(open('../../data/t2/tbw.json'))      # les bascules T de tbascule.py (étape 3)
else:                                                                   # toutes les conversions où le vaisseau ressort EXACT
    W = [dict(c, Delta=0) for c in json.load(open('../../data/t2/conversions_effet.json')) if c['kind'].endswith('/ exact')]
MAXPOSE = 3 if mode != 'tb' else 10**9
refs = []; seen = set()
for w in W:
    if (w['o'], w['k']) in seen: continue
    seen.add((w['o'], w['k']))
    a, c = parts_of(O[w['o']]['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    for _ in range(w['ph']): step(A, G)
    s_a, s_c = at((0, (w['k'] - 40, 40), w['tau']), 0)
    A.append(list(s_a)); G.update({tuple(x): 1 for x in s_c})
    for t in range(400):
        if hd(A[2][0], A[2][1]) <= 10: break
        step(A, G)
    sx, sy, sh = A[2]
    ship = (sh, frozenset((q[0] - sx, q[1] - sy) for q in G if hd(q[0] - sx, q[1] - sy) <= 2))
    obj = ([(x - sx, y - sy, h) for x, y, h in A[:2]], [(q[0] - sx, q[1] - sy) for q in G if hd(q[0] - sx, q[1] - sy) > 2])
    refs.append({'o': w['o'], 'k': w['k'], 'p0': O[w['o']]['p'], 'ship': ship, 'obj': obj, 'Deltas': sorted({x['Delta'] for x in W if x['o'] == w['o'] and x['k'] == w['k']})})
print('bascules de référence :', [(r['o'], r['k'], r['p0']) for r in refs], flush=True)
clocks = [w for w in json.load(open('s2_horloge/tri_cycles_rB5.json')) if w['P'] <= Pmax]
if mode != 'tb':
    one = {}
    for w in clocks: one.setdefault(w['P'], w)
    clocks = list(one.values())
jobs = []; info = []
for ci, w in enumerate(clocks):
    P = w['P']; a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    npose = collections.Counter()
    for t in range(P):
        for i, (x, y, h) in enumerate(A):
            if min(hd(x - b[0], y - b[1]) for j, b in enumerate(A) if j != i) < 12: continue
            loc = frozenset((q[0] - x, q[1] - y) for q in G if hd(q[0] - x, q[1] - y) <= 2)
            for ri, r in enumerate(refs):
                for kk in range(6):
                    if h != (r['ship'][0] + kk) % 6 or loc != frozenset(rot(q, kk) for q in r['ship'][1]): continue
                    Pa = [(*(lambda v: (v[0] + x, v[1] + y))(rot((px, py), kk)), (ph + kk) % 6) for px, py, ph in r['obj'][0]]
                    Pc = [(lambda v: (v[0] + x, v[1] + y))(rot(q, kk)) for q in r['obj'][1]]
                    if min(hd(p[0] - b[0], p[1] - b[1]) for p in Pa for j, b in enumerate(A) if j != i) < 8: continue
                    if any(q in G for q in Pc): continue
                    if npose[(i, kk, ri)] >= MAXPOSE: continue
                    npose[(i, kk, ri)] += 1
                    jobs.append(fmt(Pa + [tuple(q) for q in A], list(G) + Pc)); info.append({'clock': ci, 'P0': P, 't': t, 'ship': i, 'kk': kk, 'ref': ri})
        step(A, G)
print('poses :', len(jobs), flush=True)
hits = []; tot = collections.Counter(); B = 4000
for s in range(0, len(jobs), B):
    Tm = 10 * max(x['P0'] for x in info[s:s + B]) + 10
    res = lot(jobs[s:s + B], Tm)
    for j, inf, o in zip(jobs[s:s + B], info[s:s + B], res):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] == 'CYCLE': hits.append({**inf, 'P': int(f[5]), 'sit': j})
    json.dump(hits, open('s2_horloge/t2_tb_horloge%s.json' % ('' if mode == 'tb' else '_' + mode), 'w'))
    print(s + B, dict(tot), 'CYCLE', len(hits), collections.Counter(h['P'] // h['P0'] if h['P'] % h['P0'] == 0 else -1 for h in hits), flush=True)
print(collections.Counter((h['P0'], h['P']) for h in hits).most_common(15))
